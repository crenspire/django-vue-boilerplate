import json
from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest
from django.shortcuts import redirect

from apps.admin_panel.domain.policies import can_access_admin

TRUE_VALUES = (True, "true", "on", 1, "1")
FALSE_VALUES = (False, "false", "off", 0, "0")


def get_request_data(request: HttpRequest) -> dict:
    """
    Return POST data as a dict. Supports both form-encoded and JSON body (Inertia).
    For form-encoded, list values (e.g. group_ids) are kept as lists; single values unwrapped.
    """
    raw = {}
    if request.content_type and "application/json" in request.content_type and request.body:
        try:
            raw = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            pass
    elif request.POST:
        raw = {k: v if len(v) != 1 else v[0] for k, v in request.POST.lists()}
    if not isinstance(raw, dict):
        return {}
    return raw


def parse_str(data: dict, key: str) -> str:
    value = data.get(key)
    return value.strip() if isinstance(value, str) else ""


def parse_bool(data: dict, key: str, default: bool = False) -> bool:
    value = data.get(key)
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    return default


def parse_id_list(data: dict, key: str) -> list[int]:
    value = data.get(key)
    if not isinstance(value, list):
        value = [] if value in (None, "") else [value]
    return [int(item) for item in value if str(item).isdigit()]


def parse_int(value, default: int, *, minimum: int, maximum: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, number))


def parse_list_params(request: HttpRequest, *, allowed_order: set[str], default_order: str) -> dict:
    """Read search/sort/pagination query params without ever raising on bad input."""
    order_by = request.GET.get("order_by", default_order)
    return {
        "search": request.GET.get("search", "").strip() or None,
        "order_by": order_by if order_by in allowed_order else default_order,
        "page": request.GET.get("page", 1),
        "page_size": parse_int(request.GET.get("page_size"), 25, minimum=1, maximum=100),
    }


def admin_view(policy=None):
    """
    Guard an admin view.

    Anonymous or non-staff users go to the login page. Staff users lacking the
    required permission get a flash message and are sent to the dashboard,
    instead of being bounced back to a login form they are already past.
    """

    def decorator(view):
        @wraps(view)
        def wrapped(request: HttpRequest, *args, **kwargs):
            if not can_access_admin(request.user):
                return redirect_to_login(request.get_full_path())
            if policy is not None and not policy(request.user):
                messages.error(request, "You don't have permission to access that page.")
                return redirect("admin_dashboard")
            return view(request, *args, **kwargs)

        return wrapped

    return decorator
