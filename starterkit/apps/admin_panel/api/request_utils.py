import json
from django.http import HttpRequest


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
