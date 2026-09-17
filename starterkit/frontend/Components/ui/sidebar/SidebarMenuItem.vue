<script setup>
import { cn } from "@/lib/utils"

const props = defineProps({
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})
</script>

<template>
  <li data-sidebar="menu-item" :class="cn('group/menu-item relative', props.class)">
    <slot />
  </li>
</template>
