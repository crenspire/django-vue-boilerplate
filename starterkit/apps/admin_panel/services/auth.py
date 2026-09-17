from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpRequest
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from apps.admin_panel.dto.auth import LoginInputDTO, LoginResultDTO
from apps.admin_panel.forms.errors import form_errors


def clean_next_url(request: HttpRequest, next_url: str | None) -> str:
    """
    Apply Django-style host checking to the `next` URL, falling back to the dashboard.
    """

    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return reverse("admin_dashboard")


def login_service(dto: LoginInputDTO, request: HttpRequest) -> LoginResultDTO:
    """
    Log in with Django admin's own AdminAuthenticationForm, so the rules match exactly:

    - Credentials are checked with `authenticate`.
    - Inactive and non-staff users get the same generic error as a wrong password,
      which avoids revealing whether an account exists.
    - A validated `next` parameter is used for the post-login redirect.
    """

    form = AdminAuthenticationForm(request, data={"username": dto.username, "password": dto.password})
    if not form.is_valid():
        return LoginResultDTO(
            success=False,
            redirect_url=None,
            user_id=None,
            username=None,
            is_staff=False,
            is_superuser=False,
            errors=form_errors(form),
        )

    user = form.get_user()
    django_login(request, user)

    return LoginResultDTO(
        success=True,
        redirect_url=clean_next_url(request, dto.next_url),
        user_id=user.pk,
        username=user.get_username(),
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
        errors={},
    )


def logout_service(request: HttpRequest) -> str:
    """
    Log the user out and return the appropriate redirect URL.
    """

    django_logout(request)
    return f"{reverse('login')}?next={reverse('admin_dashboard')}"
