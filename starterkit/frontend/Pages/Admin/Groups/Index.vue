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
  groups: { type: Array, default: () => [] },
  pagination: { type: Object, required: true },
  filters: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) },
})

const searchForm = useForm({
  search: props.filters?.search ?? "",
})

const currentOrderBy = computed(() => props.filters?.order_by ?? "name")

function doSearch() {
  Inertia.get("/admin/groups/", { search: searchForm.search, order_by: currentOrderBy.value }, { preserveState: true })
}

function clearSearch() {
  Inertia.get("/admin/groups/", { order_by: currentOrderBy.value }, { preserveState: true })
}

function onSort(orderBy) {
  Inertia.get("/admin/groups/", { search: props.filters?.search || "", order_by: orderBy }, { preserveState: true })
}

function buildPageUrl(page) {
  const params = new URLSearchParams()
  if (props.filters?.search) params.set("search", props.filters.search)
  if (currentOrderBy.value) params.set("order_by", currentOrderBy.value)
  params.set("page", page)
  return `/admin/groups/?${params.toString()}`
}
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Groups">
      <template #actions>
        <Link href="/admin/groups/create/">
          <Button>
            <Plus class="h-4 w-4 mr-2" />
            Add group
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
            placeholder="Search group name..."
            @search="doSearch"
            @clear="clearSearch"
          />

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>
                  <SortableHeader field="name" :current-order-by="currentOrderBy" label="Name" @sort="onSort" />
                </TableHead>
                <TableHead>Users</TableHead>
                <TableHead>Permissions</TableHead>
                <TableHead class="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-if="!groups.length">
                <TableCell colspan="4" class="text-center text-muted-foreground py-8">
                  No groups found.
                </TableCell>
              </TableRow>
              <TableRow v-for="g in groups" :key="g.id">
                <TableCell class="font-medium">
                  <Link :href="`/admin/groups/${g.id}/edit/`" class="hover:underline">
                    {{ g.name }}
                  </Link>
                </TableCell>
                <TableCell>
                  <Badge variant="secondary">{{ g.user_count }}</Badge>
                </TableCell>
                <TableCell>
                  <Badge variant="outline">{{ g.permission_count }}</Badge>
                </TableCell>
                <TableCell class="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger>
                      <Button variant="ghost" size="icon-sm">
                        <MoreHorizontal class="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem class="cursor-pointer" @click="Inertia.visit(`/admin/groups/${g.id}/edit/`)">
                        <Pencil class="h-4 w-4 mr-2" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DeleteConfirmDialog
                        :delete-url="`/admin/groups/${g.id}/delete/`"
                        title="Delete group"
                        :description="`Are you sure you want to delete '${g.name}'? This action cannot be undone.`"
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
