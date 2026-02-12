from django.contrib.auth.decorators import login_required
from inertia import render

@login_required
def dashboard(request):
    return render(request, "Admin/Dashboard", {
        "auth": {
            "user": {
                "id": request.user.id,
                "email": request.user.email,
            }
        }
    })