from django.middleware.csrf import get_token
from inertia import share


def get_auth_props(request):
    """
    Build auth payload for Inertia props. Use in middleware (share) and in views (explicit pass).
    """
    user = getattr(request, "user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return {"user": None}
    return {
        "user": {
            "id": user.id,
            "username": (user.get_username() or "").strip(),
            "email": (getattr(user, "email", None) or "").strip(),
            "first_name": (getattr(user, "first_name", None) or "").strip(),
            "last_name": (getattr(user, "last_name", None) or "").strip(),
            "is_staff": getattr(user, "is_staff", False),
            "is_superuser": getattr(user, "is_superuser", False),
        }
    }


def inertia_shared_props(get_response):
    """
    Middleware to inject global Inertia props, keeping Django authoritative.
    """

    def middleware(request):
        share(
            request,
            auth=get_auth_props(request),
            csrf_token=get_token(request),
        )
        return get_response(request)

    return middleware

