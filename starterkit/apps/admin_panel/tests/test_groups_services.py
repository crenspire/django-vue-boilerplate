from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from apps.admin_panel.dto.groups import GroupFormInputDTO
from apps.admin_panel.services.groups import create_group_service, delete_group_service, update_group_service
from apps.admin_panel.tests.helpers import GROUP_PERMS, make_staff, service_request


class GroupServicesTests(TestCase):
    def setUp(self):
        self.manager = make_staff("manager", *GROUP_PERMS)

    def test_create_group_success(self):
        result = create_group_service(GroupFormInputDTO(name="Editors", permission_ids=[]), service_request(self.manager))
        self.assertTrue(result.success, result.errors)
        self.assertTrue(Group.objects.filter(name="Editors").exists())

    def test_staff_without_permission_cannot_create(self):
        result = create_group_service(GroupFormInputDTO(name="Editors", permission_ids=[]), service_request(make_staff("plain")))
        self.assertFalse(result.success)

    def test_create_group_duplicate_name_fails(self):
        Group.objects.create(name="Existing")
        result = create_group_service(GroupFormInputDTO(name="Existing", permission_ids=[]), service_request(self.manager))
        self.assertFalse(result.success)
        self.assertIn("name", result.errors)

    def test_create_group_requires_name(self):
        result = create_group_service(GroupFormInputDTO(name="", permission_ids=[]), service_request(self.manager))
        self.assertIn("name", result.errors)

    def test_can_grant_permissions_they_hold(self):
        perm = Permission.objects.get(codename="view_group")
        result = create_group_service(GroupFormInputDTO(name="Viewers", permission_ids=[perm.id]), service_request(self.manager))
        self.assertTrue(result.success, result.errors)

    def test_cannot_grant_permissions_they_lack(self):
        perm = Permission.objects.get(codename="delete_user")
        group = Group.objects.create(name="Mine")
        result = update_group_service(group.id, GroupFormInputDTO(name="Mine", permission_ids=[perm.id]), service_request(self.manager))
        self.assertFalse(result.success)
        self.assertIn("permission_ids", result.errors)
        self.assertFalse(group.permissions.exists())

    def test_keeping_existing_ungrantable_permission_is_allowed(self):
        perm = Permission.objects.get(codename="delete_user")
        group = Group.objects.create(name="Mine")
        group.permissions.add(perm)
        result = update_group_service(group.id, GroupFormInputDTO(name="Renamed", permission_ids=[perm.id]), service_request(self.manager))
        self.assertTrue(result.success, result.errors)

    def test_update_group_success(self):
        group = Group.objects.create(name="OldName")
        result = update_group_service(group.id, GroupFormInputDTO(name="NewName", permission_ids=[]), service_request(self.manager))
        self.assertTrue(result.success, result.errors)
        group.refresh_from_db()
        self.assertEqual(group.name, "NewName")

    def test_delete_group_success(self):
        group = Group.objects.create(name="ToDelete")
        result = delete_group_service(group.id, service_request(self.manager))
        self.assertTrue(result.success)
        self.assertFalse(Group.objects.filter(pk=group.id).exists())
