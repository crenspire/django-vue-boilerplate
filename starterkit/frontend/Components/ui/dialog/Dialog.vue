<script setup>
import { DialogRoot } from "reka-ui"
const props = defineProps({ open: { type: Boolean, required: false } })
const emit = defineEmits(["update:open"])
</script>
<template>
  <DialogRoot :open="open" @update:open="emit('update:open', $event)">
    <slot />
  </DialogRoot>
</template>
