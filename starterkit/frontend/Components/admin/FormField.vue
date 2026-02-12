<script setup>
import { Label } from "@/Components/ui/label"

defineProps({
  label: { type: String, required: true },
  error: { type: String, default: null },
  htmlFor: { type: String, default: null },
  required: { type: Boolean, default: false },
})
</script>

<template>
  <div class="space-y-2">
    <Label :for="htmlFor">
      {{ label }}<span v-if="required" class="text-destructive ml-1">*</span>
    </Label>
    <slot />
    <p v-if="error" class="text-sm text-destructive">{{ error }}</p>
  </div>
</template>
