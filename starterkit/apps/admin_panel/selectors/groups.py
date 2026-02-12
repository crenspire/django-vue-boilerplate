from django.contrib.auth.models import Group
from django.db.models import Count, QuerySet

from apps.admin_panel.dto.groups import GroupDetailDTO, GroupListItemDTO


def get_groups_queryset(
    *,
    search: str | None = None,
    order_by: str = "name",
) -> QuerySet:
    qs = Group.objects.annotate(
        user_count=Count("user"),
        permission_count=Count("permissions"),
    ).order_by(order_by)
    if search and search.strip():
        term = search.strip()
        qs = qs.filter(name__icontains=term)
    return qs


def get_group_list_page(
    *,
    search: str | None = None,
    order_by: str = "name",
    page: int = 1,
    page_size: int = 25,
) -> tuple[list[GroupListItemDTO], int]:
    qs = get_groups_queryset(search=search, order_by=order_by)
    total = qs.count()
    start = (page - 1) * page_size
    rows = qs[start : start + page_size]
    items = [
        GroupListItemDTO(
            id=g.id,
            name=g.name,
            user_count=g.user_count,
            permission_count=g.permission_count,
        )
        for g in rows
    ]
    return items, total


def get_group_by_id(group_id: int) -> Group | None:
    return Group.objects.filter(pk=group_id).first()


def get_group_detail_dto(group_id: int) -> GroupDetailDTO | None:
    group = get_group_by_id(group_id)
    if not group:
        return None
    perms = list(group.permissions.all().order_by("content_type__app_label", "codename"))
    users = list(group.user_set.all().order_by("username"))
    return GroupDetailDTO(
        id=group.id,
        name=group.name,
        permission_ids=[p.id for p in perms],
        permission_codenames=[f"{p.content_type.app_label}.{p.codename}" for p in perms],
        user_ids=[u.id for u in users],
        user_usernames=[u.username for u in users],
    )


def get_groups_choices() -> list[dict]:
    """Return list of {id, name} for all groups for use in user forms."""
    return [{"id": g.id, "name": g.name} for g in Group.objects.order_by("name")]


def get_all_permissions_choices() -> list[tuple[int, str]]:
    """Return (id, label) for all permissions for use in forms."""
    from django.contrib.auth.models import Permission

    perms = (
        Permission.objects.select_related("content_type")
        .order_by("content_type__app_label", "codename")
        .all()
    )
    return [(p.id, f"{p.content_type.app_label}.{p.codename}") for p in perms]
