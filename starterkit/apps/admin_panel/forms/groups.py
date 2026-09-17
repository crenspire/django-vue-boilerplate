from django import forms
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

from apps.admin_panel.domain.grants import grantable_permission_ids


class GroupAdminForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type"),
        required=False,
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]

    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.grantable_permission_ids = grantable_permission_ids(actor)

    def clean_permissions(self):
        permissions = self.cleaned_data["permissions"]
        if self.grantable_permission_ids is None:
            return permissions
        existing = set(self.instance.permissions.values_list("id", flat=True)) if self.instance.pk else set()
        added = {permission.id for permission in permissions} - existing
        if added - self.grantable_permission_ids:
            raise ValidationError("You can only add permissions you also have.")
        return permissions
