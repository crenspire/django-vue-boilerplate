from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import RequestFactory, TestCase

from apps.admin_panel.dto.groups import GroupFormInputDTO
from apps.admin_panel.services.groups import create_group_service, delete_group_service, update_group_service

User = get_user_model()


class GroupServicesTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff = User.objects.create_user(
            username="staff",
            password="testpass",
            is_staff=True,
            is_active=True,
        )

    def test_create_group_success(self):
        request = self.factory.post("/admin/groups/create/")
        request.user = self.staff
        dto = GroupFormInputDTO(name="Editors", permission_ids=[])
        result = create_group_service(dto, request)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.group_id)
        self.assertTrue(Group.objects.filter(name="Editors").exists())

    def test_create_group_duplicate_name_fails(self):
        Group.objects.create(name="Existing")
        request = self.factory.post("/admin/groups/create/")
        request.user = self.staff
        dto = GroupFormInputDTO(name="Existing", permission_ids=[])
        result = create_group_service(dto, request)
        self.assertFalse(result.success)
        self.assertIn("name", result.errors)

    def test_update_group_success(self):
        group = Group.objects.create(name="OldName")
        request = self.factory.post("/admin/groups/1/edit/")
        request.user = self.staff
        dto = GroupFormInputDTO(name="NewName", permission_ids=[])
        result = update_group_service(group.id, dto, request)
        self.assertTrue(result.success)
        group.refresh_from_db()
        self.assertEqual(group.name, "NewName")

    def test_delete_group_success(self):
        group = Group.objects.create(name="ToDelete")
        request = self.factory.post("/admin/groups/delete/")
        request.user = self.staff
        result = delete_group_service(group.id, request)
        self.assertTrue(result.success)
        self.assertFalse(Group.objects.filter(pk=group.id).exists())
