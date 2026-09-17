<script setup>
import { computed } from "vue"
import { ArrowDown, ArrowUp, ChevronsUpDown } from "lucide-vue-next"
import { Button } from "@/Components/ui/button"
import { cn } from "@/lib/utils"

const props = defineProps({
  field: { type: String, required: true },
  currentOrderBy: { type: String, default: "" },
  label: { type: String, required: true },
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})

const emit = defineEmits(["sort"])

const direction = computed(() => {
  if (props.currentOrderBy === props.field) return "asc"
  if (props.currentOrderBy === `-${props.field}`) return "desc"
  return null
})

function toggle() {
  emit("sort", direction.value === "asc" ? `-${props.field}` : props.field)
}
</script>

<template>
  <Button
    variant="ghost"
    size="sm"
    :class="cn('-ml-3 h-8 font-medium data-[active=true]:text-foreground', props.class)"
    :data-active="direction !== null"
    :aria-sort="direction === 'asc' ? 'ascending' : direction === 'desc' ? 'descending' : 'none'"
    @click="toggle"
  >
    {{ label }}
    <ArrowUp v-if="direction === 'asc'" class="h-3.5 w-3.5" />
    <ArrowDown v-else-if="direction === 'desc'" class="h-3.5 w-3.5" />
    <ChevronsUpDown v-else class="h-3.5 w-3.5 opacity-50" />
  </Button>
</template>
