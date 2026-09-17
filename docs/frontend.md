# Frontend & UI

The frontend lives in `starterkit/frontend`: Vue 3 (`<script setup>`, plain JavaScript), Inertia v3, Vite 8, Tailwind CSS 3 and [shadcn-vue](https://www.shadcn-vue.com/) components built on [reka-ui](https://reka-ui.com/).

```
frontend/
├── app.js                 # Inertia entry: page resolver, CSRF names, title template
├── main.css               # Theme tokens (shadcn "zinc"), light + dark
├── tailwind.config.js
├── Layouts/
│   ├── AdminLayout.vue    # SidebarProvider + AppSidebar + SiteHeader + CommandMenu + toasts
│   └── AuthLayout.vue     # Centered layout for the login page
├── Pages/                 # One file per Inertia component name, e.g. Admin/Users/Index.vue
├── Components/
│   ├── ui/                # shadcn-vue components (generated, lightly patched)
│   └── admin/             # App components: AppSidebar, NavMain, NavUser, SiteHeader,
│                          # CommandMenu, UserForm, GroupForm, DataTablePagination, ...
├── composables/
│   ├── useAdminNav.js     # Navigation items, filtered by permissions
│   ├── useListQuery.js    # Search/sort/pagination state for server-driven tables
│   └── useTheme.js        # light / dark / system theme
└── lib/                   # cn(), toggleId(), formatting helpers
```

## Pages and layouts

A Django view renders a component by name:

```python
return render(request, "Admin/Users/Index", {"users": [...]})
```

which resolves to `Pages/Admin/Users/Index.vue`. Pages choose a persistent layout:

```vue
<script setup>
import AdminLayout from "@/Layouts/AdminLayout.vue"
defineOptions({ layout: AdminLayout })
</script>
```

Read shared data with `usePage()`:

```js
import { usePage } from "@inertiajs/vue3"
const page = usePage()
const can = computed(() => page.props.auth?.user?.permissions ?? {})
```

## The admin shell

The layout follows shadcn's [`sidebar-07`](https://www.shadcn-vue.com/blocks) block:

- **`AppSidebar`** is an inset sidebar that collapses to icons (<kbd>⌘B</kbd>, saved in the `sidebar_state` cookie) and turns into a slide-out sheet on screens under 768px. It holds the app logo, `NavMain` (collapsible sections), `NavSecondary` (View site, Django admin, docs) and `NavUser` (account menu with theme and log out).
- **`SiteHeader`** has the sidebar toggle, breadcrumbs, search and a theme toggle. Breadcrumbs come from the page component name, so pages don't pass them in (see `crumbs` in `SiteHeader.vue`).
- **`CommandMenu`** opens with <kbd>⌘K</kbd>. It lists pages, actions and links from `useAdminNav`, plus theme switching.
- **`FlashToaster`** turns Django messages into [Sonner](https://vue-sonner.vercel.app/) toasts.

### Adding a navigation item

Edit `composables/useAdminNav.js`. Items can depend on permissions and are shared by the sidebar and command menu:

```js
can.value.view_permissions && {
  title: "Permissions",
  href: "/admin/permissions/",
  icon: KeyRound,
  isActive: isActive("/admin/permissions/"),
},
```

Then add a breadcrumb label in `SiteHeader.vue`. The full walkthrough is in [Adding an admin page](guides/adding-an-admin-page.md).

## shadcn-vue components

`Components/ui/*` were generated with the shadcn-vue CLI using the Tailwind 3 **default** style (`components.json` has `"typescript": false`). To add another component:

```bash
cd starterkit/frontend
npx shadcn-vue@latest add accordion
```

Known deviations from the generated code:

| Component | Change | Why |
|-----------|--------|-----|
| `ui/sidebar/*` | Hand-ported from the registry's TypeScript source | The CLI's TS→JS conversion fails on the sidebar |
| `ui/select/SelectContent.vue`, sidebar | `w-(--var)` → `w-[--var]` | That syntax only exists in Tailwind v4 |
| `ui/checkbox/Checkbox.vue` | Shows a dash for `indeterminate` | The generated component always shows a check |

If you regenerate one of these, re-apply the change.

## Theming

Colors are CSS variables in `main.css` (HSL channels, shadcn "zinc" palette) under `:root` and `.dark`, and Tailwind maps them to classes like `bg-background`, `text-muted-foreground` and `bg-sidebar`. To rebrand, change `--primary` and `--sidebar-primary`, or paste a theme from [ui.shadcn.com/themes](https://ui.shadcn.com/themes) (use the HSL values).

`useTheme()` exposes `theme` (`light`, `dark` or `system`), `resolvedTheme` and `setTheme()`. The choice is stored in `localStorage` under `admin-theme`, and `applyStoredTheme()` in `app.js` applies it before Vue mounts, so the page doesn't flash the wrong theme.

The font is [Geist](https://vercel.com/font), loaded from `@fontsource-variable/geist`.

## Forms

Use Inertia's `useForm` and read errors from page props:

```vue
<script setup>
import { useForm } from "@inertiajs/vue3"
const props = defineProps({ form: Object, errors: Object })
const form = useForm({ name: props.form.name })
</script>

<template>
  <form @submit.prevent="form.post('/admin/groups/create/')">
    <FormField label="Name" html-for="name" :error="errors?.name?.[0]" required>
      <Input id="name" v-model="form.name" />
    </FormField>
  </form>
</template>
```

`Checkbox` uses `v-model` (reka-ui 2 uses `modelValue`, not `checked`). For id lists, use `toggleId(form.group_ids, id, checked)` from `@/lib/utils`.

## Tables

List pages use server-side search, sorting and pagination. `useListQuery(baseUrl, props, defaultOrder)` keeps the URL in sync (`?search=&order_by=&page=&page_size=`), and `DataTablePagination` / `SortableHeader` render the controls. The allowed sort fields are whitelisted in each view (`ALLOWED_USER_ORDER_FIELDS`).

## Gotchas

- **Dialogs inside dropdown menus:** the menu's content unmounts when it closes, taking any dialog inside it along. Keep one dialog at page level and open it from the menu item's `@select`, as `Users/Index.vue` does.
- **`as-child`:** wrap links in buttons with `<Button as-child><Link ...>` so the HTML is a single `<a>`, not a button inside a link.
