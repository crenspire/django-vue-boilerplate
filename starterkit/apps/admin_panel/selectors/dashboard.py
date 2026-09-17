from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count, Q
from django.utils import timezone

from apps.admin_panel.domain.policies import AnyUser, can_view_groups, can_view_users

User = get_user_model()

RECENT_USERS_LIMIT = 6
TOP_GROUPS_LIMIT = 5


def _user_stats() -> dict:
    now = timezone.now()
    last_30 = now - timedelta(days=30)
    prev_30 = now - timedelta(days=60)
    return User.objects.aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(is_active=True)),
        staff=Count("id", filter=Q(is_staff=True)),
        new_last_30_days=Count("id", filter=Q(date_joined__gte=last_30)),
        new_previous_30_days=Count("id", filter=Q(date_joined__gte=prev_30, date_joined__lt=last_30)),
    )


def _group_stats() -> dict:
    return Group.objects.aggregate(
        total=Count("id", distinct=True),
        with_members=Count("id", filter=Q(user__isnull=False), distinct=True),
    )


def _recent_users() -> list[dict]:
    users = User.objects.order_by("-date_joined", "-id")[:RECENT_USERS_LIMIT]
    return [
        {
            "id": u.id,
            "username": u.username,
            "full_name": u.get_full_name(),
            "email": u.email or "",
            "is_active": u.is_active,
            "is_staff": u.is_staff,
            "is_superuser": u.is_superuser,
            "date_joined": u.date_joined.isoformat(),
        }
        for u in users
    ]


def _top_groups() -> list[dict]:
    groups = Group.objects.annotate(
        user_count=Count("user", distinct=True),
        permission_count=Count("permissions", distinct=True),
    ).order_by("-user_count", "name")[:TOP_GROUPS_LIMIT]
    return [
        {"id": g.id, "name": g.name, "user_count": g.user_count, "permission_count": g.permission_count}
        for g in groups
    ]


def get_dashboard_data(user: AnyUser) -> dict:
    """Aggregates for the admin dashboard, limited to what the user may view."""
    show_users = can_view_users(user)
    show_groups = can_view_groups(user)
    return {
        "stats": {
            "users": _user_stats() if show_users else None,
            "groups": _group_stats() if show_groups else None,
        },
        "recent_users": _recent_users() if show_users else [],
        "top_groups": _top_groups() if show_groups else [],
    }
