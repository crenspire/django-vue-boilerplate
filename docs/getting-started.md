# Getting started

## Prerequisites

- **Python 3.13** and [uv](https://docs.astral.sh/uv/)
- **Node.js** `^20.19` or `>=22.12` (required by Vite 8)

## 1. Install and migrate

```bash
git clone https://github.com/crenspire/django-vue-boilerplate.git
cd django-vue-boilerplate

uv sync
uv run python starterkit/manage.py migrate
```

## 2. Create an account

Either create your own superuser:

```bash
uv run python starterkit/manage.py createsuperuser
```

…or load demo data (26 users, 5 groups, realistic sign-up dates). This only runs with `DEBUG` on:

```bash
uv run python starterkit/manage.py seed_demo
```

| Username | Role | Password |
|----------|------|----------|
| `admin` | Superuser | `demo-password-123` |
| `manager` | Staff in "User managers" (can manage users, not groups) | `demo-password-123` |

Use `--password` to choose a different password. The command is idempotent, so running it again resets the demo accounts.

## 3. Run the dev servers

Run Django and Vite in two terminals:

```bash
# Terminal 1 — Django on http://127.0.0.1:8000
uv run python starterkit/manage.py runserver
```

```bash
# Terminal 2 — Vite on http://localhost:5173 (hot reload)
cd starterkit/frontend
npm install
npm run dev
```

Open **http://127.0.0.1:8000** for the landing page or **http://127.0.0.1:8000/admin/** for the admin.

> You always browse Django (port 8000). Django renders the HTML shell and [django-vite](https://github.com/MrBin99/django-vite) points it at the Vite dev server for JavaScript and CSS.

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| <kbd>⌘</kbd>/<kbd>Ctrl</kbd> + <kbd>K</kbd> | Command menu (pages, actions, theme) |
| <kbd>⌘</kbd>/<kbd>Ctrl</kbd> + <kbd>B</kbd> | Collapse or expand the sidebar |

## Configuration

Nothing is required locally. Every setting is an environment variable with a sensible default; see [`.env.example`](../.env.example) and [Deployment](deployment.md). To load a file:

```bash
uv run --env-file .env python starterkit/manage.py runserver
```

## Troubleshooting

**Port 5173 or 8000 is already in use.** Run Vite on another port and tell Django about it:

```bash
VITE_PORT=5174 npm run dev
DJANGO_VITE_DEV_SERVER_PORT=5174 uv run python starterkit/manage.py runserver 8001
```

**The page is blank or unstyled.** The Vite dev server isn't running (or is on a different port than `DJANGO_VITE_DEV_SERVER_PORT`). Start it, or build the assets once with `npm run build` and run Django with `DJANGO_VITE_DEV_MODE=false`.

**Form posts fail with 403 (CSRF).** Django sets the `csrftoken` cookie on every response and the Inertia client sends it back as `X-CSRFToken` (configured in `frontend/app.js`). If you rename `CSRF_COOKIE_NAME` or `CSRF_HEADER_NAME`, update the `http` options there too. Behind a proxy or on a different origin, set `DJANGO_CSRF_TRUSTED_ORIGINS`.

**"You don't have permission to access that page."** Staff accounts need model permissions for each screen. See [Permissions](permissions.md).

**`seed_demo` refuses to run.** It only works with `DJANGO_DEBUG=true`, because it creates accounts with a known password.
