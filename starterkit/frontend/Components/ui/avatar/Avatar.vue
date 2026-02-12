<script setup>
import { cn } from "@/lib/utils"
const props = defineProps({ class: { type: null, required: false } })
</script>
<template>
  <span :class="cn('relative flex h-9 w-9 shrink-0 overflow-hidden rounded-full', props.class)">
    <slot />
  </span>
</template>
