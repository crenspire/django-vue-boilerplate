<script setup>
import { computed } from "vue"
import { router, usePage } from "@inertiajs/vue3"
import { BadgeCheck, ChevronsUpDown, Laptop, LogOut, Moon, Sun } from "lucide-vue-next"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/Components/ui/dropdown-menu"
import { SidebarMenu, SidebarMenuButton, SidebarMenuItem, useSidebar } from "@/Components/ui/sidebar"
import UserAvatar from "@/Components/admin/UserAvatar.vue"
import { useTheme } from "@/composables/useTheme"
import { displayName } from "@/lib/format"

const page = usePage()
const user = computed(() => page.props.auth?.user)
const name = computed(() => displayName(user.value))
const role = computed(() => (user.value?.is_superuser ? "Superuser" : "Staff"))
const { isMobile } = useSidebar()
const { theme, setTheme } = useTheme()

function logout() {
  router.post("/logout/")
}
</script>

<template>
  <SidebarMenu v-if="user">
    <SidebarMenuItem>
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <SidebarMenuButton
            size="lg"
            class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            :aria-label="`Account menu for ${name}`"
          >
            <UserAvatar :user="user" />
            <div class="grid flex-1 text-left text-sm leading-tight">
              <span class="truncate font-semibold">{{ name }}</span>
              <span class="truncate text-xs text-muted-foreground">{{ user.email || role }}</span>
            </div>
            <ChevronsUpDown class="ml-auto size-4" />
          </SidebarMenuButton>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          class="w-[--reka-dropdown-menu-trigger-width] min-w-56 rounded-lg"
          :side="isMobile ? 'bottom' : 'right'"
          align="end"
          :side-offset="4"
        >
          <DropdownMenuLabel class="p-0 font-normal">
            <div class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
              <UserAvatar :user="user" />
              <div class="grid flex-1 text-left text-sm leading-tight">
                <span class="truncate font-semibold">{{ name }}</span>
                <span class="truncate text-xs text-muted-foreground">{{ user.email || user.username }}</span>
              </div>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem v-if="user.permissions?.change_users" @select="router.visit(`/admin/users/${user.id}/edit/`)">
              <BadgeCheck />
              Account
            </DropdownMenuItem>
            <DropdownMenuSub>
              <DropdownMenuSubTrigger class="gap-2">
                <Sun class="h-4 w-4 dark:hidden" />
                <Moon class="hidden h-4 w-4 dark:block" />
                Theme
              </DropdownMenuSubTrigger>
              <DropdownMenuSubContent>
                <DropdownMenuRadioGroup :model-value="theme" @update:model-value="setTheme">
                  <DropdownMenuRadioItem value="light" class="gap-2"><Sun class="h-4 w-4 text-muted-foreground" /> Light</DropdownMenuRadioItem>
                  <DropdownMenuRadioItem value="dark" class="gap-2"><Moon class="h-4 w-4 text-muted-foreground" /> Dark</DropdownMenuRadioItem>
                  <DropdownMenuRadioItem value="system" class="gap-2"><Laptop class="h-4 w-4 text-muted-foreground" /> System</DropdownMenuRadioItem>
                </DropdownMenuRadioGroup>
              </DropdownMenuSubContent>
            </DropdownMenuSub>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem @select="logout">
            <LogOut />
            Log out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </SidebarMenuItem>
  </SidebarMenu>
</template>
