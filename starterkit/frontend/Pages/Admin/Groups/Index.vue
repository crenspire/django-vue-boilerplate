<script setup>
import { computed, ref } from "vue"
import { Link, router, usePage } from "@inertiajs/vue3"
import { KeyRound, MoreHorizontal, Pencil, Plus, Shield, Trash2, Users } from "lucide-vue-next"
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
import { useListQuery } from "@/composables/useListQuery"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  groups: { type: Array, default: () => [] },
  pagination: { type: Object, required: true },
  filters: { type: Object, default: () => ({}) },
})

const page = usePage()
const can = computed(() => page.props.auth?.user?.permissions ?? {})
const { search, orderBy, doSearch, clearSearch, sort, pageUrl } = useListQuery("/admin/groups/", props, "name")

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
    <PageHeader title="Groups" description="Bundle permissions into roles and assign them to users.">
      <template #actions>
        <Button v-if="can.add_groups" as-child size="sm">
          <Link href="/admin/groups/create/">
            <Plus class="h-4 w-4" />
            Add group
          </Link>
        </Button>
      </template>
    </PageHeader>

    <div class="flex flex-col gap-4">
      <SearchBar v-model="search" placeholder="Search groups…" @search="doSearch" @clear="clearSearch" />

      <div class="overflow-hidden rounded-lg border">
        <Table>
          <TableHeader class="bg-muted/50">
            <TableRow class="hover:bg-transparent">
              <TableHead class="pl-4">
                <SortableHeader field="name" :current-order-by="orderBy" label="Name" @sort="sort" />
              </TableHead>
              <TableHead>
                <SortableHeader field="user_count" :current-order-by="orderBy" label="Members" @sort="sort" />
              </TableHead>
              <TableHead>
                <SortableHeader field="permission_count" :current-order-by="orderBy" label="Permissions" @sort="sort" />
              </TableHead>
              <TableHead class="w-12"><span class="sr-only">Actions</span></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-if="!groups.length" class="hover:bg-transparent">
              <TableCell colspan="4" class="h-48">
                <div class="flex flex-col items-center justify-center gap-2 text-center">
                  <div class="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                    <Shield class="h-5 w-5 text-muted-foreground" />
                  </div>
                  <p class="text-sm font-medium">No groups found</p>
                  <p class="text-sm text-muted-foreground">
                    {{ filters.search ? "Try a different search term." : "Groups let you grant the same permissions to many users." }}
                  </p>
                </div>
              </TableCell>
            </TableRow>
            <TableRow v-for="g in groups" :key="g.id">
              <TableCell class="pl-4">
                <div class="flex items-center gap-3">
                  <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border bg-muted/50">
                    <Shield class="h-4 w-4 text-muted-foreground" />
                  </div>
                  <Link v-if="can.change_groups" :href="`/admin/groups/${g.id}/edit/`" class="font-medium hover:underline">
                    {{ g.name }}
                  </Link>
                  <span v-else class="font-medium">{{ g.name }}</span>
                </div>
              </TableCell>
              <TableCell>
                <Badge variant="outline" class="gap-1 px-1.5 font-normal text-muted-foreground">
                  <Users class="h-3.5 w-3.5" />
                  {{ g.user_count }} {{ g.user_count === 1 ? "member" : "members" }}
                </Badge>
              </TableCell>
              <TableCell>
                <Badge variant="outline" class="gap-1 px-1.5 font-normal text-muted-foreground">
                  <KeyRound class="h-3.5 w-3.5" />
                  {{ g.permission_count }}
                </Badge>
              </TableCell>
              <TableCell class="pr-4 text-right">
                <DropdownMenu v-if="can.change_groups || can.delete_groups">
                  <DropdownMenuTrigger as-child>
                    <Button variant="ghost" size="icon" class="h-8 w-8 text-muted-foreground data-[state=open]:bg-muted" :aria-label="`Actions for ${g.name}`">
                      <MoreHorizontal class="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" class="w-36">
                    <DropdownMenuItem v-if="can.change_groups" @select="router.visit(`/admin/groups/${g.id}/edit/`)">
                      <Pencil />
                      Edit
                    </DropdownMenuItem>
                    <template v-if="can.delete_groups">
                      <DropdownMenuSeparator v-if="can.change_groups" />
                      <DropdownMenuItem class="text-destructive focus:text-destructive" @select="pendingDelete = g">
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
      :delete-url="pendingDelete ? `/admin/groups/${pendingDelete.id}/delete/` : null"
      title="Delete group?"
      :description="`Members of '${pendingDelete?.name ?? ''}' will lose the permissions it grants. This action cannot be undone.`"
    />
  </div>
</template>
