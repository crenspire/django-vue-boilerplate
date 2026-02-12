import dataclasses
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from inertia import render

from apps.admin_panel.api.request_utils import get_request_data
from apps.admin_panel.domain.policies import can_manage_groups
from apps.admin_panel.dto.groups import GroupFormInputDTO
from apps.admin_panel.selectors.groups import (
    get_all_permissions_choices,
    get_group_detail_dto,
    get_group_list_page,
)
from apps.admin_panel.services.groups import (
    create_group_service,
    delete_group_service,
    update_group_service,
)
from main.middleware import get_auth_props


def _parse_group_form_data(request: HttpRequest) -> dict:
    data = get_request_data(request)
    permission_ids = data.get("permission_ids")
    if not isinstance(permission_ids, list):
        permission_ids = [permission_ids] if permission_ids is not None and permission_ids != "" else []
    permission_ids = [int(x) for x in permission_ids if str(x).isdigit()]
    return {
        "name": (data.get("name") or "").strip(),
        "permission_ids": permission_ids,
    }


ALLOWED_GROUP_ORDER_FIELDS = {"name", "-name", "user_count", "-user_count", "permission_count", "-permission_count"}


@login_required
@user_passes_test(can_manage_groups)
def group_list(request: HttpRequest):
    search = request.GET.get("search", "").strip() or None
    page = max(1, int(request.GET.get("page", 1)))
    page_size = max(1, min(100, int(request.GET.get("page_size", 25))))
    order_by = request.GET.get("order_by", "name")
    if order_by not in ALLOWED_GROUP_ORDER_FIELDS:
        order_by = "name"
    items, total = get_group_list_page(search=search, order_by=order_by, page=page, page_size=page_size)
    return render(
        request,
        "Admin/Groups/Index",
        {
            "auth": get_auth_props(request),
            "groups": [dataclasses.asdict(g) for g in items],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size if total else 0,
            },
            "filters": {"search": search or "", "order_by": order_by},
        },
    )


@login_required
@user_passes_test(can_manage_groups)
def group_create(request: HttpRequest):
    if request.method == "POST":
        fd = _parse_group_form_data(request)
        dto = GroupFormInputDTO(
            name=fd["name"],
            permission_ids=fd["permission_ids"],
        )
        result = create_group_service(dto, request)
        if result.success and result.group_id:
            return HttpResponseRedirect(reverse("admin_group_edit", kwargs={"group_id": result.group_id}))
        return render(
            request,
            "Admin/Groups/Create",
            {
                "auth": get_auth_props(request),
                "form": {"name": dto.name, "permission_ids": dto.permission_ids},
                "errors": result.errors,
                "permissions_choices": _permissions_choices(),
            },
        )

    return render(
        request,
        "Admin/Groups/Create",
        {
            "auth": get_auth_props(request),
            "form": {"name": "", "permission_ids": []},
            "errors": {},
            "permissions_choices": _permissions_choices(),
        },
    )


@login_required
@user_passes_test(can_manage_groups)
def group_edit(request: HttpRequest, group_id: int):
    detail = get_group_detail_dto(group_id)
    if not detail:
        return HttpResponseRedirect(reverse("admin_groups"))

    if request.method == "POST":
        fd = _parse_group_form_data(request)
        dto = GroupFormInputDTO(
            name=fd["name"],
            permission_ids=fd["permission_ids"],
        )
        result = update_group_service(group_id, dto, request)
        if result.success:
            return HttpResponseRedirect(reverse("admin_group_edit", kwargs={"group_id": group_id}))
        return render(
            request,
            "Admin/Groups/Edit",
            {
                "auth": get_auth_props(request),
                "group": _detail_to_form(detail),
                "form": {"name": dto.name, "permission_ids": dto.permission_ids},
                "errors": result.errors,
                "permissions_choices": _permissions_choices(),
            },
        )

    return render(
        request,
        "Admin/Groups/Edit",
        {
            "auth": get_auth_props(request),
            "group": _detail_to_form(detail),
            "form": {"name": detail.name, "permission_ids": detail.permission_ids},
            "errors": {},
            "permissions_choices": _permissions_choices(),
        },
    )


@login_required
@user_passes_test(can_manage_groups)
def group_delete(request: HttpRequest, group_id: int):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_groups"))
    result = delete_group_service(group_id, request)
    if result.success:
        return HttpResponseRedirect(reverse("admin_groups"))
    return render(
        request,
        "Admin/Groups/Index",
        {"auth": get_auth_props(request), "errors": result.errors, "groups": [], "pagination": {"page": 1, "page_size": 25, "total": 0, "total_pages": 0}, "filters": {}},
    )


def _permissions_choices():
    return [{"id": pid, "codename": cname} for pid, cname in get_all_permissions_choices()]


def _detail_to_form(detail):
    return {
        "id": detail.id,
        "name": detail.name,
        "permission_ids": detail.permission_ids,
        "permission_codenames": detail.permission_codenames,
        "user_ids": detail.user_ids,
        "user_usernames": detail.user_usernames,
    }
