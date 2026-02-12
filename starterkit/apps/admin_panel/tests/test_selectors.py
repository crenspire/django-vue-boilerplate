from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from apps.admin_panel.selectors.groups import get_group_detail_dto, get_group_list_page, get_groups_queryset
from apps.admin_panel.selectors.users import get_user_detail_dto, get_user_list_page, get_users_queryset

User = get_user_model()


class UserSelectorsTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="alice", email="alice@example.com", is_staff=True)
        User.objects.create_user(username="bob", email="bob@example.com", is_staff=False)
        User.objects.create_user(username="charlie", email="charlie@test.com", is_staff=False)

    def test_get_users_queryset_search(self):
        qs = get_users_queryset(search="alice")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().username, "alice")

    def test_get_user_list_page_pagination(self):
        items, total = get_user_list_page(page=1, page_size=2)
        self.assertEqual(len(items), 2)
        self.assertEqual(total, 3)

    def test_get_user_detail_dto(self):
        user = User.objects.first()
        dto = get_user_detail_dto(user.id)
        self.assertIsNotNone(dto)
        self.assertEqual(dto.username, user.username)
        self.assertEqual(dto.email, user.email)


class GroupSelectorsTests(TestCase):
    def setUp(self):
        Group.objects.create(name="Admins")
        Group.objects.create(name="Editors")
        Group.objects.create(name="Viewers")

    def test_get_groups_queryset_search(self):
        qs = get_groups_queryset(search="Admin")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().name, "Admins")

    def test_get_group_list_page(self):
        items, total = get_group_list_page(page=1, page_size=2)
        self.assertEqual(len(items), 2)
        self.assertEqual(total, 3)

    def test_get_group_detail_dto(self):
        group = Group.objects.first()
        dto = get_group_detail_dto(group.id)
        self.assertIsNotNone(dto)
        self.assertEqual(dto.name, group.name)
