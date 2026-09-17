<script setup>
import { computed, ref } from "vue"
import { Link, router, usePage } from "@inertiajs/vue3"
import { CircleCheck, CircleDashed, MoreHorizontal, Pencil, Plus, ShieldCheck, Trash2, UserRound, Users } from "lucide-vue-next"
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Badge } from "@/Components/ui/badge"
import { Button } from "@/Components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/Components/ui/dropdown-menu"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/Components/ui/table"
import DataTablePagination from "@/Components/admin/DataTablePagination.vue"
import DeleteConfirmDialog from "@/Components/admin/DeleteConfirmDialog.vue"
import PageHeader from "@/Components/admin/PageHeader.vue"
import SearchBar from "@/Components/admin/SearchBar.vue"
import SortableHeader from "@/Components/admin/SortableHeader.vue"
import UserAvatar from "@/Components/admin/UserAvatar.vue"
import { useListQuery } from "@/composables/useListQuery"
import { displayName, formatDate, timeAgo } from "@/lib/format"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  users: { type: Array, default: () => [] },
  pagination: { type: Object, required: true },
  filters: { type: Object, default: () => ({}) },
})

const page = usePage()
const can = computed(() => page.props.auth?.user?.permissions ?? {})
const { search, orderBy, doSearch, clearSearch, sort, pageUrl } = useListQuery("/admin/users/", props, "username")

// A single dialog outside the dropdown menus (menu content unmounts on close).
const pendingDelete = ref(null)
const confirmOpen = computed({
  get: () => pendingDelete.value !== null,
  set: (open) => {
    if (!open) pendingDelete.value = null
  },
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageHeader title="Users" description="Manage accounts, their status and group membership.">
      <template #actions>
        <Button v-if="can.add_users" as-child size="sm">
          <Link href="/admin/users/create/">
            <Plus class="h-4 w-4" />
            Add user
          </Link>
        </Button>
      </template>
    </PageHeader>

    <div class="flex flex-col gap-4">
      <div class="flex items-center justify-between gap-2">
        <SearchBar v-model="search" placeholder="Search name, username or email…" @search="doSearch" @clear="clearSearch" />
      </div>

      <div class="overflow-hidden rounded-lg border">
        <Table>
          <TableHeader class="bg-muted/50">
            <TableRow class="hover:bg-transparent">
              <TableHead class="pl-4">
                <SortableHeader field="username" :current-order-by="orderBy" label="User" @sort="sort" />
              </TableHead>
              <TableHead>
                <SortableHeader field="is_active" :current-order-by="orderBy" label="Status" @sort="sort" />
              </TableHead>
              <TableHead class="hidden md:table-cell">Role</TableHead>
              <TableHead class="hidden lg:table-cell">
                <SortableHeader field="date_joined" :current-order-by="orderBy" label="Joined" @sort="sort" />
              </TableHead>
              <TableHead class="hidden lg:table-cell">
                <SortableHeader field="last_login" :current-order-by="orderBy" label="Last login" @sort="sort" />
              </TableHead>
              <TableHead class="w-12"><span class="sr-only">Actions</span></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-if="!users.length" class="hover:bg-transparent">
              <TableCell colspan="6" class="h-48">
                <div class="flex flex-col items-center justify-center gap-2 text-center">
                  <div class="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                    <Users class="h-5 w-5 text-muted-foreground" />
                  </div>
                  <p class="text-sm font-medium">No users found</p>
                  <p class="text-sm text-muted-foreground">
                    {{ filters.search ? "Try a different search term." : "Create the first user to get started." }}
                  </p>
                </div>
              </TableCell>
            </TableRow>
            <TableRow v-for="u in users" :key="u.id">
              <TableCell class="pl-4">
                <div class="flex items-center gap-3">
                  <UserAvatar :user="u" class="h-9 w-9" />
                  <div class="grid min-w-0 leading-tight">
                    <Link v-if="u.can_edit" :href="`/admin/users/${u.id}/edit/`" class="truncate font-medium hover:underline">
                      {{ displayName(u) }}
                    </Link>
                    <span v-else class="truncate font-medium">{{ displayName(u) }}</span>
                    <span class="truncate text-xs text-muted-foreground">
                      {{ u.full_name ? `@${u.username}` : "" }}{{ u.full_name && u.email ? " · " : "" }}{{ u.email }}
                    </span>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <Badge variant="outline" class="gap-1 px-1.5 font-normal text-muted-foreground">
                  <CircleCheck v-if="u.is_active" class="h-3.5 w-3.5 fill-success text-background" />
                  <CircleDashed v-else class="h-3.5 w-3.5" />
                  {{ u.is_active ? "Active" : "Inactive" }}
                </Badge>
              </TableCell>
              <TableCell class="hidden md:table-cell">
                <span class="inline-flex items-center gap-1.5 text-sm">
                  <ShieldCheck v-if="u.is_superuser" class="h-4 w-4 text-muted-foreground" />
                  <UserRound v-else class="h-4 w-4 text-muted-foreground" />
                  {{ u.is_superuser ? "Superuser" : u.is_staff ? "Staff" : "Member" }}
                </span>
              </TableCell>
              <TableCell class="hidden text-muted-foreground lg:table-cell" :title="formatDate(u.date_joined)">
                {{ formatDate(u.date_joined) }}
              </TableCell>
              <TableCell class="hidden text-muted-foreground lg:table-cell">
                {{ timeAgo(u.last_login) }}
              </TableCell>
              <TableCell class="pr-4 text-right">
                <DropdownMenu v-if="u.can_edit || u.can_delete">
                  <DropdownMenuTrigger as-child>
                    <Button variant="ghost" size="icon" class="h-8 w-8 text-muted-foreground data-[state=open]:bg-muted" :aria-label="`Actions for ${u.username}`">
                      <MoreHorizontal class="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" class="w-36">
                    <DropdownMenuItem v-if="u.can_edit" @select="router.visit(`/admin/users/${u.id}/edit/`)">
                      <Pencil />
                      Edit
                    </DropdownMenuItem>
                    <template v-if="u.can_delete">
                      <DropdownMenuSeparator v-if="u.can_edit" />
                      <DropdownMenuItem class="text-destructive focus:text-destructive" @select="pendingDelete = u">
                        <Trash2 />
                        Delete
                      </DropdownMenuItem>
                    </template>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <DataTablePagination :pagination="pagination" :build-url="pageUrl" />
    </div>

    <DeleteConfirmDialog
      v-model:open="confirmOpen"
      :delete-url="pendingDelete ? `/admin/users/${pendingDelete.id}/delete/` : null"
      title="Delete user?"
      :description="`This permanently deletes '${pendingDelete?.username ?? ''}' and removes them from all groups. This action cannot be undone.`"
    />
  </div>
</template>
