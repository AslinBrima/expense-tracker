import csv
import json
from datetime import date, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseForm, FilterForm, SignupForm
from .models import Expense, predict_category
def home(request):
    return HttpResponse("Site working")

# ─── Auth Views ───────────────────────────────────────────────

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── Dashboard ────────────────────────────────────────────────

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    filter_form = FilterForm(request.GET)

    period = request.GET.get('period', 'month')
    category_filter = request.GET.get('category', '')
    today = date.today()

    if period == 'today':
        expenses = expenses.filter(date=today)
    elif period == 'week':
        expenses = expenses.filter(date__gte=today - timedelta(days=7))
    elif period == 'month':
        expenses = expenses.filter(date__year=today.year, date__month=today.month)

    if category_filter:
        expenses = expenses.filter(category=category_filter)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Category breakdown for chart
    category_data = (
        expenses.values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    chart_labels = [item['category'] for item in category_data]
    chart_values = [float(item['total']) for item in category_data]

    # Recent (last 7 days) daily totals for bar chart
    daily_data = {}
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        daily_data[d.strftime('%b %d')] = 0.0

    week_expenses = Expense.objects.filter(
        user=request.user,
        date__gte=today - timedelta(days=6)
    ).values('date').annotate(total=Sum('amount'))
    for item in week_expenses:
        key = item['date'].strftime('%b %d')
        if key in daily_data:
            daily_data[key] = float(item['total'])

    context = {
        'expenses': expenses[:10],
        'total': total,
        'filter_form': filter_form,
        'period': period,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'daily_labels': json.dumps(list(daily_data.keys())),
        'daily_values': json.dumps(list(daily_data.values())),
        'expense_count': expenses.count(),
    }
    return render(request, 'expenses/dashboard.html', context)


# ─── Expense CRUD ─────────────────────────────────────────────

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')
    else:
        form = ExpenseForm(initial={'date': date.today()})
    return render(request, 'expenses/expense_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'action': 'Edit', 'expense': expense})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted.')
        return redirect('expense_list')
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    filter_form = FilterForm(request.GET)

    period = request.GET.get('period', 'all')
    category_filter = request.GET.get('category', '')
    today = date.today()

    if period == 'today':
        expenses = expenses.filter(date=today)
    elif period == 'week':
        expenses = expenses.filter(date__gte=today - timedelta(days=7))
    elif period == 'month':
        expenses = expenses.filter(date__year=today.year, date__month=today.month)

    if category_filter:
        expenses = expenses.filter(category=category_filter)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'total': total,
        'filter_form': filter_form,
        'period': period,
    })


# ─── Smart Category Prediction (AJAX) ─────────────────────────

@login_required
def predict_category_view(request):
    description = request.GET.get('description', '')
    category = predict_category(description)
    return JsonResponse({'category': category})


# ─── Download Report ──────────────────────────────────────────

@login_required
def download_csv(request):
    expenses = Expense.objects.filter(user=request.user)
    period = request.GET.get('period', 'all')
    today = date.today()

    if period == 'today':
        expenses = expenses.filter(date=today)
    elif period == 'week':
        expenses = expenses.filter(date__gte=today - timedelta(days=7))
    elif period == 'month':
        expenses = expenses.filter(date__year=today.year, date__month=today.month)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="expenses_{period}_{today}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Description', 'Category', 'Amount (₹)', 'Notes'])
    for expense in expenses:
        writer.writerow([
            expense.date,
            expense.description,
            expense.category,
            expense.amount,
            expense.notes or '',
        ])

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    writer.writerow([])
    writer.writerow(['', '', 'TOTAL', total, ''])

    return response
