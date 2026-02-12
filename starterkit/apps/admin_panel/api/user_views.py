import dataclasses
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from inertia import render

from apps.admin_panel.api.request_utils import get_request_data
from apps.admin_panel.domain.policies import can_manage_users
from apps.admin_panel.dto.users import UserFormInputDTO
from apps.admin_panel.selectors.groups import get_groups_choices
from apps.admin_panel.selectors.users import get_user_detail_dto, get_user_list_page
from apps.admin_panel.services.users import (
    create_user_service,
    delete_user_service,
    update_user_service,
)
from main.middleware import get_auth_props


def _parse_user_form_data(request: HttpRequest) -> dict:
    data = get_request_data(request)
    group_ids = data.get("group_ids")
    if not isinstance(group_ids, list):
        group_ids = [group_ids] if group_ids is not None and group_ids != "" else []
    group_ids = [int(x) for x in group_ids if str(x).isdigit()]
    return {
        "username": (data.get("username") or "").strip(),
        "email": (data.get("email") or "").strip(),
        "first_name": (data.get("first_name") or "").strip(),
        "last_name": (data.get("last_name") or "").strip(),
        "is_staff": data.get("is_staff") in (True, "true", "on", 1, "1"),
        "is_superuser": data.get("is_superuser") in (True, "true", "on", 1, "1"),
        "is_active": data.get("is_active") not in (False, "false", 0, "0"),
        "group_ids": group_ids,
        "password": data.get("password") or None,
    }


ALLOWED_USER_ORDER_FIELDS = {"username", "-username", "email", "-email", "is_staff", "-is_staff", "is_active", "-is_active", "is_superuser", "-is_superuser"}


@login_required
@user_passes_test(can_manage_users)
def user_list(request: HttpRequest):
    search = request.GET.get("search", "").strip() or None
    page = max(1, int(request.GET.get("page", 1)))
    page_size = max(1, min(100, int(request.GET.get("page_size", 25))))
    order_by = request.GET.get("order_by", "username")
    if order_by not in ALLOWED_USER_ORDER_FIELDS:
        order_by = "username"
    items, total = get_user_list_page(search=search, order_by=order_by, page=page, page_size=page_size)
    return render(
        request,
        "Admin/Users/Index",
        {
            "auth": get_auth_props(request),
            "users": [dataclasses.asdict(u) for u in items],
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
@user_passes_test(can_manage_users)
def user_create(request: HttpRequest):
    if request.method == "POST":
        fd = _parse_user_form_data(request)
        dto = UserFormInputDTO(
            username=fd["username"],
            email=fd["email"],
            first_name=fd["first_name"],
            last_name=fd["last_name"],
            is_staff=fd["is_staff"],
            is_superuser=fd["is_superuser"],
            is_active=fd["is_active"],
            group_ids=fd["group_ids"],
            password=fd["password"],
        )
        result = create_user_service(dto, request)
        if result.success and result.user_id:
            return HttpResponseRedirect(reverse("admin_user_edit", kwargs={"user_id": result.user_id}))
        return render(
            request,
            "Admin/Users/Create",
            {
                "auth": get_auth_props(request),
                "form": {
                    "username": dto.username,
                    "email": dto.email,
                    "first_name": dto.first_name,
                    "last_name": dto.last_name,
                    "is_staff": dto.is_staff,
                    "is_superuser": dto.is_superuser,
                    "is_active": dto.is_active,
                    "group_ids": dto.group_ids,
                    "password": "",
                },
                "errors": result.errors,
                "groups_choices": get_groups_choices(),
            },
        )

    return render(
        request,
        "Admin/Users/Create",
        {
            "auth": get_auth_props(request),
            "form": {
                "username": "",
                "email": "",
                "first_name": "",
                "last_name": "",
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
                "group_ids": [],
                "password": "",
            },
            "errors": {},
            "groups_choices": get_groups_choices(),
        },
    )


@login_required
@user_passes_test(can_manage_users)
def user_edit(request: HttpRequest, user_id: int):
    detail = get_user_detail_dto(user_id)
    if not detail:
        return HttpResponseRedirect(reverse("admin_users"))

    if request.method == "POST":
        fd = _parse_user_form_data(request)
        dto = UserFormInputDTO(
            username=fd["username"],
            email=fd["email"],
            first_name=fd["first_name"],
            last_name=fd["last_name"],
            is_staff=fd["is_staff"],
            is_superuser=fd["is_superuser"],
            is_active=fd["is_active"],
            group_ids=fd["group_ids"],
            password=fd["password"],
        )
        result = update_user_service(user_id, dto, request)
        if result.success:
            return HttpResponseRedirect(reverse("admin_user_edit", kwargs={"user_id": user_id}))
        return render(
            request,
            "Admin/Users/Edit",
            {
                "auth": get_auth_props(request),
                "user": _detail_to_form(detail),
                "form": {
                    "username": dto.username,
                    "email": dto.email,
                    "first_name": dto.first_name,
                    "last_name": dto.last_name,
                    "is_staff": dto.is_staff,
                    "is_superuser": dto.is_superuser,
                    "is_active": dto.is_active,
                    "group_ids": dto.group_ids,
                    "password": "",
                },
                "errors": result.errors,
                "groups_choices": get_groups_choices(),
            },
        )

    return render(
        request,
        "Admin/Users/Edit",
        {
            "auth": get_auth_props(request),
            "user": _detail_to_form(detail),
            "form": {
                "username": detail.username,
                "email": detail.email,
                "first_name": detail.first_name,
                "last_name": detail.last_name,
                "is_staff": detail.is_staff,
                "is_superuser": detail.is_superuser,
                "is_active": detail.is_active,
                "group_ids": detail.group_ids,
                "password": "",
            },
            "errors": {},
            "groups_choices": get_groups_choices(),
        },
    )


@login_required
@user_passes_test(can_manage_users)
def user_delete(request: HttpRequest, user_id: int):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_users"))
    result = delete_user_service(user_id, request)
    if result.success:
        return HttpResponseRedirect(reverse("admin_users"))
    return render(
        request,
        "Admin/Users/Index",
        {"auth": get_auth_props(request), "errors": result.errors, "users": [], "pagination": {"page": 1, "page_size": 25, "total": 0, "total_pages": 0}, "filters": {}},
    )


def _detail_to_form(detail):
    return {
        "id": detail.id,
        "username": detail.username,
        "email": detail.email,
        "first_name": detail.first_name,
        "last_name": detail.last_name,
        "is_staff": detail.is_staff,
        "is_superuser": detail.is_superuser,
        "is_active": detail.is_active,
        "group_ids": detail.group_ids,
        "group_names": detail.group_names,
    }
