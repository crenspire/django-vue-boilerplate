from typing import Dict, List

from django.contrib.auth.models import Group, Permission
from django.http import HttpRequest

from apps.admin_panel.domain.policies import can_manage_groups
from apps.admin_panel.dto.groups import GroupFormInputDTO, GroupFormResultDTO
from apps.admin_panel.selectors.groups import get_group_by_id


def _check_permission(request: HttpRequest) -> GroupFormResultDTO | None:
    if not can_manage_groups(request.user):
        return GroupFormResultDTO(
            success=False,
            group_id=None,
            errors={"non_field_errors": ["Permission denied."]},
        )
    return None


def create_group_service(dto: GroupFormInputDTO, request: HttpRequest) -> GroupFormResultDTO:
    denied = _check_permission(request)
    if denied:
        return denied

    errors: Dict[str, List[str]] = {}
    name = (dto.name or "").strip()
    if not name:
        errors.setdefault("name", []).append("This field is required.")
    if Group.objects.filter(name=name).exists():
        errors.setdefault("name", []).append("A group with that name already exists.")

    if errors:
        return GroupFormResultDTO(success=False, group_id=None, errors=errors)

    group = Group(name=name)
    group.save()
    permission_ids = getattr(dto, "permission_ids", []) or []
    group.permissions.set(Permission.objects.filter(pk__in=permission_ids))

    return GroupFormResultDTO(success=True, group_id=group.id, errors={})


def update_group_service(
    group_id: int,
    dto: GroupFormInputDTO,
    request: HttpRequest,
) -> GroupFormResultDTO:
    denied = _check_permission(request)
    if denied:
        return denied

    group = get_group_by_id(group_id)
    if not group:
        return GroupFormResultDTO(
            success=False,
            group_id=None,
            errors={"non_field_errors": ["Group not found."]},
        )

    errors: Dict[str, List[str]] = {}
    name = (dto.name or "").strip()
    if not name:
        errors.setdefault("name", []).append("This field is required.")
    if Group.objects.filter(name=name).exclude(pk=group_id).exists():
        errors.setdefault("name", []).append("A group with that name already exists.")

    if errors:
        return GroupFormResultDTO(success=False, group_id=None, errors=errors)

    group.name = name
    group.save()
    permission_ids = getattr(dto, "permission_ids", []) or []
    group.permissions.set(Permission.objects.filter(pk__in=permission_ids))

    return GroupFormResultDTO(success=True, group_id=group.id, errors={})


def delete_group_service(group_id: int, request: HttpRequest) -> GroupFormResultDTO:
    denied = _check_permission(request)
    if denied:
        return denied

    group = get_group_by_id(group_id)
    if not group:
        return GroupFormResultDTO(
            success=False,
            group_id=None,
            errors={"non_field_errors": ["Group not found."]},
        )

    group.delete()
    return GroupFormResultDTO(success=True, group_id=None, errors={})
