from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Travel', 'Travel'),
    ('Shopping', 'Shopping'),
    ('Entertainment', 'Entertainment'),
    ('Health', 'Health'),
    ('Education', 'Education'),
    ('Utilities', 'Utilities'),
    ('Other', 'Other'),
]

# Keyword → category mapping for smart prediction
CATEGORY_KEYWORDS = {
    'Food': ['pizza', 'burger', 'restaurant', 'cafe', 'coffee', 'lunch', 'dinner',
             'breakfast', 'swiggy', 'zomato', 'groceries', 'supermarket', 'food',
             'snack', 'bakery', 'canteen', 'biryani', 'hotel'],
    'Travel': ['uber', 'ola', 'taxi', 'bus', 'train', 'flight', 'petrol', 'fuel',
               'metro', 'auto', 'travel', 'trip', 'toll', 'parking', 'cab'],
    'Shopping': ['amazon', 'flipkart', 'clothes', 'shirt', 'shoes', 'shopping',
                 'mall', 'purchase', 'buy', 'myntra', 'meesho'],
    'Entertainment': ['movie', 'netflix', 'spotify', 'game', 'cinema', 'concert',
                      'hotstar', 'prime', 'youtube', 'subscription'],
    'Health': ['medicine', 'doctor', 'hospital', 'pharmacy', 'gym', 'medical',
               'clinic', 'health', 'vaccine', 'lab', 'test'],
    'Education': ['book', 'course', 'tuition', 'school', 'college', 'udemy',
                  'study', 'coaching', 'exam', 'fees', 'education'],
    'Utilities': ['electricity', 'water', 'internet', 'wifi', 'phone', 'mobile',
                  'recharge', 'rent', 'gas', 'bill', 'maintenance'],
}


def predict_category(description):
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    return 'Other'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.description} - ₹{self.amount} ({self.date})"
