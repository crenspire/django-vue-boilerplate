<script setup>
import { cn } from "@/lib/utils"

const props = defineProps({
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})
</script>

<template>
  <div data-sidebar="group" :class="cn('relative flex w-full min-w-0 flex-col p-2', props.class)">
    <slot />
  </div>
</template>
