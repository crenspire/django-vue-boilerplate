from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods, require_POST
from inertia import render

from apps.admin_panel.api.request_utils import get_request_data, parse_str
from apps.admin_panel.domain.policies import can_access_admin
from apps.admin_panel.dto.auth import LoginInputDTO
from apps.admin_panel.services.auth import clean_next_url, login_service, logout_service


def _render_login(request: HttpRequest, *, username: str, next_url: str, errors: dict):
    return render(
        request,
        "Auth/Login",
        {
            # The password is never echoed back to the client.
            "form": {"username": username, "password": "", "next": next_url},
            "errors": errors,
        },
    )


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest):
    """
    Inertia-powered login view that mirrors Django admin login behavior.
    """

    data = get_request_data(request) if request.method == "POST" else {}
    next_url = clean_next_url(request, parse_str(data, "next") or request.GET.get("next"))

    if request.method == "POST":
        dto = LoginInputDTO(
            username=parse_str(data, "username"),
            password=data.get("password") if isinstance(data.get("password"), str) else "",
            next_url=next_url,
        )
        result = login_service(dto, request)
        if result.success and result.redirect_url:
            return HttpResponseRedirect(result.redirect_url)
        return _render_login(request, username=dto.username, next_url=next_url, errors=result.errors)

    if can_access_admin(request.user):
        return redirect(next_url)

    errors = {}
    if request.user.is_authenticated:
        errors["non_field_errors"] = [
            f"You are authenticated as {request.user.get_username()}, but are not authorized to "
            "access this page. Would you like to login to a different account?"
        ]
    return _render_login(request, username="", next_url=next_url, errors=errors)


@require_POST
def logout_view(request: HttpRequest):
    return HttpResponseRedirect(logout_service(request))
