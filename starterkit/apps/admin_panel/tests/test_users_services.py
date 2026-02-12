from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from apps.admin_panel.dto.users import UserFormInputDTO
from apps.admin_panel.services.users import create_user_service, delete_user_service, update_user_service

User = get_user_model()


class UserServicesTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff = User.objects.create_user(
            username="staff",
            password="testpass",
            is_staff=True,
            is_active=True,
        )

    def test_create_user_success(self):
        request = self.factory.post("/admin/users/create/")
        request.user = self.staff
        dto = UserFormInputDTO(
            username="newuser",
            email="new@example.com",
            first_name="New",
            last_name="User",
            is_staff=False,
            is_superuser=False,
            is_active=True,
            group_ids=[],
            password="securepass123",
        )
        result = create_user_service(dto, request)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.user_id)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_create_user_duplicate_username_fails(self):
        User.objects.create_user(username="existing", password="x")
        request = self.factory.post("/admin/users/create/")
        request.user = self.staff
        dto = UserFormInputDTO(
            username="existing",
            email="e@e.com",
            first_name="",
            last_name="",
            is_staff=False,
            is_superuser=False,
            is_active=True,
            group_ids=[],
            password="pass123",
        )
        result = create_user_service(dto, request)
        self.assertFalse(result.success)
        self.assertIn("username", result.errors)

    def test_update_user_success(self):
        user = User.objects.create_user(username="toupdate", password="x", is_staff=False)
        request = self.factory.post("/admin/users/1/edit/")
        request.user = self.staff
        dto = UserFormInputDTO(
            username="toupdate",
            email="updated@example.com",
            first_name="",
            last_name="",
            is_staff=False,
            is_superuser=False,
            is_active=True,
            group_ids=[],
            password=None,
        )
        result = update_user_service(user.id, dto, request)
        self.assertTrue(result.success)
        user.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")

    def test_delete_user_success(self):
        user = User.objects.create_user(username="todelete", password="x")
        request = self.factory.post("/admin/users/delete/")
        request.user = self.staff
        result = delete_user_service(user.id, request)
        self.assertTrue(result.success)
        self.assertFalse(User.objects.filter(pk=user.id).exists())
