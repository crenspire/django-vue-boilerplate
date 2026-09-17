<script setup>
import { cn } from "@/lib/utils"
import { Separator } from "@/Components/ui/separator"

const props = defineProps({
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})
</script>

<template>
  <Separator data-sidebar="separator" :class="cn('mx-2 w-auto bg-sidebar-border', props.class)">
    <slot />
  </Separator>
</template>
