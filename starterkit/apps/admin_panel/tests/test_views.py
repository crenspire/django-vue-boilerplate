from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.admin_panel.tests.helpers import GROUP_PERMS, USER_PERMS, InertiaClient, make_staff

User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        self.manager = make_staff("manager", *USER_PERMS, *GROUP_PERMS)
        self.client = InertiaClient()
        self.client.force_login(self.manager)

    def test_dashboard_stats(self):
        User.objects.create_user("inactive", is_active=False)
        page = self.client.get("/admin/").json()
        users = page["props"]["stats"]["users"]
        self.assertEqual((users["total"], users["active"], users["staff"], users["new_last_30_days"]), (2, 1, 1, 2))
        self.assertEqual(page["props"]["recent_users"][0]["username"], "inactive")
        self.assertEqual(page["props"]["stats"]["groups"], {"total": 0, "with_members": 0})

    def test_bad_query_params_do_not_error(self):
        for url in ("/admin/users/?page=abc&page_size=xyz", "/admin/groups/?page=-5&page_size=0&order_by=password"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)

    def test_list_page_shares_auth_and_permissions(self):
        page = self.client.get("/admin/users/").json()
        self.assertEqual(page["component"], "Admin/Users/Index")
        self.assertTrue(page["props"]["auth"]["user"]["permissions"]["delete_users"])

    def test_staff_without_permission_is_redirected_with_flash(self):
        plain = InertiaClient()
        plain.force_login(make_staff("plain"))
        response = plain.get("/admin/users/")
        self.assertRedirects(response, "/admin/", fetch_redirect_response=False)
        page = plain.get("/admin/").json()
        self.assertEqual(page["flash"]["messages"][0]["level"], "error")
        self.assertIsNone(page["props"]["stats"]["users"])
        self.assertEqual(page["props"]["recent_users"], [])

    def test_anonymous_is_sent_to_login(self):
        response = InertiaClient().get("/admin/users/")
        self.assertRedirects(response, "/admin/login/?next=/admin/users/", fetch_redirect_response=False)

    def test_login_page_redirects_authenticated_staff(self):
        response = self.client.get("/admin/login/?next=/admin/groups/")
        self.assertRedirects(response, "/admin/groups/", fetch_redirect_response=False)

    def test_login_page_explains_non_staff_session(self):
        client = InertiaClient()
        client.force_login(User.objects.create_user("normal", password="S3cure-pass-123"))
        page = client.get("/admin/login/").json()
        self.assertIn("not authorized", page["props"]["errors"]["non_field_errors"][0])

    def test_changing_own_password_keeps_session(self):
        response = self.client.post_json(
            f"/admin/users/{self.manager.id}/edit/",
            {"username": "manager", "is_staff": True, "is_active": True, "password": "Brand-new-pass-456"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get("/admin/").status_code, 200)

    def test_delete_failure_redirects_with_flash(self):
        response = self.client.post(f"/admin/users/{self.manager.id}/delete/")
        self.assertRedirects(response, "/admin/users/", fetch_redirect_response=False)
        page = self.client.get("/admin/users/").json()
        self.assertEqual(page["flash"]["messages"][0]["message"], "You cannot delete your own account.")
        self.assertTrue(len(page["props"]["users"]) > 0)

    def test_validation_errors_rerender_form_without_password(self):
        page = self.client.post_json("/admin/users/create/", {"username": "", "password": "1"}).json()
        self.assertEqual(page["component"], "Admin/Users/Create")
        self.assertIn("username", page["props"]["errors"])
        self.assertEqual(page["props"]["form"]["password"], "")

    def test_list_only_offers_actions_the_user_can_take(self):
        User.objects.create_superuser("root", password="S3cure-pass-123")
        rows = {u["username"]: u for u in self.client.get("/admin/users/").json()["props"]["users"]}
        self.assertEqual((rows["root"]["can_edit"], rows["root"]["can_delete"]), (False, False))
        self.assertEqual((rows["manager"]["can_edit"], rows["manager"]["can_delete"]), (True, False))

    def test_non_superuser_cannot_open_superuser_edit_page(self):
        root = User.objects.create_superuser("root", password="S3cure-pass-123")
        response = self.client.get(f"/admin/users/{root.id}/edit/")
        self.assertRedirects(response, "/admin/users/", fetch_redirect_response=False)

    def test_csrf_is_enforced_for_inertia_posts(self):
        client = InertiaClient(enforce_csrf_checks=True)
        client.force_login(self.manager)
        response = client.post_json("/admin/groups/create/", {"name": "x"})
        self.assertEqual(response.status_code, 403)

    def test_logout_requires_post(self):
        self.assertEqual(self.client.get("/logout/").status_code, 405)
        self.assertEqual(self.client.post("/logout/").status_code, 302)
