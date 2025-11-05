# LMS API (Django + DRF)

## Local Quickstart (Windows)

1) Create venv and install deps

```
py -3 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Configure env (optional; SQLite is default)

```
copy .env.example .env  (or create .env with defaults)
```

3) Migrate and run

```
python manage.py migrate
python manage.py runserver
```

4) Create admin user (optional)

```
python manage.py createsuperuser
```

5) Seed demo data (optional)

```
python manage.py shell < seed.py
```

API base: `http://127.0.0.1:8000/api/`

- Auth: `POST /auth/login` (username, password)
- Me: `GET /auth/me`
- Books: `GET /books`, `POST /books`, `GET /books/:id`, `PATCH /books/:id`
- Borrow: `POST /borrow` (borrower_id, book_id)
- Return: `POST /return` (borrow_id)
- Reports: `/reports/circulation-summary`, `/reports/top-borrowed`

## Deploy
- Backend: Railway/Render (set `DATABASE_URL`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`)
- Start: `gunicorn core.wsgi:application --bind 0.0.0.0:8000`

