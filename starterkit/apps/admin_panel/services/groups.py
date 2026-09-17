from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.http import HttpRequest

from apps.admin_panel.domain.policies import can_add_groups, can_change_groups, can_delete_groups
from apps.admin_panel.dto.groups import GroupFormInputDTO, GroupFormResultDTO
from apps.admin_panel.forms.errors import form_errors
from apps.admin_panel.forms.groups import GroupAdminForm
from apps.admin_panel.selectors.groups import get_group_by_id


def _failure(message: str) -> GroupFormResultDTO:
    return GroupFormResultDTO(success=False, group_id=None, errors={"non_field_errors": [message]})


def _save(dto: GroupFormInputDTO, request: HttpRequest, instance: Group | None = None) -> GroupFormResultDTO:
    form = GroupAdminForm(
        data={"name": dto.name, "permissions": dto.permission_ids},
        instance=instance,
        actor=request.user,
    )
    if not form.is_valid():
        return GroupFormResultDTO(success=False, group_id=None, errors=form_errors(form, {"permissions": "permission_ids"}))
    try:
        with transaction.atomic():
            group = form.save()
    except IntegrityError:
        return GroupFormResultDTO(
            success=False,
            group_id=None,
            errors={"name": ["Group with this Name already exists."]},
        )
    return GroupFormResultDTO(success=True, group_id=group.id, errors={})


def create_group_service(dto: GroupFormInputDTO, request: HttpRequest) -> GroupFormResultDTO:
    if not can_add_groups(request.user):
        return _failure("Permission denied.")
    return _save(dto, request)


def update_group_service(
    group_id: int,
    dto: GroupFormInputDTO,
    request: HttpRequest,
) -> GroupFormResultDTO:
    if not can_change_groups(request.user):
        return _failure("Permission denied.")
    group = get_group_by_id(group_id)
    if not group:
        return _failure("Group not found.")
    return _save(dto, request, instance=group)


def delete_group_service(group_id: int, request: HttpRequest) -> GroupFormResultDTO:
    if not can_delete_groups(request.user):
        return _failure("Permission denied.")
    group = get_group_by_id(group_id)
    if not group:
        return _failure("Group not found.")
    group.delete()
    return GroupFormResultDTO(success=True, group_id=None, errors={})
