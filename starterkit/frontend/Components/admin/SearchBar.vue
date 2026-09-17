<script setup>
import { Search, X } from "lucide-vue-next"
import { Input } from "@/Components/ui/input"

defineProps({
  modelValue: { type: String, default: "" },
  placeholder: { type: String, default: "Search..." },
})

const emit = defineEmits(["update:modelValue", "search", "clear"])

function onClear() {
  emit("update:modelValue", "")
  emit("clear")
}
</script>

<template>
  <form class="relative w-full sm:max-w-xs" role="search" @submit.prevent="emit('search')">
    <Search class="pointer-events-none absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
    <Input
      :model-value="modelValue"
      :placeholder="placeholder"
      class="h-9 pl-8 pr-8"
      type="search"
      @update:model-value="emit('update:modelValue', $event)"
    />
    <button
      v-if="modelValue"
      type="button"
      class="absolute right-2 top-1/2 flex h-5 w-5 -translate-y-1/2 items-center justify-center rounded-sm text-muted-foreground hover:text-foreground"
      aria-label="Clear search"
      @click="onClear"
    >
      <X class="h-3.5 w-3.5" />
    </button>
  </form>
</template>
