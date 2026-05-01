from django.urls import path
from django.contrib import admin
from django.urls import path
from yourapp import views
from . import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.home),
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete_expense'),

    path('api/predict-category/', views.predict_category_view, name='predict_category'),
    path('download/csv/', views.download_csv, name='download_csv'),
]
