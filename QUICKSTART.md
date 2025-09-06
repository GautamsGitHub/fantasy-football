# Quickstart Guide for fantasy-football

This guide will help you set up and run the fantasy-football app from scratch.

## 1. Clone the repository and enter the project directory
```
git clone <repo-url>
cd fantasy-football
```

## 2. Create a virtual environment and install dependencies
```
python -m venv venv
venv\Scripts\activate  # On Windows
# Or: source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
```

## 3. Set up your `.env` file in the project root

Example:
```
DJANGO_SECRET_KEY=your-django-secret-key
MEMBER_PASSWORD_CHECK=pbkdf2_sha256$600000$wt5ierc5CehHsJQaEVMyNo$RpZKBUsO62Le6pHKy9owQU3C6fGFoZYjIXRku0K+Dew=
DATABASE_URL=notyet
```

> The above MEMBER_PASSWORD_CHECK hash is the default for the password: `memberpass`.

## 4. Apply migrations
```
python manage.py migrate
```

## 5. Seed demo data (optional, for maintainers to explore the app)
```
python manage.py seed_demo_data
```
> This will only run if your database is empty. It creates demo teams, players, fixtures, and a sample user.

## 6. Create a superuser (for admin access)
```
python manage.py createsuperuser
```

## 7. Run the development server
```
python manage.py runserver
```

## 8. Access the app
- Main site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 9. Running tests
To run the test suite (uses a separate test database, does not affect your data):
```
python manage.py test
```

---
For more details, see the code comments or ask a maintainer.
