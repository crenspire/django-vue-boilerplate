from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase

from apps.admin_panel.dto.auth import LoginInputDTO
from apps.admin_panel.services.auth import login_service, logout_service

User = get_user_model()

GENERIC_ERROR = "Please enter the correct username and password for a staff account."


def _request_with_session(method="GET", path="/"):
    factory = RequestFactory()
    request = factory.get(path) if method == "GET" else factory.post(path)
    session = SessionStore()
    session.create()
    request.session = session
    return request


class LoginServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="staffuser",
            password="testpass123",
            email="staff@example.com",
            is_staff=True,
            is_active=True,
        )

    def _login(self, username="staffuser", password="testpass123", next_url=None):
        return login_service(LoginInputDTO(username=username, password=password, next_url=next_url), _request_with_session("POST", "/admin/login/"))

    def test_login_success_returns_redirect(self):
        result = self._login()
        self.assertTrue(result.success)
        self.assertEqual(result.redirect_url, "/admin/")
        self.assertEqual(result.user_id, self.user.id)
        self.assertTrue(result.is_staff)

    def test_login_respects_safe_next_and_rejects_external(self):
        self.assertEqual(self._login(next_url="/admin/users/").redirect_url, "/admin/users/")
        self.assertEqual(self._login(next_url="https://evil.example/").redirect_url, "/admin/")

    def test_login_wrong_password_returns_errors(self):
        result = self._login(password="wrong")
        self.assertFalse(result.success)
        self.assertIn(GENERIC_ERROR, result.errors["non_field_errors"][0])

    def test_inactive_user_with_wrong_password_gets_generic_error(self):
        self.user.is_active = False
        self.user.save()
        result = self._login(password="wrong")
        self.assertFalse(result.success)
        self.assertIn(GENERIC_ERROR, result.errors["non_field_errors"][0])
        self.assertNotIn("inactive", str(result.errors).lower())

    def test_inactive_user_with_correct_password_gets_generic_error(self):
        self.user.is_active = False
        self.user.save()
        result = self._login()
        self.assertFalse(result.success)
        self.assertNotIn("inactive", str(result.errors).lower())

    def test_login_non_staff_returns_error(self):
        self.user.is_staff = False
        self.user.save()
        result = self._login()
        self.assertFalse(result.success)
        self.assertIn(GENERIC_ERROR, result.errors["non_field_errors"][0])

    def test_login_empty_username_returns_validation_error(self):
        result = self._login(username="")
        self.assertFalse(result.success)
        self.assertIn("username", result.errors)


class LogoutServiceTests(TestCase):
    def test_logout_returns_login_redirect(self):
        redirect_url = logout_service(_request_with_session("POST", "/logout/"))
        self.assertEqual(redirect_url, "/admin/login/?next=/admin/")
