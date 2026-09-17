# Permissions

The admin follows Django admin's model: signing in needs a staff account, and each screen needs a model permission. On top of that, a few rules stop admins from escalating their own access.

## Signing in

Only **active staff** accounts can sign in (`AdminAuthenticationForm`). Wrong passwords, inactive accounts and non-staff accounts all get the same generic error, so the login form doesn't reveal which accounts exist.

A signed-in user without staff access who opens `/admin/` is sent to the login page with a "not authorized" message.

## Screen permissions

| Capability (`auth.user.permissions`) | Django permission | Grants |
|--------------------------------------|-------------------|--------|
| `view_users` | `users.view_user` or `users.change_user` | Users list |
| `add_users` | `users.add_user` | Add user |
| `change_users` | `users.change_user` | Edit user |
| `delete_users` | `users.delete_user` | Delete user |
| `view_groups` | `auth.view_group` or `auth.change_group` | Groups list |
| `add_groups` | `auth.add_group` | Add group |
| `change_groups` | `auth.change_group` | Edit group |
| `delete_groups` | `auth.delete_group` | Delete group |

Superusers have every permission. Grant the others through groups (for example the demo "User managers" group) or per user in the classic Django admin.

A staff user who opens a page they can't use is redirected to the dashboard with a toast. Screens they can't use are hidden from the sidebar, the command menu and the dashboard.

## Rules that prevent escalation

| Rule | Where |
|------|-------|
| Only superusers can grant or remove superuser status | `forms/users.py` disables the field for everyone else |
| Only superusers can edit or delete a superuser account | `domain/policies.py` → `can_edit_user`, `can_delete_user` |
| Nobody can delete their own account | `can_delete_user`, `delete_user_service` |
| Nobody can change their own active/staff/superuser status | `forms/users.py` disables those fields when editing yourself |
| Non-superusers can only **add** a user to groups whose permissions they already hold | `domain/grants.py` → `assignable_group_ids`, `UserAdminForm.clean_groups` |
| Non-superusers can only **add** permissions they already hold to a group | `grantable_permission_ids`, `GroupAdminForm.clean_permissions` |

Removing a group or permission is always allowed, because it only reduces access. The forms show non-grantable options as disabled, but the server check is what counts.

## Where to change the rules

- **Who can open a screen:** `apps/admin_panel/domain/policies.py`, applied in views with `@admin_view(can_...)`.
- **What the frontend sees:** `admin_permissions()` in the same file, which feeds `auth.user.permissions`.
- **What users may hand out:** `apps/admin_panel/domain/grants.py`.

Every rule has a test in `apps/admin_panel/tests/` (`test_users_services.py`, `test_groups_services.py`, `test_views.py`).
