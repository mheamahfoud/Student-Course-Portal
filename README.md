# AWD — Student Portal

✅ **Quick description**

AWD is a small Django-based student portal for browsing course offerings and subscribing to courses. Subscriptions are handled via an AJAX endpoint and use session-based authentication (users log in using the app's login form).

---

## 🔧 Prerequisites

- Python 3.10+ installed
- A virtual environment (recommended)
- (Optional) A database supported by Django (SQLite works out-of-the-box)

---

## 🚀 Quick start

1. Create & activate virtual environment

   Windows (PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   Windows (cmd):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run the dev server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

---

## 🧭 Main pages & endpoints

- Home: `/`
- Register: `/register/` (create account)
- Login: `/login/` (login form supports `?next=` redirect)
- Offerings (browse courses): `/offerings/`
- Dashboard: `/dashboard/` (lists user subscriptions)
- AJAX subscription endpoint: `POST /ajax/subscribe/` (expects JSON `{ "offering_id": <id> }`)
- API: `GET /api/offerings/` (returns offerings as JSON)

> Note: routes use trailing slashes. Forms and links were updated to include `/` to avoid Django's APPEND_SLASH POST redirect errors.

---

## 🔐 Subscription flow (how it works)

1. User logs in via `/login/?next=/offerings` or `/register/` then is redirected back to `/offerings/`.
2. On the offerings page, the "Subscribe" button sends a `POST` to `/ajax/subscribe/` with the offering id as JSON.
3. The backend reads the logged-in user id from `request.session['user_id']` and creates a `Subscription` record if one doesn't already exist.
4. CSRF protection is enabled: the page ensures a CSRF cookie is set and sends the `X-CSRFToken` header with the AJAX request.

---

## 🧪 Testing the process

- Visit `/offerings/` as an anonymous user and try to subscribe — you should be redirected to `/login/?next=/offerings`.
- Log in (or register) and you should return to `/offerings/`.
- Click "Subscribe" on a course: the button shows a spinner, then updates to "Subscribed" and becomes disabled.

---

## ⚙️ Troubleshooting

- If you see `ImportError: Couldn't import Django`, activate your venv and run `pip install -r requirements.txt`.
- If you see the `RuntimeError` about APPEND_SLASH and POST, ensure your forms and links point to the trailing-slash URL (e.g., `/login/`).
- If AJAX returns 401, user is not authenticated (check session handling / cookie settings).

---

## 🔮 Suggested improvements

- Migrate to Django's built-in auth (`AbstractUser`) for full auth support and admin integration.
- Add uniqueness constraint on `(user, offering)` at the database level (via migration) to prevent duplicates.
- Add more fields to `Offering` (instructor, duration, enrolled count) and corresponding migrations.
- Add automated tests for the subscription endpoint and UI flows.

---

## 📁 Project structure (top-level)

```
AWD/                 # Django app
myproject/           # Project settings
manage.py
db.sqlite3
templates/
static/
requirements.txt
README.md
```

---

If you want, I can: trim `requirements.txt` to a minimal set for this app, add a `CONTRIBUTING.md`, or convert the project to use Django's auth system. Tell me which you'd like next. 🎯
