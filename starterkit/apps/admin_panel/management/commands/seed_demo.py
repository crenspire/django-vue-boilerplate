import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

User = get_user_model()

PEOPLE = [
    ("olivia", "Olivia", "Martin"), ("liam", "Liam", "Nguyen"), ("emma", "Emma", "Garcia"),
    ("noah", "Noah", "Patel"), ("ava", "Ava", "Kim"), ("lucas", "Lucas", "Rossi"),
    ("sofia", "Sofia", "Silva"), ("ethan", "Ethan", "Brown"), ("zoe", "Zoe", "Clark"),
    ("leo", "Leo", "Fischer"), ("isla", "Isla", "Murphy"), ("mateo", "Mateo", "Lopez"),
    ("hana", "Hana", "Sato"), ("omar", "Omar", "Haddad"), ("chloe", "Chloe", "Dubois"),
    ("arjun", "Arjun", "Mehta"), ("nora", "Nora", "Jensen"), ("felix", "Felix", "Wagner"),
    ("maya", "Maya", "Cohen"), ("kai", "Kai", "Tanaka"), ("lena", "Lena", "Novak"),
    ("samuel", "Samuel", "Okafor"), ("ruby", "Ruby", "Walsh"), ("diego", "Diego", "Ramos"),
]

GROUPS = {
    "User managers": ["view_user", "add_user", "change_user", "delete_user"],
    "Group admins": ["view_group", "add_group", "change_group", "delete_group"],
    "Editors": ["view_user", "change_user"],
    "Support": ["view_user"],
    "Auditors": ["view_user", "view_group"],
}


class Command(BaseCommand):
    help = "Create demo users and groups for local development and screenshots. Refuses to run with DEBUG off."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="demo-password-123", help="Password for the demo admin and manager accounts.")
        parser.add_argument("--seed", type=int, default=7, help="Random seed, so the data is reproducible.")

    @transaction.atomic
    def handle(self, *args, password, seed, **options):
        if not settings.DEBUG:
            raise CommandError("seed_demo only runs with DEBUG enabled; it creates accounts with a known password.")

        rnd = random.Random(seed)
        now = timezone.now()

        groups = {}
        for name, codenames in GROUPS.items():
            group, _ = Group.objects.get_or_create(name=name)
            group.permissions.set(Permission.objects.filter(codename__in=codenames))
            groups[name] = group

        admin = self._user("admin", "Alex", "Morgan", password=password, is_staff=True, is_superuser=True)
        admin.date_joined = now - timedelta(days=90)
        admin.save(update_fields=["date_joined"])

        manager = self._user("manager", "Mia", "Manager", password=password, is_staff=True)
        manager.date_joined = now - timedelta(days=75)
        manager.save(update_fields=["date_joined"])
        manager.groups.set([groups["User managers"]])

        members = []
        for index, (username, first, last) in enumerate(PEOPLE):
            user = self._user(username, first, last, is_active=index % 9 != 4)
            user.date_joined = now - timedelta(days=rnd.randint(0, 58), hours=rnd.randint(0, 23))
            user.last_login = now - timedelta(days=rnd.randint(0, 20), hours=rnd.randint(1, 23)) if rnd.random() < 0.7 else None
            user.save(update_fields=["date_joined", "last_login"])
            members.append(user)

        for name in ("Editors", "Support", "Auditors", "Group admins"):
            groups[name].user_set.set(rnd.sample(members, rnd.randint(2, 9)))

        self.stdout.write(self.style.SUCCESS(
            f"Demo data ready: {len(members) + 2} users, {len(groups)} groups. "
            f"Sign in as 'admin' (superuser) or 'manager' (user managers) with password '{password}'."
        ))

    def _user(self, username, first_name, last_name, password=None, **flags):
        user, _ = User.objects.update_or_create(
            username=username,
            defaults={"first_name": first_name, "last_name": last_name, "email": f"{username}@example.com", **flags},
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user
