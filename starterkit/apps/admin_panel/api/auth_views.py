from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from inertia import render

from apps.admin_panel.api.request_utils import get_request_data
from apps.admin_panel.dto.auth import LoginInputDTO
from apps.admin_panel.services.auth import login_service, logout_service


def login_view(request: HttpRequest):
    """
    Inertia-powered login view that mirrors Django admin login behavior.
    """

    data = get_request_data(request) if request.method == "POST" else {}
    next_url = (
        request.GET.get("next")
        or (data.get("next") if isinstance(data.get("next"), str) else None)
        or reverse("admin_dashboard")
    )

    if request.method == "POST":
        dto = LoginInputDTO(
            username=data.get("username", "") or "",
            password=data.get("password", "") or "",
            next_url=next_url,
        )

        result = login_service(dto, request)

        if result.success and result.redirect_url:
            return HttpResponseRedirect(result.redirect_url)

        # Re-render the login page with errors and the submitted username.
        return render(
            request,
            "Auth/Login",
            {
                "form": {
                    "username": dto.username,
                    # For security reasons, do not echo the password back to the client.
                    "password": "",
                    "next": next_url,
                },
                "errors": result.errors,
            },
        )

    # GET request: render empty login form.
    return render(
        request,
        "Auth/Login",
        {
            "form": {
                "username": "",
                "password": "",
                "next": next_url,
            },
            "errors": {},
        },
    )


@login_required
def logout_view(request: HttpRequest):
    if request.method != "POST":
        # Mirror Django admin: logout is POST-only; redirect to admin index if GET
        return HttpResponseRedirect(reverse("admin_dashboard"))

    redirect_url = logout_service(request)
    return HttpResponseRedirect(redirect_url)

