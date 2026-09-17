import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, RequestFactory

User = get_user_model()


def make_staff(username="staff", *perms, **extra):
    """Create an active staff user holding the given 'app_label.codename' permissions."""
    user = User.objects.create_user(username=username, password="S3cure-pass-123", is_staff=True, **extra)
    for perm in perms:
        app_label, codename = perm.split(".")
        user.user_permissions.add(Permission.objects.get(content_type__app_label=app_label, codename=codename))
    return User.objects.get(pk=user.pk)  # Fresh instance so the permission cache is empty.


def service_request(user, path="/"):
    request = RequestFactory().post(path)
    request.user = user
    return request


class InertiaClient(Client):
    """Test client that speaks the Inertia protocol and returns the page object."""

    def __init__(self, **defaults):
        super().__init__(HTTP_X_INERTIA="true", HTTP_X_INERTIA_VERSION=settings.INERTIA_VERSION, **defaults)

    def post_json(self, path, data, **extra):
        return self.post(path, json.dumps(data), content_type="application/json", **extra)


USER_PERMS = ("users.view_user", "users.add_user", "users.change_user", "users.delete_user")
GROUP_PERMS = ("auth.view_group", "auth.add_group", "auth.change_group", "auth.delete_group")
