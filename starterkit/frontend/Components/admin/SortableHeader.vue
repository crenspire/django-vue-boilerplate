<script setup>
import { computed } from "vue"
import { ArrowUp, ArrowDown, ArrowUpDown } from "lucide-vue-next"

const props = defineProps({
  field: { type: String, required: true },
  currentOrderBy: { type: String, default: "" },
  label: { type: String, required: true },
})

const emit = defineEmits(["sort"])

const sortDirection = computed(() => {
  if (props.currentOrderBy === props.field) return "asc"
  if (props.currentOrderBy === `-${props.field}`) return "desc"
  return null
})

function toggleSort() {
  if (sortDirection.value === "asc") {
    emit("sort", `-${props.field}`)
  } else {
    emit("sort", props.field)
  }
}
</script>

<template>
  <button
    type="button"
    class="inline-flex items-center gap-1 hover:text-foreground transition-colors"
    @click="toggleSort"
  >
    {{ label }}
    <ArrowUp v-if="sortDirection === 'asc'" class="h-4 w-4" />
    <ArrowDown v-else-if="sortDirection === 'desc'" class="h-4 w-4" />
    <ArrowUpDown v-else class="h-4 w-4 opacity-50" />
  </button>
</template>
