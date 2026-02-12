<script setup>
import { computed, ref, onMounted, onUnmounted, watch, nextTick } from "vue"
import { Link, usePage } from "@inertiajs/inertia-vue3"
import { Inertia } from "@inertiajs/inertia"
import {
  LayoutDashboard,
  Users,
  Shield,
  LogOut,
  ChevronDown,
  Search,
  Sun,
  Moon,
  Settings,
  PanelLeftClose,
  PanelLeft,
} from "lucide-vue-next"
import { Avatar, AvatarFallback } from "@/Components/ui/avatar"
import { Button } from "@/Components/ui/button"
import { Input } from "@/Components/ui/input"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuLabel,
} from "@/Components/ui/dropdown-menu"
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/Components/ui/tooltip"
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from "@/Components/ui/dialog"
import { useTheme } from "@/composables/useTheme"
import { useSidebar } from "@/composables/useSidebar"
import { cn } from "@/lib/utils"

const iconUrl = typeof window !== "undefined" ? `${window.location.origin}/static/icon.svg` : ""

// Auth can come from layout props (Inertia passes page.props to layout) or usePage()
const layoutProps = defineProps({
  auth: { type: Object, default: () => ({ user: null }) },
})
const page = usePage()
const authUser = computed(() => layoutProps.auth?.user ?? page.props?.auth?.user ?? null)
const { theme, toggle: toggleTheme } = useTheme()
const { sidebarOpen, toggle: toggleSidebar } = useSidebar()

const searchOpen = ref(false)
const searchQuery = ref("")
const searchInputRef = ref(null)

function openSearch() {
  searchOpen.value = true
  searchQuery.value = ""
}
function closeSearch() {
  searchOpen.value = false
}

watch(searchOpen, (open) => {
  if (open) {
    searchQuery.value = ""
    nextTick(() => searchInputRef.value?.focus())
  }
})

function onSearchKeydown(e) {
  if (e.key === "Escape") closeSearch()
}

function handleGlobalKeydown(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === "k") {
    e.preventDefault()
    searchOpen.value = !searchOpen.value
    if (searchOpen.value) searchQuery.value = ""
  }
}

onMounted(() => {
  window.addEventListener("keydown", handleGlobalKeydown)
})
onUnmounted(() => {
  window.removeEventListener("keydown", handleGlobalKeydown)
})

const allNavItems = [
  { href: "/admin/", label: "Dashboard", icon: LayoutDashboard, section: "General" },
  { href: "/admin/users/", label: "Users", icon: Users, section: "General" },
  { href: "/admin/groups/", label: "Groups", icon: Shield, section: "General" },
  { href: "#", label: "Settings", icon: Settings, section: "Other" },
]

const filteredNavItems = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return allNavItems
  return allNavItems.filter(
    (item) =>
      item.label.toLowerCase().includes(q) || item.section.toLowerCase().includes(q)
  )
})

// Display name: "First Last" if set, else username, else email, else "User"
const displayName = computed(() => {
  const u = authUser.value
  if (!u) return "User"
  const first = u.first_name ?? ""
  const last = u.last_name ?? ""
  const full = [first, last].filter(Boolean).join(" ")
  if (full) return full
  if (u.username) return u.username
  if (u.email) return u.email
  return "User"
})

// Initials: from first+last, else username or email, else "U"
const userInitials = computed(() => {
  const u = authUser.value
  if (!u) return "U"
  const first = u.first_name ?? ""
  const last = u.last_name ?? ""
  if (first && last) return `${first[0]}${last[0]}`.toUpperCase()
  if (first) return first.slice(0, 2).toUpperCase()
  const name = u.username || u.email || ""
  if (name) return name.slice(0, 2).toUpperCase()
  return "U"
})

const userEmail = computed(() => authUser.value?.email || "No email")

const currentUrl = (() => {
  const u = page.url
  if (typeof u === "string") return u
  if (u != null && typeof u === "object" && typeof u.pathname === "string") return u.pathname
  return ""
})()

const generalNavItems = [
  { href: "/admin/", label: "Dashboard", icon: LayoutDashboard, match: (url) => url === "/admin/" },
  {
    href: "/admin/users/",
    label: "Users",
    icon: Users,
    match: (url) => typeof url === "string" && url.startsWith("/admin/users"),
  },
  {
    href: "/admin/groups/",
    label: "Groups",
    icon: Shield,
    match: (url) => typeof url === "string" && url.startsWith("/admin/groups"),
  },
]


function logout() {
  Inertia.post("/logout/")
}
</script>

<template>
  <div class="flex h-screen bg-background">
    <!-- Sidebar: expanded (w-64) or collapsed (w-16 icons only); state in localStorage -->
    <aside
      :class="[
        'flex flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground shrink-0 transition-[width] duration-200 overflow-hidden',
        sidebarOpen ? 'w-64' : 'w-16',
      ]"
    >
      <TooltipProvider :delay-duration="300">
        <!-- Branding -->
        <div
          :class="[
            'flex border-b border-sidebar-border shrink-0',
            sidebarOpen ? 'items-center gap-3 p-4' : 'justify-center py-4 px-0',
          ]"
        >
          <img v-if="iconUrl" :src="iconUrl" alt="" class="h-9 w-9 shrink-0 rounded-lg object-contain" />
          <div v-show="sidebarOpen" class="flex flex-col min-w-0">
            <span class="font-semibold text-sm truncate">Admin</span>
            <span class="text-xs text-muted-foreground truncate">Django + Inertia</span>
          </div>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 overflow-y-auto py-3">
          <div v-show="sidebarOpen" class="px-3 mb-2">
            <p class="text-xs font-medium text-muted-foreground uppercase tracking-wider">General</p>
          </div>
          <div :class="['space-y-0.5', sidebarOpen ? 'px-2' : 'px-2 flex flex-col items-center']">
            <template v-for="item in generalNavItems" :key="item.href">
              <Tooltip v-if="!sidebarOpen" :delay-duration="0">
                <TooltipTrigger as-child>
                  <Link
                    :href="item.href"
                    :class="
                      cn(
                        'flex items-center rounded-md text-sm font-medium transition-colors',
                        sidebarOpen ? 'gap-3 px-3 py-2 w-full' : 'justify-center p-2 w-10 h-10',
                        item.match(currentUrl)
                          ? 'bg-accent text-accent-foreground'
                          : 'text-sidebar-foreground hover:bg-accent/50 hover:text-accent-foreground'
                      )
                    "
                  >
                    <component :is="item.icon" class="h-4 w-4 shrink-0" />
                    <span v-show="sidebarOpen" class="truncate">{{ item.label }}</span>
                  </Link>
                </TooltipTrigger>
                <TooltipContent side="right" class="border-sidebar-border">
                  {{ item.label }}
                </TooltipContent>
              </Tooltip>
              <Link
                v-else
                :href="item.href"
                :class="
                  cn(
                    'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                    item.match(currentUrl)
                      ? 'bg-accent text-accent-foreground'
                      : 'text-sidebar-foreground hover:bg-accent/50 hover:text-accent-foreground'
                  )
                "
              >
                <component :is="item.icon" class="h-4 w-4 shrink-0" />
                {{ item.label }}
              </Link>
            </template>
          </div>
          <div v-show="sidebarOpen" class="px-3 mt-6 mb-2">
            <p class="text-xs font-medium text-muted-foreground uppercase tracking-wider">Other</p>
          </div>
          <div :class="['space-y-0.5', sidebarOpen ? 'px-2' : 'px-2 flex flex-col items-center']">
            <Tooltip v-if="!sidebarOpen">
              <TooltipTrigger as-child>
                <span
                  class="flex justify-center p-2 w-10 h-10 rounded-md text-muted-foreground cursor-not-allowed"
                >
                  <Settings class="h-4 w-4 shrink-0" />
                </span>
              </TooltipTrigger>
              <TooltipContent side="right" class="border-sidebar-border">Settings</TooltipContent>
            </Tooltip>
            <span
              v-else
              class="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground cursor-not-allowed"
            >
              <Settings class="h-4 w-4 shrink-0" />
              Settings
            </span>
          </div>
        </nav>

        <!-- User profile at bottom -->
        <div :class="['border-t border-sidebar-border shrink-0', sidebarOpen ? 'p-3' : 'p-2 flex justify-center']">
          <DropdownMenu>
            <Tooltip v-if="!sidebarOpen">
              <TooltipTrigger as-child>
                <DropdownMenuTrigger as-child>
                  <button
                    class="flex rounded-md hover:bg-accent/50 transition-colors outline-none focus-visible:ring-2 focus-visible:ring-ring p-2"
                  >
                    <Avatar class="h-8 w-8 shrink-0">
                      <AvatarFallback class="bg-primary/10 text-primary text-xs">
                        {{ userInitials }}
                      </AvatarFallback>
                    </Avatar>
                  </button>
                </DropdownMenuTrigger>
              </TooltipTrigger>
              <TooltipContent side="right" class="border-sidebar-border">
                {{ displayName }}
              </TooltipContent>
            </Tooltip>
            <DropdownMenuTrigger v-else as-child>
              <button
                class="flex items-center gap-3 w-full rounded-md px-3 py-2 text-sm hover:bg-accent/50 transition-colors outline-none focus-visible:ring-2 focus-visible:ring-ring"
              >
                <Avatar class="h-8 w-8 shrink-0">
                  <AvatarFallback class="bg-primary/10 text-primary text-xs">
                    {{ userInitials }}
                  </AvatarFallback>
                </Avatar>
                <div class="flex-1 text-left min-w-0">
                  <p class="font-medium truncate text-sidebar-foreground">{{ displayName }}</p>
                  <p class="text-xs text-muted-foreground truncate">{{ userEmail }}</p>
                </div>
                <ChevronDown class="h-4 w-4 shrink-0 opacity-50" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent side="top" align="start" class="w-56">
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem class="text-destructive cursor-pointer" @click="logout">
                <LogOut class="h-4 w-4 mr-2" />
                Log out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </TooltipProvider>
    </aside>

    <!-- Main area: header + content -->
    <div class="flex flex-1 flex-col min-w-0">
      <!-- Header -->
      <header class="flex h-14 shrink-0 items-center gap-4 border-b border-border bg-background px-4 sm:px-6">
        <Button
          variant="ghost"
          size="icon"
          class="h-9 w-9 shrink-0"
          :aria-label="sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'"
          @click="toggleSidebar"
        >
          <PanelLeftClose v-if="sidebarOpen" class="h-4 w-4" />
          <PanelLeft v-else class="h-4 w-4" />
        </Button>
        <div class="flex-1" />
        <div class="flex items-center gap-2">
          <!-- Search bar: click opens command palette -->
          <button
            type="button"
            class="relative hidden sm:flex items-center w-64 gap-2 rounded-md border border-input bg-muted/50 px-3 py-2 h-9 text-sm text-muted-foreground hover:bg-muted/80 hover:text-foreground transition-colors text-left"
            @click="openSearch"
          >
            <Search class="h-4 w-4 shrink-0" />
            <span class="flex-1 truncate">Search...</span>
            <kbd class="hidden sm:inline-flex h-5 select-none items-center gap-0.5 rounded border bg-background/80 px-1.5 font-mono text-[10px] font-medium">
              <span class="text-xs">⌘</span>K
            </kbd>
          </button>
          <!-- Theme toggle -->
          <Button
            variant="ghost"
            size="icon"
            class="h-9 w-9 shrink-0"
            @click="toggleTheme"
          >
            <Sun v-if="theme === 'light'" class="h-4 w-4" />
            <Moon v-else class="h-4 w-4" />
          </Button>
          <!-- User avatar (header) -->
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="ghost" size="icon" class="h-9 w-9 shrink-0 rounded-full">
                <Avatar class="h-8 w-8">
                  <AvatarFallback class="bg-primary/10 text-primary text-xs">
                    {{ userInitials }}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" class="w-56">
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem class="text-destructive cursor-pointer" @click="logout">
                <LogOut class="h-4 w-4 mr-2" />
                Log out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      <!-- Command palette: center modal with sidebar menus -->
      <Dialog :open="searchOpen" @update:open="(v) => (searchOpen = v)">
        <DialogContent
          class="max-w-lg gap-0 p-0 overflow-hidden"
          @keydown="onSearchKeydown"
          @pointer-down-outside="closeSearch"
        >
          <DialogTitle class="sr-only">Search and navigate</DialogTitle>
          <DialogDescription class="sr-only">
            Search or jump to a page. Sidebar menu options listed below.
          </DialogDescription>
          <div class="flex items-center border-b border-border px-3">
            <Search class="h-4 w-4 shrink-0 text-muted-foreground" />
            <input
              ref="searchInputRef"
              v-model="searchQuery"
              type="text"
              placeholder="Search or jump to..."
              class="flex-1 bg-transparent py-3 px-3 text-sm outline-none placeholder:text-muted-foreground"
              autofocus
            />
            <kbd class="hidden sm:inline-flex h-5 select-none items-center gap-0.5 rounded border bg-muted px-1.5 font-mono text-[10px] text-muted-foreground">Esc</kbd>
          </div>
          <div class="max-h-[min(60vh,400px)] overflow-y-auto py-2">
            <template v-for="(item, i) in filteredNavItems" :key="item.href + item.label">
              <Link
                v-if="item.href !== '#'"
                :href="item.href"
                class="flex items-center gap-3 px-3 py-2.5 text-sm hover:bg-accent hover:text-accent-foreground transition-colors"
                @click="closeSearch"
              >
                <component :is="item.icon" class="h-4 w-4 shrink-0 text-muted-foreground" />
                <span class="font-medium">{{ item.label }}</span>
                <span class="text-xs text-muted-foreground ml-auto">{{ item.section }}</span>
              </Link>
              <span
                v-else
                class="flex items-center gap-3 px-3 py-2.5 text-sm text-muted-foreground cursor-not-allowed"
              >
                <component :is="item.icon" class="h-4 w-4 shrink-0" />
                {{ item.label }}
                <span class="text-xs ml-auto">{{ item.section }}</span>
              </span>
            </template>
            <p v-if="filteredNavItems.length === 0" class="px-3 py-4 text-sm text-muted-foreground">
              No matches.
            </p>
          </div>
        </DialogContent>
      </Dialog>

      <!-- Page content -->
      <main class="flex-1 overflow-auto">
        <div class="p-6">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>
