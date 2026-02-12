<script setup>
import { computed } from "vue"
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Button } from "@/Components/ui/button"
import { Badge } from "@/Components/ui/badge"
import { Card, CardContent } from "@/Components/ui/card"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/Components/ui/table"
import { Alert, AlertDescription } from "@/Components/ui/alert"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/Components/ui/dropdown-menu"
import PageHeader from "@/Components/admin/PageHeader.vue"
import SearchBar from "@/Components/admin/SearchBar.vue"
import SortableHeader from "@/Components/admin/SortableHeader.vue"
import DataTablePagination from "@/Components/admin/DataTablePagination.vue"
import DeleteConfirmDialog from "@/Components/admin/DeleteConfirmDialog.vue"
import { Link, useForm } from "@inertiajs/inertia-vue3"
import { Inertia } from "@inertiajs/inertia"
import { Plus, MoreHorizontal, Pencil, Trash2, AlertCircle } from "lucide-vue-next"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  users: { type: Array, default: () => [] },
  pagination: { type: Object, required: true },
  filters: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) },
})

const searchForm = useForm({
  search: props.filters?.search ?? "",
})

const currentOrderBy = computed(() => props.filters?.order_by ?? "username")

function doSearch() {
  Inertia.get("/admin/users/", { search: searchForm.search, order_by: currentOrderBy.value }, { preserveState: true })
}

function clearSearch() {
  Inertia.get("/admin/users/", { order_by: currentOrderBy.value }, { preserveState: true })
}

function onSort(orderBy) {
  Inertia.get("/admin/users/", { search: props.filters?.search || "", order_by: orderBy }, { preserveState: true })
}

function buildPageUrl(page) {
  const params = new URLSearchParams()
  if (props.filters?.search) params.set("search", props.filters.search)
  if (currentOrderBy.value) params.set("order_by", currentOrderBy.value)
  params.set("page", page)
  return `/admin/users/?${params.toString()}`
}
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Users">
      <template #actions>
        <Link href="/admin/users/create/">
          <Button>
            <Plus class="h-4 w-4 mr-2" />
            Add user
          </Button>
        </Link>
      </template>
    </PageHeader>

    <Alert v-if="errors?.non_field_errors?.length" variant="destructive">
      <AlertCircle class="h-4 w-4" />
      <AlertDescription>
        <span v-for="(msg, i) in errors.non_field_errors" :key="i">{{ msg }}</span>
      </AlertDescription>
    </Alert>

    <Card>
      <CardContent class="pt-6">
        <div class="space-y-4">
          <SearchBar
            v-model="searchForm.search"
            placeholder="Search username or email..."
            @search="doSearch"
            @clear="clearSearch"
          />

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>
                  <SortableHeader field="username" :current-order-by="currentOrderBy" label="Username" @sort="onSort" />
                </TableHead>
                <TableHead>
                  <SortableHeader field="email" :current-order-by="currentOrderBy" label="Email" @sort="onSort" />
                </TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Role</TableHead>
                <TableHead class="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-if="!users.length">
                <TableCell colspan="5" class="text-center text-muted-foreground py-8">
                  No users found.
                </TableCell>
              </TableRow>
              <TableRow v-for="u in users" :key="u.id">
                <TableCell class="font-medium">
                  <Link :href="`/admin/users/${u.id}/edit/`" class="hover:underline">
                    {{ u.username }}
                  </Link>
                </TableCell>
                <TableCell class="text-muted-foreground">{{ u.email || "-" }}</TableCell>
                <TableCell>
                  <Badge v-if="u.is_active" variant="outline" class="border-green-200 bg-green-50 text-green-700">
                    Active
                  </Badge>
                  <Badge v-else variant="outline" class="border-red-200 bg-red-50 text-red-700">
                    Inactive
                  </Badge>
                </TableCell>
                <TableCell>
                  <div class="flex gap-1">
                    <Badge v-if="u.is_superuser" variant="default">superuser</Badge>
                    <Badge v-else-if="u.is_staff" variant="secondary">staff</Badge>
                  </div>
                </TableCell>
                <TableCell class="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger>
                      <Button variant="ghost" size="icon-sm">
                        <MoreHorizontal class="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem class="cursor-pointer" @click="Inertia.visit(`/admin/users/${u.id}/edit/`)">
                        <Pencil class="h-4 w-4 mr-2" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DeleteConfirmDialog
                        :delete-url="`/admin/users/${u.id}/delete/`"
                        title="Delete user"
                        :description="`Are you sure you want to delete '${u.username}'? This action cannot be undone.`"
                      >
                        <template #default="{ open }">
                          <DropdownMenuItem class="text-destructive cursor-pointer" @click="open">
                            <Trash2 class="h-4 w-4 mr-2" />
                            Delete
                          </DropdownMenuItem>
                        </template>
                      </DeleteConfirmDialog>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>

          <DataTablePagination :pagination="pagination" :build-url="buildPageUrl" />
        </div>
      </CardContent>
    </Card>
  </div>
</template>
