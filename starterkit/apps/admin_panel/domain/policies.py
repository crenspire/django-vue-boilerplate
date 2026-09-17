from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

AnyUser = AbstractBaseUser | AnonymousUser


def can_access_admin(user: AnyUser) -> bool:
    """
    Central place for admin access rules.

    Mirrors Django admin: the user must be authenticated, active and staff.
    What they can do once inside is governed by model permissions below.
    """

    return bool(
        getattr(user, "is_authenticated", False)
        and getattr(user, "is_active", False)
        and getattr(user, "is_staff", False)
    )


def _has_perm(user: AnyUser, codename: str) -> bool:
    return can_access_admin(user) and user.has_perm(codename)


# --- Users -----------------------------------------------------------------


def can_view_users(user: AnyUser) -> bool:
    return _has_perm(user, "users.view_user") or _has_perm(user, "users.change_user")


def can_add_users(user: AnyUser) -> bool:
    return _has_perm(user, "users.add_user")


def can_change_users(user: AnyUser) -> bool:
    return _has_perm(user, "users.change_user")


def can_delete_users(user: AnyUser) -> bool:
    return _has_perm(user, "users.delete_user")


def can_edit_user(actor: AnyUser, target) -> bool:
    """Non-superusers may never modify a superuser account."""
    return can_change_users(actor) and (actor.is_superuser or not target.is_superuser)


def can_delete_user(actor: AnyUser, target) -> bool:
    """Nobody deletes their own account here, and only superusers delete superusers."""
    return (
        can_delete_users(actor)
        and actor.id != target.id
        and (actor.is_superuser or not target.is_superuser)
    )


def can_grant_superuser(actor: AnyUser) -> bool:
    return bool(getattr(actor, "is_superuser", False))


# --- Groups ----------------------------------------------------------------


def can_view_groups(user: AnyUser) -> bool:
    return _has_perm(user, "auth.view_group") or _has_perm(user, "auth.change_group")


def can_add_groups(user: AnyUser) -> bool:
    return _has_perm(user, "auth.add_group")


def can_change_groups(user: AnyUser) -> bool:
    return _has_perm(user, "auth.change_group")


def can_delete_groups(user: AnyUser) -> bool:
    return _has_perm(user, "auth.delete_group")


def admin_permissions(user: AnyUser) -> dict[str, bool]:
    """Capabilities exposed to the frontend so it can hide actions the user cannot take."""
    return {
        "view_users": can_view_users(user),
        "add_users": can_add_users(user),
        "change_users": can_change_users(user),
        "delete_users": can_delete_users(user),
        "view_groups": can_view_groups(user),
        "add_groups": can_add_groups(user),
        "change_groups": can_change_groups(user),
        "delete_groups": can_delete_groups(user),
    }
