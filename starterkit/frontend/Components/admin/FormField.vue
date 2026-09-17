<script setup>
import { Label } from "@/Components/ui/label"

defineProps({
  label: { type: String, required: true },
  error: { type: String, default: null },
  htmlFor: { type: String, default: null },
  required: { type: Boolean, default: false },
  hint: { type: String, default: "" },
})
</script>

<template>
  <div class="grid gap-2">
    <Label :for="htmlFor" :class="error ? 'text-destructive' : ''">
      {{ label }}<span v-if="required" class="ml-0.5 text-destructive">*</span>
    </Label>
    <slot />
    <p v-if="error" class="text-sm text-destructive">{{ error }}</p>
    <p v-else-if="hint" class="text-xs text-muted-foreground">{{ hint }}</p>
  </div>
</template>
