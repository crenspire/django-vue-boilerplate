from django.contrib.auth.models import AbstractBaseUser, AnonymousUser


def can_access_admin(user: AbstractBaseUser | AnonymousUser) -> bool:
    """
    Central place for admin access rules.

    For now, we mirror Django admin and require is_staff.
    """

    return bool(getattr(user, "is_authenticated", False) and getattr(user, "is_staff", False))


def is_active_staff(user: AbstractBaseUser | AnonymousUser) -> bool:
    """
    Helper for login rules: user must be active and staff.
    """

    return bool(
        getattr(user, "is_authenticated", False)
        and getattr(user, "is_active", False)
        and getattr(user, "is_staff", False)
    )


def can_manage_users(user: AbstractBaseUser | AnonymousUser) -> bool:
    """Staff can manage users (mirror Django admin)."""
    return can_access_admin(user)


def can_manage_groups(user: AbstractBaseUser | AnonymousUser) -> bool:
    """Staff can manage groups (mirror Django admin)."""
    return can_access_admin(user)

