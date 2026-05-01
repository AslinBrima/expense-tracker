# Smart Expense Tracker (Django)

A full-featured personal finance web app built with Django.

## Features
- User Authentication (signup, login, logout)
- Add / Edit / Delete expenses
- Smart Category Prediction (keyword-based, auto-fills on typing)
- Date-wise filtering: Today / This Week / This Month / All Time
- Category filtering
- Dashboard with Pie Chart + Bar Chart (Chart.js)
- CSV Download / Export
- Django Admin panel

## Setup Instructions

### 1. Install dependencies
```bash
pip install django
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Create a superuser (optional, for admin panel)
```bash
python manage.py createsuperuser
```

### 4. Start the server
```bash
python manage.py runserver
```

### 5. Open in browser
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Default Admin Credentials
- Username: admin
- Password: admin123

## Project Structure
```
expense_tracker/
├── expense_tracker/     # Django project settings & urls
├── expenses/            # Main app (models, views, forms, urls)
├── templates/           # HTML templates
│   ├── base.html
│   ├── auth/            # login.html, signup.html
│   └── expenses/        # dashboard, list, form, delete
├── static/              # CSS/JS (Bootstrap CDN used)
├── manage.py
└── db.sqlite3           # SQLite database (auto-created)
```

## Smart Category Keywords
| Category | Keywords |
|---|---|
| Food | pizza, burger, cafe, swiggy, zomato, groceries... |
| Travel | uber, ola, taxi, train, flight, petrol, metro... |
| Shopping | amazon, flipkart, clothes, mall... |
| Entertainment | netflix, movie, spotify, hotstar... |
| Health | medicine, doctor, hospital, gym... |
| Education | book, course, tuition, udemy... |
| Utilities | electricity, wifi, phone, rent, bill... |
