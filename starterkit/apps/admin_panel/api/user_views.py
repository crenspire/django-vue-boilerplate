import dataclasses

from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods, require_POST
from inertia import render

from apps.admin_panel.api.request_utils import (
    admin_view,
    get_request_data,
    parse_bool,
    parse_id_list,
    parse_list_params,
    parse_str,
)
from apps.admin_panel.domain.grants import assignable_group_ids
from apps.admin_panel.domain.policies import (
    can_add_users,
    can_change_users,
    can_delete_user,
    can_edit_user,
    can_grant_superuser,
    can_view_users,
)
from apps.admin_panel.dto.users import UserFormInputDTO
from apps.admin_panel.selectors.groups import get_groups_choices
from apps.admin_panel.selectors.users import get_user_by_id, get_user_detail_dto, get_user_list_page
from apps.admin_panel.services.users import create_user_service, delete_user_service, update_user_service

ALLOWED_USER_ORDER_FIELDS = {
    "username", "-username", "email", "-email", "is_staff", "-is_staff", "is_active", "-is_active",
    "is_superuser", "-is_superuser", "date_joined", "-date_joined", "last_login", "-last_login",
}

EMPTY_FORM = {
    "username": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "is_staff": False,
    "is_superuser": False,
    "is_active": True,
    "group_ids": [],
    "password": "",
}


def _parse_user_form(request: HttpRequest) -> UserFormInputDTO:
    data = get_request_data(request)
    password = data.get("password")
    return UserFormInputDTO(
        username=parse_str(data, "username"),
        email=parse_str(data, "email"),
        first_name=parse_str(data, "first_name"),
        last_name=parse_str(data, "last_name"),
        is_staff=parse_bool(data, "is_staff"),
        is_superuser=parse_bool(data, "is_superuser"),
        is_active=parse_bool(data, "is_active", default=True),
        group_ids=parse_id_list(data, "group_ids"),
        password=password if isinstance(password, str) and password else None,
    )


def _form_props(request: HttpRequest, form: dict, errors: dict, *, is_self: bool = False) -> dict:
    return {
        # The password is never echoed back to the client.
        "form": {**form, "password": ""},
        "errors": errors,
        "groups_choices": get_groups_choices(assignable_group_ids(request.user)),
        "can_grant_superuser": can_grant_superuser(request.user),
        "is_self": is_self,
    }


@admin_view(can_view_users)
def user_list(request: HttpRequest):
    params = parse_list_params(request, allowed_order=ALLOWED_USER_ORDER_FIELDS, default_order="username")
    items, pagination = get_user_list_page(**params)
    return render(
        request,
        "Admin/Users/Index",
        {
            "users": [
                {
                    **dataclasses.asdict(u),
                    "can_edit": can_edit_user(request.user, u),
                    "can_delete": can_delete_user(request.user, u),
                }
                for u in items
            ],
            "pagination": dataclasses.asdict(pagination),
            "filters": {"search": params["search"] or "", "order_by": params["order_by"]},
        },
    )


@admin_view(can_add_users)
@require_http_methods(["GET", "POST"])
def user_create(request: HttpRequest):
    if request.method == "POST":
        dto = _parse_user_form(request)
        result = create_user_service(dto, request)
        if result.success:
            messages.success(request, f"User “{dto.username}” was created.")
            return redirect("admin_user_edit", user_id=result.user_id)
        return render(request, "Admin/Users/Create", _form_props(request, dataclasses.asdict(dto), result.errors))

    return render(request, "Admin/Users/Create", _form_props(request, EMPTY_FORM, {}))


@admin_view(can_change_users)
@require_http_methods(["GET", "POST"])
def user_edit(request: HttpRequest, user_id: int):
    target = get_user_by_id(user_id)
    if not target:
        messages.error(request, "That user no longer exists.")
        return redirect("admin_users")
    if not can_edit_user(request.user, target):
        messages.error(request, "Only superusers can edit superuser accounts.")
        return redirect("admin_users")

    is_self = target.pk == request.user.pk
    detail = get_user_detail_dto(user_id)
    extra = {
        "user": dataclasses.asdict(detail),
        "can_delete": can_delete_user(request.user, target),
    }

    if request.method == "POST":
        dto = _parse_user_form(request)
        result = update_user_service(user_id, dto, request)
        if result.success:
            messages.success(request, f"User “{dto.username}” was saved.")
            return redirect("admin_user_edit", user_id=user_id)
        props = _form_props(request, dataclasses.asdict(dto), result.errors, is_self=is_self)
        return render(request, "Admin/Users/Edit", {**props, **extra})

    form = {k: v for k, v in dataclasses.asdict(detail).items() if k in EMPTY_FORM}
    return render(request, "Admin/Users/Edit", {**_form_props(request, form, {}, is_self=is_self), **extra})


@admin_view(can_view_users)
@require_POST
def user_delete(request: HttpRequest, user_id: int):
    target = get_user_by_id(user_id)
    result = delete_user_service(user_id, request)
    if result.success:
        messages.success(request, f"User “{target.username}” was deleted.")
    else:
        for message in result.errors.get("non_field_errors", []):
            messages.error(request, message)
    return redirect("admin_users")
