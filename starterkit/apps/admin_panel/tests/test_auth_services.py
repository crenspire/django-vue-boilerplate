from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase

from apps.admin_panel.dto.auth import LoginInputDTO
from apps.admin_panel.services.auth import login_service, logout_service

User = get_user_model()


def _request_with_session(method="GET", path="/"):
    factory = RequestFactory()
    request = factory.get(path) if method == "GET" else factory.post(path)
    session = SessionStore()
    session.create()
    request.session = session
    return request


class LoginServiceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="staffuser",
            password="testpass123",
            email="staff@example.com",
            is_staff=True,
            is_active=True,
        )

    def test_login_success_returns_redirect(self):
        request = _request_with_session("POST", "/admin/login/")
        dto = LoginInputDTO(username="staffuser", password="testpass123", next_url=None)
        result = login_service(dto, request)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.redirect_url)
        self.assertEqual(result.user_id, self.user.id)
        self.assertTrue(result.is_staff)

    def test_login_wrong_password_returns_errors(self):
        request = self.factory.post("/admin/login/")
        dto = LoginInputDTO(username="staffuser", password="wrong", next_url=None)
        result = login_service(dto, request)
        self.assertFalse(result.success)
        self.assertIn("non_field_errors", result.errors)

    def test_login_inactive_user_returns_error(self):
        self.user.is_active = False
        self.user.save()
        request = self.factory.post("/admin/login/")
        dto = LoginInputDTO(username="staffuser", password="testpass123", next_url=None)
        result = login_service(dto, request)
        self.assertFalse(result.success)
        self.assertIn("non_field_errors", result.errors)

    def test_login_non_staff_returns_error(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.post("/admin/login/")
        dto = LoginInputDTO(username="staffuser", password="testpass123", next_url=None)
        result = login_service(dto, request)
        self.assertFalse(result.success)

    def test_login_empty_username_returns_validation_error(self):
        request = self.factory.post("/admin/login/")
        dto = LoginInputDTO(username="", password="testpass123", next_url=None)
        result = login_service(dto, request)
        self.assertFalse(result.success)
        self.assertIn("username", result.errors)


class LogoutServiceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logout_returns_login_redirect(self):
        request = _request_with_session("POST", "/logout/")
        redirect_url = logout_service(request)
        self.assertIn("/admin/login/", redirect_url)
