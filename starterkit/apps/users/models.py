from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Project user model.

    Defined up front so fields can be added later without a painful
    mid-project swap of AUTH_USER_MODEL.
    """
