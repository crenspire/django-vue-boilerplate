import dataclasses

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods, require_POST
from inertia import render

from apps.admin_panel.api.request_utils import admin_view, get_request_data, parse_id_list, parse_list_params, parse_str
from apps.admin_panel.domain.grants import grantable_permission_ids
from apps.admin_panel.domain.policies import can_add_groups, can_change_groups, can_view_groups
from apps.admin_panel.dto.groups import GroupFormInputDTO
from apps.admin_panel.selectors.groups import (
    get_all_permissions_choices,
    get_group_by_id,
    get_group_detail_dto,
    get_group_list_page,
)
from apps.admin_panel.services.groups import create_group_service, delete_group_service, update_group_service

ALLOWED_GROUP_ORDER_FIELDS = {"name", "-name", "user_count", "-user_count", "permission_count", "-permission_count"}


def _parse_group_form(request: HttpRequest) -> GroupFormInputDTO:
    data = get_request_data(request)
    return GroupFormInputDTO(name=parse_str(data, "name"), permission_ids=parse_id_list(data, "permission_ids"))


def _form_props(request: HttpRequest, form: dict, errors: dict) -> dict:
    return {
        "form": form,
        "errors": errors,
        "permissions_choices": get_all_permissions_choices(grantable_permission_ids(request.user)),
    }


@admin_view(can_view_groups)
def group_list(request: HttpRequest):
    params = parse_list_params(request, allowed_order=ALLOWED_GROUP_ORDER_FIELDS, default_order="name")
    items, pagination = get_group_list_page(**params)
    return render(
        request,
        "Admin/Groups/Index",
        {
            "groups": [dataclasses.asdict(g) for g in items],
            "pagination": dataclasses.asdict(pagination),
            "filters": {"search": params["search"] or "", "order_by": params["order_by"]},
        },
    )


@admin_view(can_add_groups)
@require_http_methods(["GET", "POST"])
def group_create(request: HttpRequest):
    if request.method == "POST":
        dto = _parse_group_form(request)
        result = create_group_service(dto, request)
        if result.success:
            messages.success(request, f"Group “{dto.name}” was created.")
            return redirect("admin_group_edit", group_id=result.group_id)
        return render(request, "Admin/Groups/Create", _form_props(request, dataclasses.asdict(dto), result.errors))

    return render(request, "Admin/Groups/Create", _form_props(request, {"name": "", "permission_ids": []}, {}))


@admin_view(can_change_groups)
@require_http_methods(["GET", "POST"])
def group_edit(request: HttpRequest, group_id: int):
    detail = get_group_detail_dto(group_id)
    if not detail:
        messages.error(request, "That group no longer exists.")
        return redirect("admin_groups")

    if request.method == "POST":
        dto = _parse_group_form(request)
        result = update_group_service(group_id, dto, request)
        if result.success:
            messages.success(request, f"Group “{dto.name}” was saved.")
            return redirect("admin_group_edit", group_id=group_id)
        props = _form_props(request, dataclasses.asdict(dto), result.errors)
        return render(request, "Admin/Groups/Edit", {**props, "group": dataclasses.asdict(detail)})

    form = {"name": detail.name, "permission_ids": detail.permission_ids}
    return render(request, "Admin/Groups/Edit", {**_form_props(request, form, {}), "group": dataclasses.asdict(detail)})


@admin_view(can_view_groups)
@require_POST
def group_delete(request: HttpRequest, group_id: int):
    group = get_group_by_id(group_id)
    result = delete_group_service(group_id, request)
    if result.success:
        messages.success(request, f"Group “{group.name}” was deleted.")
    else:
        for message in result.errors.get("non_field_errors", []):
            messages.error(request, message)
    return redirect("admin_groups")
