<script setup>
import { computed } from "vue"
import { router } from "@inertiajs/vue3"
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-vue-next"
import { Button } from "@/Components/ui/button"
import { Label } from "@/Components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/Components/ui/select"

const props = defineProps({
  pagination: { type: Object, required: true },
  buildUrl: { type: Function, required: true },
  pageSizes: { type: Array, default: () => [10, 25, 50, 100] },
})

const first = computed(() => (props.pagination.total ? (props.pagination.page - 1) * props.pagination.page_size + 1 : 0))
const last = computed(() => Math.min(props.pagination.page * props.pagination.page_size, props.pagination.total))
const totalPages = computed(() => Math.max(props.pagination.total_pages, 1))

function go(page, extra = {}) {
  router.visit(props.buildUrl(page, extra), { preserveScroll: true, preserveState: true })
}
</script>

<template>
  <div class="flex flex-col-reverse items-center justify-between gap-3 px-1 sm:flex-row">
    <p class="text-sm text-muted-foreground">
      <template v-if="pagination.total">
        Showing <span class="font-medium text-foreground">{{ first }}–{{ last }}</span> of
        <span class="font-medium text-foreground">{{ pagination.total }}</span>
      </template>
      <template v-else>No results</template>
    </p>
    <div class="flex items-center gap-6 lg:gap-8">
      <div class="hidden items-center gap-2 sm:flex">
        <Label for="rows-per-page" class="text-sm font-medium">Rows per page</Label>
        <Select :model-value="String(pagination.page_size)" @update:model-value="(size) => go(1, { page_size: Number(size) })">
          <SelectTrigger id="rows-per-page" class="h-8 w-[70px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent side="top">
            <SelectItem v-for="size in pageSizes" :key="size" :value="String(size)">{{ size }}</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div class="text-sm font-medium">Page {{ pagination.page }} of {{ totalPages }}</div>
      <div class="flex items-center gap-2">
        <Button variant="outline" size="icon" class="hidden h-8 w-8 lg:flex" :disabled="pagination.page <= 1" @click="go(1)">
          <span class="sr-only">First page</span>
          <ChevronsLeft class="h-4 w-4" />
        </Button>
        <Button variant="outline" size="icon" class="h-8 w-8" :disabled="pagination.page <= 1" @click="go(pagination.page - 1)">
          <span class="sr-only">Previous page</span>
          <ChevronLeft class="h-4 w-4" />
        </Button>
        <Button variant="outline" size="icon" class="h-8 w-8" :disabled="pagination.page >= totalPages" @click="go(pagination.page + 1)">
          <span class="sr-only">Next page</span>
          <ChevronRight class="h-4 w-4" />
        </Button>
        <Button variant="outline" size="icon" class="hidden h-8 w-8 lg:flex" :disabled="pagination.page >= totalPages" @click="go(totalPages)">
          <span class="sr-only">Last page</span>
          <ChevronsRight class="h-4 w-4" />
        </Button>
      </div>
    </div>
  </div>
</template>
