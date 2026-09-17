<script setup>
import { computed } from "vue"
import { Link, usePage } from "@inertiajs/vue3"
import { Search } from "lucide-vue-next"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/Components/ui/breadcrumb"
import { Button } from "@/Components/ui/button"
import { Separator } from "@/Components/ui/separator"
import { SidebarTrigger } from "@/Components/ui/sidebar"
import ThemeToggle from "@/Components/admin/ThemeToggle.vue"

defineEmits(["open-command"])

const page = usePage()

// Breadcrumbs are derived from the Inertia page, so pages don't need to pass them.
const crumbs = computed(() => {
  const props = page.props
  const section = {
    Users: { label: "Users", href: "/admin/users/" },
    Groups: { label: "Groups", href: "/admin/groups/" },
  }
  const [, area, view] = page.component.split("/")
  if (area === "Dashboard") return [{ label: "Dashboard" }]
  const parent = section[area]
  if (!parent) return []
  if (view === "Index") return [{ label: parent.label }]
  if (view === "Create") return [parent, { label: area === "Users" ? "Add user" : "Add group" }]
  if (view === "Edit") return [parent, { label: props.user?.username ?? props.group?.name ?? "Edit" }]
  return [parent]
})
</script>

<template>
  <header
    class="flex h-14 shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12"
  >
    <div class="flex w-full items-center gap-2 px-4">
      <SidebarTrigger class="-ml-1" />
      <Separator orientation="vertical" class="mr-2 h-4" />
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem class="hidden md:block">
            <BreadcrumbLink as-child>
              <Link href="/admin/">Admin</Link>
            </BreadcrumbLink>
          </BreadcrumbItem>
          <template v-for="(crumb, index) in crumbs" :key="crumb.label">
            <BreadcrumbSeparator :class="index === 0 ? 'hidden md:block' : ''" />
            <BreadcrumbItem>
              <BreadcrumbLink v-if="crumb.href && index < crumbs.length - 1" as-child>
                <Link :href="crumb.href">{{ crumb.label }}</Link>
              </BreadcrumbLink>
              <BreadcrumbPage v-else class="max-w-[16rem] truncate">{{ crumb.label }}</BreadcrumbPage>
            </BreadcrumbItem>
          </template>
        </BreadcrumbList>
      </Breadcrumb>

      <div class="ml-auto flex items-center gap-2">
        <Button
          variant="outline"
          class="relative hidden h-8 w-56 justify-start rounded-md bg-muted/40 px-3 text-sm font-normal text-muted-foreground shadow-none hover:bg-muted/60 sm:flex lg:w-64"
          @click="$emit('open-command')"
        >
          <Search class="mr-2 h-4 w-4" />
          Search…
          <kbd class="pointer-events-none absolute right-1.5 top-1.5 hidden h-5 select-none items-center gap-1 rounded border bg-background px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
            <span class="text-xs">⌘</span>K
          </kbd>
        </Button>
        <Button variant="ghost" size="icon" class="h-8 w-8 sm:hidden" @click="$emit('open-command')">
          <Search class="h-4 w-4" />
          <span class="sr-only">Search</span>
        </Button>
        <ThemeToggle />
      </div>
    </div>
  </header>
</template>
