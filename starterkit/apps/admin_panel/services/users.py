from typing import Dict, List

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpRequest

from apps.admin_panel.domain.policies import can_manage_users
from apps.admin_panel.dto.users import (
    UserFormInputDTO,
    UserFormResultDTO,
)
from apps.admin_panel.selectors.users import get_user_by_id

User = get_user_model()


def _check_permission(request: HttpRequest) -> UserFormResultDTO | None:
    if not can_manage_users(request.user):
        return UserFormResultDTO(
            success=False,
            user_id=None,
            errors={"non_field_errors": ["Permission denied."]},
        )
    return None


def create_user_service(dto: UserFormInputDTO, request: HttpRequest) -> UserFormResultDTO:
    denied = _check_permission(request)
    if denied:
        return denied

    errors: Dict[str, List[str]] = {}

    if not (dto.username or "").strip():
        errors.setdefault("username", []).append("This field is required.")
    if User.objects.filter(username=(dto.username or "").strip()).exists():
        errors.setdefault("username", []).append("A user with that username already exists.")

    if dto.password is None or (isinstance(dto.password, str) and len(dto.password) < 1):
        errors.setdefault("password", []).append("This field is required.")

    if errors:
        return UserFormResultDTO(success=False, user_id=None, errors=errors)

    user = User()
    user.username = (dto.username or "").strip()
    user.email = (dto.email or "").strip()
    user.first_name = (dto.first_name or "").strip()
    user.last_name = (dto.last_name or "").strip()
    user.is_staff = bool(dto.is_staff)
    user.is_superuser = bool(dto.is_superuser)
    user.is_active = bool(dto.is_active)
    if dto.password:
        user.set_password(dto.password)
    user.save()

    group_ids = getattr(dto, "group_ids", []) or []
    user.groups.set(Group.objects.filter(pk__in=group_ids))

    return UserFormResultDTO(success=True, user_id=user.id, errors={})


def update_user_service(
    user_id: int,
    dto: UserFormInputDTO,
    request: HttpRequest,
) -> UserFormResultDTO:
    denied = _check_permission(request)
    if denied:
        return denied

    user = get_user_by_id(user_id)
    if not user:
        return UserFormResultDTO(
            success=False,
            user_id=None,
            errors={"non_field_errors": ["User not found."]},
        )

    errors: Dict[str, List[str]] = {}

    username = (dto.username or "").strip()
    if not username:
        errors.setdefault("username", []).append("This field is required.")
    if User.objects.filter(username=username).exclude(pk=user_id).exists():
        errors.setdefault("username", []).append("A user with that username already exists.")

    if errors:
        return UserFormResultDTO(success=False, user_id=None, errors=errors)

    user.username = username
    user.email = (dto.email or "").strip()
    user.first_name = (dto.first_name or "").strip()
    user.last_name = (dto.last_name or "").strip()
    user.is_staff = bool(dto.is_staff)
    user.is_superuser = bool(dto.is_superuser)
    user.is_active = bool(dto.is_active)
    if dto.password is not None and dto.password != "":
        user.set_password(dto.password)
    user.save()

    group_ids = getattr(dto, "group_ids", []) or []
    user.groups.set(Group.objects.filter(pk__in=group_ids))

    return UserFormResultDTO(success=True, user_id=user.id, errors={})


def delete_user_service(user_id: int, request: HttpRequest) -> UserFormResultDTO:
    denied = _check_permission(request)
    if denied:
        return denied

    user = get_user_by_id(user_id)
    if not user:
        return UserFormResultDTO(
            success=False,
            user_id=None,
            errors={"non_field_errors": ["User not found."]},
        )

    user.delete()
    return UserFormResultDTO(success=True, user_id=None, errors={})
