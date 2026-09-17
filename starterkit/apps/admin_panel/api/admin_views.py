from django.http import HttpRequest
from inertia import render

from apps.admin_panel.api.request_utils import admin_view
from apps.admin_panel.selectors.dashboard import get_dashboard_data


@admin_view()
def dashboard(request: HttpRequest):
    """
    Admin dashboard page with summary statistics.
    """
    return render(request, "Admin/Dashboard", get_dashboard_data(request.user))
