<script setup>
import { Link } from "@inertiajs/vue3"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/Components/ui/sidebar"
import AppLogo from "@/Components/admin/AppLogo.vue"
import NavMain from "@/Components/admin/NavMain.vue"
import NavSecondary from "@/Components/admin/NavSecondary.vue"
import NavUser from "@/Components/admin/NavUser.vue"
import { useAdminNav } from "@/composables/useAdminNav"

const { main, secondary } = useAdminNav()
</script>

<template>
  <Sidebar variant="inset" collapsible="icon">
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg" as-child tooltip="Dashboard">
            <Link href="/admin/">
              <AppLogo />
              <div class="grid flex-1 text-left text-sm leading-tight">
                <span class="truncate font-semibold">Django Inertia</span>
                <span class="truncate text-xs text-muted-foreground">Admin console</span>
              </div>
            </Link>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="main" />
      <NavSecondary :items="secondary" class="mt-auto" />
    </SidebarContent>
    <SidebarFooter>
      <NavUser />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
