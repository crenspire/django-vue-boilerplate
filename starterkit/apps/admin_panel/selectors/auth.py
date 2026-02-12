from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


UserModel = get_user_model()


def get_user_by_username(username: str) -> Optional[UserModel]:
    """
    Selector for looking up a user by username.

    No business logic, just a thin wrapper around the ORM.
    """

    if not username:
        return None

    return UserModel.objects.filter(username=username).first()


def get_dashboard_stats() -> dict:
    """Return aggregate counts for the admin dashboard."""
    return {
        "user_count": UserModel.objects.count(),
        "group_count": Group.objects.count(),
    }

