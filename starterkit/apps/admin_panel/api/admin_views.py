from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest
from inertia import render

from apps.admin_panel.domain.policies import can_access_admin
from apps.admin_panel.selectors.auth import get_dashboard_stats
from main.middleware import get_auth_props


@login_required
@user_passes_test(can_access_admin)
def dashboard(request: HttpRequest):
    """
    Admin dashboard page with summary statistics.
    """
    return render(request, "Admin/Dashboard", {
        "auth": get_auth_props(request),
        "stats": get_dashboard_stats(),
    })
