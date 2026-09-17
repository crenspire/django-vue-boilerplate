from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

from apps.admin_panel.dto.common import PaginationDTO
from apps.admin_panel.dto.users import UserDetailDTO, UserListItemDTO
from apps.admin_panel.selectors.pagination import paginate

User = get_user_model()


def get_users_queryset(
    *,
    search: str | None = None,
    order_by: str = "username",
) -> QuerySet:
    # `id` breaks ties so rows never shift between pages.
    qs = User.objects.all().order_by(order_by, "id")
    if search and search.strip():
        term = search.strip()
        qs = qs.filter(
            Q(username__icontains=term)
            | Q(email__icontains=term)
            | Q(first_name__icontains=term)
            | Q(last_name__icontains=term)
        )
    return qs


def get_user_list_page(
    *,
    search: str | None = None,
    order_by: str = "username",
    page: int | str | None = 1,
    page_size: int = 25,
) -> tuple[list[UserListItemDTO], PaginationDTO]:
    rows, pagination = paginate(get_users_queryset(search=search, order_by=order_by), page=page, page_size=page_size)
    items = [
        UserListItemDTO(
            id=u.id,
            username=u.username,
            full_name=u.get_full_name(),
            email=u.email or "",
            is_staff=u.is_staff,
            is_superuser=u.is_superuser,
            is_active=u.is_active,
            date_joined=u.date_joined.isoformat(),
            last_login=u.last_login.isoformat() if u.last_login else None,
        )
        for u in rows
    ]
    return items, pagination


def get_user_by_id(user_id: int) -> User | None:
    return User.objects.filter(pk=user_id).first()


def get_user_detail_dto(user_id: int) -> UserDetailDTO | None:
    user = get_user_by_id(user_id)
    if not user:
        return None
    groups = list(user.groups.order_by("name"))
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
