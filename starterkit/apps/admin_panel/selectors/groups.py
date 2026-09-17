from django.contrib.auth.models import Group, Permission
from django.db.models import Count, QuerySet

from apps.admin_panel.dto.common import PaginationDTO
from apps.admin_panel.dto.groups import GroupDetailDTO, GroupListItemDTO
from apps.admin_panel.selectors.pagination import paginate


def get_groups_queryset(
    *,
    search: str | None = None,
    order_by: str = "name",
) -> QuerySet:
    # distinct=True: two Counts over different many-to-many joins otherwise multiply each other.
    qs = Group.objects.annotate(
        user_count=Count("user", distinct=True),
        permission_count=Count("permissions", distinct=True),
    ).order_by(order_by, "id")
    if search and search.strip():
        term = search.strip()
        qs = qs.filter(name__icontains=term)
    return qs


def get_group_list_page(
    *,
    search: str | None = None,
    order_by: str = "name",
    page: int | str | None = 1,
    page_size: int = 25,
) -> tuple[list[GroupListItemDTO], PaginationDTO]:
    rows, pagination = paginate(get_groups_queryset(search=search, order_by=order_by), page=page, page_size=page_size)
    items = [
        GroupListItemDTO(
            id=g.id,
            name=g.name,
            user_count=g.user_count,
            permission_count=g.permission_count,
        )
        for g in rows
    ]
    return items, pagination


def get_group_by_id(group_id: int) -> Group | None:
    return Group.objects.filter(pk=group_id).first()


def get_group_detail_dto(group_id: int) -> GroupDetailDTO | None:
    group = get_group_by_id(group_id)
    if not group:
        return None
    perms = list(group.permissions.select_related("content_type").order_by("content_type__app_label", "codename"))
    users = list(group.user_set.order_by("username"))
    return GroupDetailDTO(
        id=group.id,
        name=group.name,
        permission_ids=[p.id for p in perms],
        permission_codenames=[f"{p.content_type.app_label}.{p.codename}" for p in perms],
        user_ids=[u.id for u in users],
        user_usernames=[u.username for u in users],
    )


def get_groups_choices(assignable_ids: set[int] | None = None) -> list[dict]:
    """
    Return `{id, name, assignable}` for all groups for use in user forms.

    `assignable_ids=None` means every group is assignable.
    """
    return [
        {"id": g.id, "name": g.name, "assignable": assignable_ids is None or g.id in assignable_ids}
        for g in Group.objects.order_by("name")
    ]


def get_all_permissions_choices(grantable_ids: set[int] | None = None) -> list[dict]:
    """
    Return `{id, codename, assignable}` for all permissions for use in group forms.

    `grantable_ids=None` means every permission is grantable.
    """
    perms = Permission.objects.select_related("content_type").order_by("content_type__app_label", "codename")
    return [
        {
            "id": p.id,
            "codename": f"{p.content_type.app_label}.{p.codename}",
            "assignable": grantable_ids is None or p.id in grantable_ids,
        }
        for p in perms
    ]
