from django.contrib.auth.models import Group, Permission

from apps.admin_panel.domain.policies import AnyUser


def _perm_key(permission: Permission) -> str:
    return f"{permission.content_type.app_label}.{permission.codename}"


def grantable_permission_ids(actor: AnyUser) -> set[int] | None:
    """
    Permissions the actor may hand out. None means "all" (superusers).

    Without this, anyone who can edit users or groups could grant themselves
    permissions they do not have.
    """
    if actor.is_superuser:
        return None
    held = actor.get_all_permissions()
    return {p.id for p in Permission.objects.select_related("content_type") if _perm_key(p) in held}


def assignable_group_ids(actor: AnyUser) -> set[int] | None:
    """Groups whose permissions are all held by the actor. None means "all" (superusers)."""
    grantable = grantable_permission_ids(actor)
    if grantable is None:
        return None
    return {
        group.id
        for group in Group.objects.prefetch_related("permissions")
        if {p.id for p in group.permissions.all()} <= grantable
    }
