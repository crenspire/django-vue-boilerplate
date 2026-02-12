from django.http import HttpRequest
from inertia import render


def home(request: HttpRequest):
    """Landing page: hero, features, footer."""
    return render(request, "Home", {})
