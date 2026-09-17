from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

User = get_user_model()


class SeedDemoTests(TestCase):
    @override_settings(DEBUG=True)
    def test_creates_demo_data_and_is_idempotent(self):
        call_command("seed_demo", stdout=open("/dev/null", "w"))
        call_command("seed_demo", stdout=open("/dev/null", "w"))
        self.assertEqual(User.objects.count(), 26)
        self.assertEqual(Group.objects.count(), 5)
        admin = User.objects.get(username="admin")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password("demo-password-123"))
        self.assertTrue(User.objects.get(username="manager").has_perm("users.change_user"))
        self.assertFalse(User.objects.get(username="olivia").has_usable_password())

    @override_settings(DEBUG=False)
    def test_refuses_without_debug(self):
        with self.assertRaises(CommandError):
            call_command("seed_demo")
