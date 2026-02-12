<script setup>
import { cn } from "@/lib/utils"
import { alertVariants } from "."
const props = defineProps({
  variant: { type: null, required: false },
  class: { type: null, required: false },
})
</script>
<template>
  <div role="alert" :class="cn(alertVariants({ variant }), props.class)">
    <slot />
  </div>
</template>
