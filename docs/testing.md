# Testing

## Running tests

```bash
uv run python starterkit/manage.py test apps                                   # everything
uv run python starterkit/manage.py test apps.admin_panel.tests.test_views      # one module
uv run python starterkit/manage.py test apps.admin_panel.tests.test_views.ViewTests.test_logout_requires_post
```

## What's covered

| File | Covers |
|------|--------|
| `test_auth_services.py` | Login rules, generic errors, safe `next` redirects, logout |
| `test_users_services.py` | Validation, superuser/self-edit protections, group grant limits, deletes |
| `test_groups_services.py` | Validation, permission grant limits, deletes |
| `test_selectors.py` | Search, pagination edge cases, stable ordering, annotated counts |
| `test_views.py` | Inertia responses, permission redirects, flash messages, CSRF, dashboard data |
| `test_seed_demo.py` | Demo data command and its `DEBUG` guard |

## Helpers

`apps/admin_panel/tests/helpers.py` keeps tests short:

```python
from apps.admin_panel.tests.helpers import InertiaClient, USER_PERMS, make_staff, service_request

manager = make_staff("manager", *USER_PERMS)          # active staff user with permissions
request = service_request(manager)                    # RequestFactory request for service tests

client = InertiaClient()                              # sends X-Inertia + the asset version
client.force_login(manager)
page = client.get("/admin/users/").json()             # the Inertia page object
page["component"], page["props"], page.get("flash")

client.post_json("/admin/users/create/", {"username": "new", "password": "S3cure-pass-123"})
```

Tips:

- Test **services** for business rules and **views** for wiring: permission redirects, props, flash.
- `make_staff` re-fetches the user so Django's permission cache starts empty.
- Use `InertiaClient(enforce_csrf_checks=True)` to test CSRF.

## Frontend checks

There's no JavaScript unit-test runner yet. Before committing UI changes, build once to catch template and import errors:

```bash
cd starterkit/frontend && npm run build
```

To check pages visually, see [Screenshots](screenshots/README.md). The capture script also fails if a page logs console errors.
