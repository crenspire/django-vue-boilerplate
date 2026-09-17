<script setup>
import { Checkbox } from "@/Components/ui/checkbox"
import { cn } from "@/lib/utils"

const model = defineModel({ type: Boolean, default: false })

const props = defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  description: { type: String, default: "" },
  disabled: { type: Boolean, default: false },
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})
</script>

<template>
  <label
    :for="id"
    :class="cn(
      'flex items-start gap-3 rounded-lg border p-3 transition-colors',
      disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer hover:bg-accent/50',
      model && !disabled && 'border-primary/40 bg-accent/40',
      props.class,
    )"
  >
    <Checkbox :id="id" v-model="model" :disabled="disabled" class="mt-0.5" />
    <div class="grid gap-1 leading-none">
      <span class="text-sm font-medium">{{ label }}</span>
      <span v-if="description" class="text-xs text-muted-foreground">{{ description }}</span>
    </div>
  </label>
</template>
