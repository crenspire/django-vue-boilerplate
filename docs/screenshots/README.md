# Screenshots

The images in this folder are used by the project README. They're captured from demo data at 1440×900 (2× pixel density) and 390×844 for mobile.

## Regenerating

Use a throwaway database so your own data isn't touched:

```bash
# From the repository root
export DJANGO_SQLITE_PATH=/tmp/demo.sqlite3
uv run python starterkit/manage.py migrate
uv run python starterkit/manage.py seed_demo

# Build the frontend and serve it without the Vite dev server
(cd starterkit/frontend && npm run build)
DJANGO_VITE_DEV_MODE=false uv run python starterkit/manage.py runserver
```

In another terminal (same `DJANGO_SQLITE_PATH`):

```bash
export DJANGO_SQLITE_PATH=/tmp/demo.sqlite3
npm install --no-save puppeteer-core   # installs into ./node_modules (git-ignored)
node docs/screenshots/capture.mjs
```

The script signs in the demo accounts by creating Django sessions (no passwords typed), captures every page in light and dark mode, and exits with an error if a page logs console errors.

Options:

| Variable | Default |
|----------|---------|
| `BASE_URL` | `http://localhost:8000` |
| `CHROME_PATH` | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |

The greeting ("Good morning") and relative dates ("3 days ago") depend on when you run it.
