from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

from apps.admin_panel.dto.users import UserDetailDTO, UserListItemDTO

User = get_user_model()


def get_users_queryset(
    *,
    search: str | None = None,
    order_by: str = "username",
) -> QuerySet:
    qs = User.objects.all().order_by(order_by)
    if search and search.strip():
        term = search.strip()
        qs = qs.filter(
            Q(username__icontains=term) | Q(email__icontains=term)
        )
    return qs


def get_user_list_page(
    *,
    search: str | None = None,
    order_by: str = "username",
    page: int = 1,
    page_size: int = 25,
) -> tuple[list[UserListItemDTO], int]:
    qs = get_users_queryset(search=search, order_by=order_by)
    total = qs.count()
    start = (page - 1) * page_size
    rows = qs[start : start + page_size]
    items = [
        UserListItemDTO(
            id=u.id,
            username=u.username,
            email=u.email or "",
            is_staff=u.is_staff,
            is_superuser=u.is_superuser,
            is_active=u.is_active,
        )
        for u in rows
    ]
    return items, total


def get_user_by_id(user_id: int) -> User | None:
    return User.objects.filter(pk=user_id).first()


def get_user_detail_dto(user_id: int) -> UserDetailDTO | None:
    user = get_user_by_id(user_id)
    if not user:
        return None
    groups = list(user.groups.all())
    return UserDetailDTO(
        id=user.id,
        username=user.username,
        email=user.email or "",
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
        is_active=user.is_active,
        group_ids=[g.id for g in groups],
        group_names=[g.name for g in groups],
    )
