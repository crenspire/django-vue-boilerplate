<script setup>
import { DropdownMenuItem } from "reka-ui"
import { cn } from "@/lib/utils"
const props = defineProps({
  class: { type: null, required: false },
  disabled: { type: Boolean, required: false },
})
</script>
<template>
  <DropdownMenuItem
    :disabled="disabled"
    :class="cn('relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50', props.class)"
  >
    <slot />
  </DropdownMenuItem>
</template>
