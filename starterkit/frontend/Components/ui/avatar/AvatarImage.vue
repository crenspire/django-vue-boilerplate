<script setup>
import { cn } from "@/lib/utils"
const props = defineProps({
  src: { type: String, required: false },
  alt: { type: String, required: false },
  class: { type: null, required: false },
})
</script>
<template>
  <img v-if="src" :src="src" :alt="alt" :class="cn('aspect-square h-full w-full', props.class)" />
</template>
