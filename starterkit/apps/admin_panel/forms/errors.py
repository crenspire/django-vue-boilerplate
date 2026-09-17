from collections.abc import Mapping

from django import forms


def form_errors(form: forms.BaseForm, field_map: Mapping[str, str] | None = None) -> dict[str, list[str]]:
    """
    Convert Django form errors to the `{field: [messages]}` shape the frontend expects.

    `__all__` becomes `non_field_errors`; `field_map` renames form fields to payload keys.
    """
    field_map = {"__all__": "non_field_errors", **(field_map or {})}
    return {field_map.get(field, field): [str(message) for message in messages] for field, messages in form.errors.items()}
