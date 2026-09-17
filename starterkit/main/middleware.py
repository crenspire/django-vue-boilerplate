from inertia import share

from apps.admin_panel.domain.policies import admin_permissions


def get_auth_props(request):
    """
    Build the auth payload shared with every Inertia page.
    """
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {"user": None}
    return {
        "user": {
            "id": user.id,
            "username": user.get_username(),
            "email": user.email or "",
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "permissions": admin_permissions(user),
        }
    }


def inertia_shared_props(get_response):
    """
    Middleware to inject global Inertia props, keeping Django authoritative.

    Props are lazy so they are only computed when an Inertia page is rendered.
    Flash messages come from django.contrib.messages via inertia-django.
    """

    def middleware(request):
        share(request, auth=lambda: get_auth_props(request))
        return get_response(request)

    return middleware
