<script setup>
import { cn } from "@/lib/utils"

const props = defineProps({
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})
</script>

<template>
  <ul data-sidebar="menu-sub" :class="cn('mx-3.5 flex min-w-0 translate-x-px flex-col gap-1 border-l border-sidebar-border px-2.5 py-0.5 group-data-[collapsible=icon]:hidden', props.class)">
    <slot />
  </ul>
</template>
