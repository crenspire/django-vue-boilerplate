from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from apps.admin_panel.domain.grants import assignable_group_ids
from apps.admin_panel.domain.policies import can_grant_superuser

User = get_user_model()


class UserAdminForm(forms.ModelForm):
    """
    Create/update form for the Inertia admin.

    Validation (username rules, uniqueness, email format, lengths and the
    configured AUTH_PASSWORD_VALIDATORS) comes from Django itself. Fields the
    acting user may not change are disabled, so submitted values are ignored.
    """

    password = forms.CharField(required=False, strip=False)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active", "groups"]

    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_create = self.instance.pk is None
        self.fields["password"].required = self.is_create

        if not can_grant_superuser(actor):
            self.fields["is_superuser"].disabled = True
        if not self.is_create and self.instance.pk == actor.pk:
            # Prevent admins from locking themselves out.
            for name in ("is_staff", "is_superuser", "is_active"):
                self.fields[name].disabled = True
        self.assignable_group_ids = assignable_group_ids(actor)

    def clean_groups(self):
        groups = self.cleaned_data["groups"]
        if self.assignable_group_ids is None:
            return groups
        existing = set(self.instance.groups.values_list("id", flat=True)) if not self.is_create else set()
        added = {group.id for group in groups} - existing
        if added - self.assignable_group_ids:
            raise ValidationError("You can only add groups whose permissions you also have.")
        return groups

    def _post_clean(self):
        super()._post_clean()
        # Validate after the instance has been populated so similarity checks see the new data.
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user
