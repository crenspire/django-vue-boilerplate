from django.contrib.auth import get_user_model, update_session_auth_hash
from django.db import IntegrityError, transaction
from django.http import HttpRequest

from apps.admin_panel.domain.policies import can_add_users, can_delete_user, can_edit_user
from apps.admin_panel.dto.users import UserFormInputDTO, UserFormResultDTO
from apps.admin_panel.forms.errors import form_errors
from apps.admin_panel.forms.users import UserAdminForm
from apps.admin_panel.selectors.users import get_user_by_id

User = get_user_model()


def _failure(message: str) -> UserFormResultDTO:
    return UserFormResultDTO(success=False, user_id=None, errors={"non_field_errors": [message]})


def _form_data(dto: UserFormInputDTO) -> dict:
    return {
        "username": dto.username,
        "email": dto.email,
        "first_name": dto.first_name,
        "last_name": dto.last_name,
        "is_staff": dto.is_staff,
        "is_superuser": dto.is_superuser,
        "is_active": dto.is_active,
        "groups": dto.group_ids,
        "password": dto.password or "",
    }


def _save(form: UserAdminForm) -> UserFormResultDTO:
    if not form.is_valid():
        return UserFormResultDTO(success=False, user_id=None, errors=form_errors(form, {"groups": "group_ids"}))
    try:
        with transaction.atomic():
            user = form.save()
    except IntegrityError:
        # Lost a race against a concurrent save with the same username.
        return UserFormResultDTO(
            success=False,
            user_id=None,
            errors={"username": ["A user with that username already exists."]},
        )
    return UserFormResultDTO(success=True, user_id=user.id, errors={})


def create_user_service(dto: UserFormInputDTO, request: HttpRequest) -> UserFormResultDTO:
    if not can_add_users(request.user):
        return _failure("Permission denied.")

    return _save(UserAdminForm(data=_form_data(dto), actor=request.user))


def update_user_service(
    user_id: int,
    dto: UserFormInputDTO,
    request: HttpRequest,
) -> UserFormResultDTO:
    user = get_user_by_id(user_id)
    if not user:
        return _failure("User not found.")
    if not can_edit_user(request.user, user):
        return _failure("Permission denied.")

    result = _save(UserAdminForm(data=_form_data(dto), instance=user, actor=request.user))

    if result.success and dto.password and user.pk == request.user.pk:
        # Keep the current session valid after changing your own password.
        update_session_auth_hash(request, user)
    return result


def delete_user_service(user_id: int, request: HttpRequest) -> UserFormResultDTO:
    user = get_user_by_id(user_id)
    if not user:
        return _failure("User not found.")
    if user.pk == request.user.pk:
        return _failure("You cannot delete your own account.")
    if not can_delete_user(request.user, user):
        return _failure("Permission denied.")

    user.delete()
    return UserFormResultDTO(success=True, user_id=None, errors={})
