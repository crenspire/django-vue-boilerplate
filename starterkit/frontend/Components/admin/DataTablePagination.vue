<script setup>
import { Link } from "@inertiajs/inertia-vue3"
import { Button } from "@/Components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-vue-next"

defineProps({
  pagination: { type: Object, required: true },
  buildUrl: { type: Function, required: true },
})
</script>

<template>
  <div v-if="pagination.total_pages > 1" class="flex items-center justify-between px-2">
    <p class="text-sm text-muted-foreground">
      Page {{ pagination.page }} of {{ pagination.total_pages }}
    </p>
    <div class="flex items-center gap-2">
      <Link
        v-if="pagination.page > 1"
        :href="buildUrl(pagination.page - 1)"
      >
        <Button variant="outline" size="sm">
          <ChevronLeft class="h-4 w-4 mr-1" />
          Previous
        </Button>
      </Link>
      <Button v-else variant="outline" size="sm" disabled>
        <ChevronLeft class="h-4 w-4 mr-1" />
        Previous
      </Button>
      <Link
        v-if="pagination.page < pagination.total_pages"
        :href="buildUrl(pagination.page + 1)"
      >
        <Button variant="outline" size="sm">
          Next
          <ChevronRight class="h-4 w-4 ml-1" />
        </Button>
      </Link>
      <Button v-else variant="outline" size="sm" disabled>
        Next
        <ChevronRight class="h-4 w-4 ml-1" />
      </Button>
    </div>
  </div>
</template>
