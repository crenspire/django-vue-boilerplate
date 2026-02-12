<script setup>
import { SelectRoot } from "reka-ui"
const props = defineProps({
  modelValue: { type: String, required: false },
  defaultValue: { type: String, required: false },
})
const emit = defineEmits(["update:modelValue"])
</script>
<template>
  <SelectRoot :model-value="modelValue" :default-value="defaultValue" @update:model-value="emit('update:modelValue', $event)">
    <slot />
  </SelectRoot>
</template>
