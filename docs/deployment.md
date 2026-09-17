# Deployment

The app deploys as a normal Django project: a WSGI/ASGI server for Django, and static files built by Vite and gathered by `collectstatic`.

## 1. Build the frontend

```bash
cd starterkit/frontend
npm ci
npm run build          # writes frontend/dist/ including manifest.json
```

## 2. Configure the environment

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `DJANGO_DEBUG` | yes (`false`) | `true` | Production settings apply only when this is `false` |
| `DJANGO_SECRET_KEY` | yes | — | Django refuses to start without it when debug is off |
| `DJANGO_ALLOWED_HOSTS` | yes | `localhost,127.0.0.1` in debug, empty otherwise | Comma-separated |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | behind HTTPS proxies | empty | e.g. `https://admin.example.com` |
| `DJANGO_SQLITE_PATH` | no | `starterkit/db.sqlite3` | Swap `DATABASES` for Postgres in real deployments |
| `DJANGO_STATIC_ROOT` | no | `<repo>/staticfiles` | Target of `collectstatic` |
| `DJANGO_VITE_DEV_MODE` | no | same as `DJANGO_DEBUG` | Set `false` to use built assets |
| `DJANGO_SECURE_SSL_REDIRECT` | no | `true` | Set `false` if your proxy already redirects |
| `DJANGO_SECURE_HSTS_SECONDS` | no | `0` | Opt in deliberately; browsers cache HSTS |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | no | `false` | |
| `DJANGO_SECURE_HSTS_PRELOAD` | no | `false` | |

Generate a secret key with:

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

With `DJANGO_DEBUG=false`, the settings also enable secure session and CSRF cookies and trust `X-Forwarded-Proto` from your proxy.

## 3. Migrate and collect static files

```bash
uv run python starterkit/manage.py migrate
uv run python starterkit/manage.py collectstatic --noinput
uv run python starterkit/manage.py check --deploy
```

## 4. Serve

Run Django under a production server, for example:

```bash
uv add gunicorn
cd starterkit && uv run gunicorn main.wsgi:application --bind 0.0.0.0:8000
```

Serve `STATIC_ROOT` at `/static/` from your web server or CDN, or add [WhiteNoise](https://whitenoise.readthedocs.io/).

## Cache busting

Built files have hashed names, and `INERTIA_VERSION` is derived from `manifest.json`. After a deploy, Inertia notices the version change on the next navigation and does a full page load, so users don't keep running old JavaScript. Restart Django after building so it picks up the new manifest.

## Checklist

- [ ] `npm run build` ran on the release you're deploying
- [ ] `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` set
- [ ] `migrate` and `collectstatic` ran
- [ ] `check --deploy` reviewed (HSTS warnings are expected until you opt in)
- [ ] A superuser exists (`createsuperuser`). Never run `seed_demo` in production; it refuses without debug anyway.
