from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from apps.admin_panel.dto.users import UserFormInputDTO
from apps.admin_panel.services.users import create_user_service, delete_user_service, update_user_service
from apps.admin_panel.tests.helpers import USER_PERMS, make_staff, service_request

User = get_user_model()


def user_dto(**overrides):
    values = dict(
        username="newuser",
        email="new@example.com",
        first_name="New",
        last_name="User",
        is_staff=False,
        is_superuser=False,
        is_active=True,
        group_ids=[],
        password="S3cure-pass-123",
    )
    values.update(overrides)
    return UserFormInputDTO(**values)


class UserServicesTests(TestCase):
    def setUp(self):
        self.manager = make_staff("manager", *USER_PERMS)
        self.root = User.objects.create_superuser("root", password="S3cure-pass-123")

    def test_create_user_success(self):
        result = create_user_service(user_dto(), service_request(self.manager))
        self.assertTrue(result.success, result.errors)
        user = User.objects.get(username="newuser")
        self.assertTrue(user.check_password("S3cure-pass-123"))

    def test_staff_without_permission_cannot_create(self):
        result = create_user_service(user_dto(), service_request(make_staff("plain")))
        self.assertFalse(result.success)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_create_user_duplicate_username_fails(self):
        User.objects.create_user(username="existing", password="x")
        result = create_user_service(user_dto(username="existing"), service_request(self.manager))
        self.assertFalse(result.success)
        self.assertIn("username", result.errors)

    def test_create_requires_password(self):
        result = create_user_service(user_dto(password=None), service_request(self.manager))
        self.assertIn("password", result.errors)

    def test_password_validators_are_enforced(self):
        result = create_user_service(user_dto(password="1"), service_request(self.manager))
        self.assertFalse(result.success)
        self.assertIn("password", result.errors)

    def test_username_and_email_are_validated(self):
        result = create_user_service(user_dto(username="x" * 300 + "<>", email="not-an-email"), service_request(self.manager))
        self.assertFalse(result.success)
        self.assertIn("username", result.errors)
        self.assertIn("email", result.errors)

    def test_non_superuser_cannot_grant_superuser(self):
        result = create_user_service(user_dto(is_superuser=True), service_request(self.manager))
        self.assertTrue(result.success, result.errors)
        self.assertFalse(User.objects.get(username="newuser").is_superuser)

    def test_non_superuser_cannot_escalate_self(self):
        dto = user_dto(username="manager", is_superuser=True, is_staff=True, password=None)
        update_user_service(self.manager.id, dto, service_request(self.manager))
        self.manager.refresh_from_db()
        self.assertFalse(self.manager.is_superuser)

    def test_cannot_lock_yourself_out(self):
        dto = user_dto(username="manager", is_staff=False, is_active=False, password=None)
        result = update_user_service(self.manager.id, dto, service_request(self.manager))
        self.assertTrue(result.success, result.errors)
        self.manager.refresh_from_db()
        self.assertTrue(self.manager.is_staff)
        self.assertTrue(self.manager.is_active)

    def test_superuser_can_grant_superuser(self):
        result = create_user_service(user_dto(is_superuser=True), service_request(self.root))
        self.assertTrue(result.success, result.errors)
        self.assertTrue(User.objects.get(username="newuser").is_superuser)

    def test_non_superuser_cannot_edit_superuser(self):
        dto = user_dto(username="root", password="Hijack-pass-123")
        result = update_user_service(self.root.id, dto, service_request(self.manager))
        self.assertFalse(result.success)
        self.root.refresh_from_db()
        self.assertTrue(self.root.check_password("S3cure-pass-123"))

    def test_non_superuser_cannot_add_group_with_permissions_they_lack(self):
        admins = Group.objects.create(name="Admins")
        admins.permissions.add(Permission.objects.get(codename="delete_group"))
        result = create_user_service(user_dto(group_ids=[admins.id]), service_request(self.manager))
        self.assertFalse(result.success)
        self.assertIn("group_ids", result.errors)

    def test_non_superuser_can_add_group_within_their_permissions(self):
        editors = Group.objects.create(name="Editors")
        editors.permissions.add(Permission.objects.get(codename="view_user"))
        result = create_user_service(user_dto(group_ids=[editors.id]), service_request(self.manager))
        self.assertTrue(result.success, result.errors)

    def test_blank_password_on_update_keeps_existing(self):
        user = User.objects.create_user(username="toupdate", password="Original-pass-123")
        dto = user_dto(username="toupdate", email="updated@example.com", password=None)
        result = update_user_service(user.id, dto, service_request(self.manager))
        self.assertTrue(result.success, result.errors)
        user.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")
        self.assertTrue(user.check_password("Original-pass-123"))

    def test_delete_user_success(self):
        user = User.objects.create_user(username="todelete", password="x")
        result = delete_user_service(user.id, service_request(self.manager))
        self.assertTrue(result.success)
        self.assertFalse(User.objects.filter(pk=user.id).exists())

    def test_cannot_delete_self(self):
        result = delete_user_service(self.manager.id, service_request(self.manager))
        self.assertFalse(result.success)
        self.assertTrue(User.objects.filter(pk=self.manager.id).exists())

    def test_non_superuser_cannot_delete_superuser(self):
        result = delete_user_service(self.root.id, service_request(self.manager))
        self.assertFalse(result.success)
        self.assertTrue(User.objects.filter(pk=self.root.id).exists())
