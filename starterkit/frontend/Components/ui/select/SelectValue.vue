<script setup>
import { SelectValue } from "reka-ui"
const props = defineProps({ placeholder: { type: String, required: false } })
</script>
<template>
  <SelectValue :placeholder="placeholder">
    <slot />
  </SelectValue>
</template>
