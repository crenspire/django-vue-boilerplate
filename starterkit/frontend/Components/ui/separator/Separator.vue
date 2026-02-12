<script setup>
import { Separator as SeparatorPrimitive } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps({
  orientation: {
    type: String,
    default: "horizontal",
  },
  decorative: {
    type: Boolean,
    default: true,
  },
  class: {
    type: [String, Array, Object],
    default: "",
  },
})
</script>

<template>
  <SeparatorPrimitive
    :orientation="props.orientation"
    :decorative="props.decorative"
    :class="
      cn(
        'shrink-0 bg-border',
        props.orientation === 'horizontal' ? 'h-[1px] w-full' : 'h-full w-[1px]',
        props.class,
      )
    "
  />
</template>
