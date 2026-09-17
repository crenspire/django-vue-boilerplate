from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from apps.admin_panel.selectors.groups import get_group_detail_dto, get_group_list_page, get_groups_queryset
from apps.admin_panel.selectors.users import get_user_detail_dto, get_user_list_page, get_users_queryset

User = get_user_model()


class UserSelectorsTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="alice", email="alice@example.com", is_staff=True)
        User.objects.create_user(username="bob", email="bob@example.com", first_name="Robert")
        User.objects.create_user(username="charlie", email="charlie@test.com")

    def test_get_users_queryset_search(self):
        qs = get_users_queryset(search="alice")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().username, "alice")

    def test_search_matches_names(self):
        self.assertEqual(get_users_queryset(search="robert").get().username, "bob")

    def test_get_user_list_page_pagination(self):
        items, pagination = get_user_list_page(page=1, page_size=2)
        self.assertEqual(len(items), 2)
        self.assertEqual(pagination.total, 3)
        self.assertEqual(pagination.total_pages, 2)

    def test_invalid_and_out_of_range_pages_do_not_error(self):
        _, pagination = get_user_list_page(page="abc", page_size=2)
        self.assertEqual(pagination.page, 1)
        items, pagination = get_user_list_page(page=99, page_size=2)
        self.assertEqual(pagination.page, 2)
        self.assertEqual(len(items), 1)

    def test_ordering_is_stable_across_pages(self):
        first, _ = get_user_list_page(order_by="is_staff", page=1, page_size=2)
        second, _ = get_user_list_page(order_by="is_staff", page=2, page_size=2)
        ids = [u.id for u in first + second]
        self.assertEqual(len(set(ids)), 3)

    def test_get_user_detail_dto(self):
        user = User.objects.first()
        dto = get_user_detail_dto(user.id)
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
        items, pagination = get_group_list_page(page=1, page_size=2)
        self.assertEqual(len(items), 2)
        self.assertEqual(pagination.total, 3)

    def test_counts_are_not_multiplied_across_relations(self):
        group = Group.objects.get(name="Admins")
        for i in range(3):
            User.objects.create_user(f"member{i}").groups.add(group)
        group.permissions.set(Permission.objects.all()[:4])
        admins = next(g for g in get_group_list_page()[0] if g.name == "Admins")
        self.assertEqual(admins.user_count, 3)
        self.assertEqual(admins.permission_count, 4)

    def test_get_group_detail_dto(self):
        group = Group.objects.first()
        dto = get_group_detail_dto(group.id)
        self.assertEqual(dto.name, group.name)
