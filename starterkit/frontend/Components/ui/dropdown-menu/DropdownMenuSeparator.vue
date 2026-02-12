<script setup>
import { DropdownMenuSeparator } from "reka-ui"
import { cn } from "@/lib/utils"
const props = defineProps({ class: { type: null, required: false } })
</script>
<template>
  <DropdownMenuSeparator :class="cn('-mx-1 my-1 h-px bg-muted', props.class)" />
</template>
