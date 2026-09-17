import { computed } from "vue"
import { usePage } from "@inertiajs/vue3"
import { BookOpen, ExternalLink, LayoutDashboard, Shield, Users, Wrench } from "lucide-vue-next"

/**
 * Single source of truth for admin navigation, filtered by the current user's
 * permissions. Used by the sidebar and the command menu.
 */
export function useAdminNav() {
  const page = usePage()
  const can = computed(() => page.props.auth?.user?.permissions ?? {})
  const path = computed(() => new URL(page.url, window.location.origin).pathname)

  const isActive = (href, exact = false) => (exact ? path.value === href : path.value.startsWith(href))

  const main = computed(() =>
    [
      {
        title: "Dashboard",
        href: "/admin/",
        icon: LayoutDashboard,
        isActive: isActive("/admin/", true),
      },
      can.value.view_users && {
        title: "Users",
        href: "/admin/users/",
        icon: Users,
        isActive: isActive("/admin/users/"),
        items: [
          { title: "All users", href: "/admin/users/", isActive: path.value === "/admin/users/" || /\/admin\/users\/\d+/.test(path.value) },
          can.value.add_users && { title: "Add user", href: "/admin/users/create/", isActive: isActive("/admin/users/create/") },
        ].filter(Boolean),
      },
      can.value.view_groups && {
        title: "Groups",
        href: "/admin/groups/",
        icon: Shield,
        isActive: isActive("/admin/groups/"),
        items: [
          { title: "All groups", href: "/admin/groups/", isActive: path.value === "/admin/groups/" || /\/admin\/groups\/\d+/.test(path.value) },
          can.value.add_groups && { title: "Add group", href: "/admin/groups/create/", isActive: isActive("/admin/groups/create/") },
        ].filter(Boolean),
      },
    ].filter(Boolean),
  )

  // Real destinations only: these open outside the Inertia app.
  const secondary = [
    { title: "View site", href: "/", icon: ExternalLink },
    { title: "Django admin", href: "/django-admin/", icon: Wrench },
    { title: "Documentation", href: "https://github.com/crenspire/django-vue-boilerplate#readme", icon: BookOpen },
  ]

  return { main, secondary, can, path }
}
