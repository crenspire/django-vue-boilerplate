<script setup>
import { cn } from "@/lib/utils"
import iconUrl from "@/icon.svg"

const props = defineProps({
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})
</script>

<template>
  <div :class="cn('flex aspect-square size-8 shrink-0 items-center justify-center overflow-hidden rounded-lg bg-sidebar-primary text-sidebar-primary-foreground', props.class)">
    <img :src="iconUrl" alt="" class="size-full object-cover" />
  </div>
</template>
