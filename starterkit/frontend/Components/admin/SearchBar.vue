<script setup>
import { Input } from "@/Components/ui/input"
import { Button } from "@/Components/ui/button"
import { Search, X } from "lucide-vue-next"

const props = defineProps({
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
  <form @submit.prevent="emit('search')" class="flex items-center gap-2">
    <div class="relative flex-1 max-w-sm">
      <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        :model-value="modelValue"
        @update:model-value="emit('update:modelValue', $event)"
        :placeholder="placeholder"
        class="pl-9 pr-9"
      />
      <button
        v-if="modelValue"
        type="button"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
        @click="onClear"
      >
        <X class="h-4 w-4" />
      </button>
    </div>
    <Button type="submit" variant="secondary" size="sm">Search</Button>
  </form>
</template>
