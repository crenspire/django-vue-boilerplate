# Tutorial: adding an admin page

This guide adds a read-only **Permissions** page that lists every Django permission and how many groups grant it. It touches every layer you need for a real feature: a policy, a selector, a view, a URL, a Vue page, navigation and a test.

**Time:** about 15 minutes. Run both dev servers while you work (see [Getting started](../getting-started.md)).

## 1. Add a policy

Decide who may open the page. In `starterkit/apps/admin_panel/domain/policies.py`, add a rule next to the others and expose it to the frontend:

```python
def can_view_permissions(user: AnyUser) -> bool:
    return _has_perm(user, "auth.view_permission")
```

```python
def admin_permissions(user: AnyUser) -> dict[str, bool]:
    return {
        # ...existing entries...
        "view_permissions": can_view_permissions(user),
    }
```

`_has_perm` already requires an active staff account, and superusers pass every check.

## 2. Add a selector

Reads go in `selectors/`. Create `starterkit/apps/admin_panel/selectors/permissions.py`:

```python
from django.contrib.auth.models import Permission
from django.db.models import Count


def get_permission_rows(*, search: str | None = None) -> list[dict]:
    """Every permission with how many groups grant it."""
    qs = (
        Permission.objects.select_related("content_type")
        .annotate(group_count=Count("group", distinct=True))
        .order_by("content_type__app_label", "codename")
    )
    if search:
        qs = qs.filter(codename__icontains=search)
    return [
        {
            "id": p.id,
            "app": p.content_type.app_label,
            "codename": p.codename,
            "name": p.name,
            "group_count": p.group_count,
        }
        for p in qs
    ]
```

Return plain dicts or dataclasses. Inertia serializes props to JSON, so don't pass model instances.

## 3. Add a view and URL

Create `starterkit/apps/admin_panel/api/permission_views.py`:

```python
from django.http import HttpRequest
from inertia import render

from apps.admin_panel.api.request_utils import admin_view
from apps.admin_panel.domain.policies import can_view_permissions
from apps.admin_panel.selectors.permissions import get_permission_rows


@admin_view(can_view_permissions)
def permission_list(request: HttpRequest):
    search = request.GET.get("search", "").strip() or None
    return render(
        request,
        "Admin/Permissions/Index",
        {
            "permissions": get_permission_rows(search=search),
            "filters": {"search": search or ""},
        },
    )
```

`@admin_view(policy)` sends anonymous and non-staff users to the login page. It redirects staff users without the permission to the dashboard with an error toast.

Register it in `starterkit/main/urls.py`:

```python
from apps.admin_panel.api.permission_views import permission_list

urlpatterns = [
    # ...
    path("admin/permissions/", permission_list, name="admin_permissions"),
]
```

## 4. Add the Vue page

The component name `Admin/Permissions/Index` maps to `starterkit/frontend/Pages/Admin/Permissions/Index.vue`:

```vue
<script setup>
import { ref } from "vue"
import { router } from "@inertiajs/vue3"
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Badge } from "@/Components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/Components/ui/table"
import PageHeader from "@/Components/admin/PageHeader.vue"
import SearchBar from "@/Components/admin/SearchBar.vue"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  permissions: { type: Array, default: () => [] },
  filters: { type: Object, default: () => ({}) },
})

const search = ref(props.filters.search ?? "")

function visit(query) {
  router.get("/admin/permissions/", query, { preserveState: true, preserveScroll: true })
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageHeader title="Permissions" description="Every permission Django knows about, and how many groups grant it." />

    <SearchBar v-model="search" placeholder="Search codename…" @search="visit({ search })" @clear="visit({})" />

    <div class="overflow-hidden rounded-lg border">
      <Table>
        <TableHeader class="bg-muted/50">
          <TableRow class="hover:bg-transparent">
            <TableHead class="pl-4">Codename</TableHead>
            <TableHead>Description</TableHead>
            <TableHead class="text-right pr-4">Groups</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="permission in permissions" :key="permission.id">
            <TableCell class="pl-4 font-mono text-xs">{{ permission.app }}.{{ permission.codename }}</TableCell>
            <TableCell class="text-muted-foreground">{{ permission.name }}</TableCell>
            <TableCell class="pr-4 text-right">
              <Badge variant="outline" class="font-normal">{{ permission.group_count }}</Badge>
            </TableCell>
          </TableRow>
          <TableRow v-if="!permissions.length" class="hover:bg-transparent">
            <TableCell colspan="3" class="h-24 text-center text-muted-foreground">No permissions found.</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>
</template>
```

`PageHeader` also sets the browser tab title.

## 5. Add navigation and breadcrumbs

In `starterkit/frontend/composables/useAdminNav.js`, import an icon and add the item to `main`:

```js
import { BookOpen, ExternalLink, KeyRound, LayoutDashboard, Shield, Users, Wrench } from "lucide-vue-next"

// inside the `main` array, after Groups:
can.value.view_permissions && {
  title: "Permissions",
  href: "/admin/permissions/",
  icon: KeyRound,
  isActive: isActive("/admin/permissions/"),
},
```

The sidebar and the <kbd>⌘K</kbd> command menu both pick it up, and hide it from users without the permission.

In `starterkit/frontend/Components/admin/SiteHeader.vue`, add the section label used by the breadcrumbs:

```js
const section = {
  Users: { label: "Users", href: "/admin/users/" },
  Groups: { label: "Groups", href: "/admin/groups/" },
  Permissions: { label: "Permissions", href: "/admin/permissions/" },
}
```

## 6. Write a test

Create `starterkit/apps/admin_panel/tests/test_permission_views.py`:

```python
from django.test import TestCase

from apps.admin_panel.tests.helpers import InertiaClient, make_staff


class PermissionListTests(TestCase):
    def test_lists_permissions_for_users_with_access(self):
        client = InertiaClient()
        client.force_login(make_staff("auditor", "auth.view_permission"))
        page = client.get("/admin/permissions/?search=add_group").json()
        self.assertEqual(page["component"], "Admin/Permissions/Index")
        self.assertEqual([p["codename"] for p in page["props"]["permissions"]], ["add_group"])

    def test_staff_without_permission_is_redirected(self):
        client = InertiaClient()
        client.force_login(make_staff("plain"))
        self.assertRedirects(client.get("/admin/permissions/"), "/admin/", fetch_redirect_response=False)
```

Run it:

```bash
uv run python starterkit/manage.py test apps.admin_panel.tests.test_permission_views
```

## 7. Try it

Sign in as `admin` (or any superuser) and open **Permissions** in the sidebar. Sign in as `manager` and the item is gone, because demo managers don't have `auth.view_permission`.

## Going further

- **Writes:** add a Django form in `forms/`, a service in `services/` that checks object-level rules and saves in `transaction.atomic()`, and a view that calls `messages.success(...)` and redirects. `user_views.py` and `services/users.py` are complete examples.
- **Pagination and sorting:** use `selectors/pagination.py`, `useListQuery` and `DataTablePagination`, as in `Pages/Admin/Users/Index.vue`.
- **Dashboard stats:** extend `selectors/dashboard.py` and the `cards` computed in `Pages/Admin/Dashboard.vue`.
