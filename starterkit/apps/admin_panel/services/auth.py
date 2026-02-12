from typing import Dict, List

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpRequest
from django.utils.http import url_has_allowed_host_and_scheme

from apps.admin_panel.domain.policies import is_active_staff
from apps.admin_panel.dto.auth import LoginInputDTO, LoginResultDTO
from apps.admin_panel.selectors.auth import get_user_by_username


def _default_admin_redirect() -> str:
    """
    Default redirect after login when no safe `next` param is provided.
    """

    # Keep in sync with the named URL for the Inertia admin dashboard.
    return "/admin/"


def _clean_next_url(request: HttpRequest, next_url: str | None) -> str:
    """
    Apply Django-style host checking to the `next` URL.
    """

    candidate = next_url or _default_admin_redirect()

    if not url_has_allowed_host_and_scheme(
        url=candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return _default_admin_redirect()

    return candidate


def login_service(dto: LoginInputDTO, request: HttpRequest) -> LoginResultDTO:
    """
    Perform login using Django's auth stack and mirror Django admin behavior:

    - Use `authenticate` with the provided credentials.
    - Require the user to be active and `is_staff`.
    - Respect a validated `next` parameter for post-login redirect.
    """

    errors: Dict[str, List[str]] = {}

    username = (dto.username or "").strip()
    password = dto.password or ""

    # Empty field validation (similar to Django admin's form).
    if not username:
        errors.setdefault("username", []).append("This field is required.")
    if not password:
        errors.setdefault("password", []).append("This field is required.")

    if errors:
        return LoginResultDTO(
            success=False,
            redirect_url=None,
            user_id=None,
            username=None,
            is_staff=False,
            is_superuser=False,
            errors=errors,
        )

    user = authenticate(request, username=username, password=password)

    # If authentication failed, we can still distinguish between inactive and non-staff users.
    if user is None:
        existing_user = get_user_by_username(username)
        non_field_errors: list[str] = []

        if existing_user is not None and not existing_user.is_active:
            non_field_errors.append("This account is inactive.")
        else:
            non_field_errors.append(
                "Please enter the correct username and password for a staff account. "
                "Note that both fields may be case-sensitive."
            )

        errors["non_field_errors"] = non_field_errors

        return LoginResultDTO(
            success=False,
            redirect_url=None,
            user_id=None,
            username=None,
            is_staff=False,
            is_superuser=False,
            errors=errors,
        )

    # Mirror Django admin: require active staff users to log into the admin.
    if not is_active_staff(user):
        errors["non_field_errors"] = [
            "Please enter the correct username and password for a staff account. "
            "Note that both fields may be case-sensitive."
        ]
        return LoginResultDTO(
            success=False,
            redirect_url=None,
            user_id=None,
            username=None,
            is_staff=False,
            is_superuser=False,
            errors=errors,
        )

    # Successful login.
    django_login(request, user)

    redirect_url = _clean_next_url(request, dto.next_url)

    return LoginResultDTO(
        success=True,
        redirect_url=redirect_url,
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

    # After logout, send users back to the login page with a default `next` to the admin.
    return "/admin/login/?next=/admin/"

