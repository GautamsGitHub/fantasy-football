

# fantasy-football
Fantasy Football. Originally for ICUAFC

## What is this?
This is a Django-based fantasy football app for running your own league, with features for team management, point scoring, and admin control.

## Key Features
- Customizable teams, players, and fixtures
- Admin interface for managing all data
- Demo data seeding for easy exploration
- Player activity (active/inactive) management
- Secure authentication and member password check

## Important Information
- **Demo Data:** Use `python manage.py seed_demo_data` to quickly populate the app for demo or exploration (only works on an empty database).
- **Environment:** You must create a `.env` file in the project root (see below).
- **Testing:** Run `python manage.py test` (uses a separate test database, does not affect your data).
- **Admin:** Access the admin at http://127.0.0.1:8000/admin/

## .env file structure

Your `.env` file should look like this (example):
```
DJANGO_SECRET_KEY=your-django-secret-key
MEMBER_PASSWORD_CHECK=pbkdf2_sha256$600000$wt5ierc5CehHsJQaEVMyNo$RpZKBUsO62Le6pHKy9owQU3C6fGFoZYjIXRku0K+Dew=
DATABASE_URL=notyet
```

> The above MEMBER_PASSWORD_CHECK hash is the default for the password: `memberpass`.

## Quickstart & Setup
See [QUICKSTART.md](QUICKSTART.md) for full setup and usage instructions.

---
For more details, see the code comments or ask a maintainer.
