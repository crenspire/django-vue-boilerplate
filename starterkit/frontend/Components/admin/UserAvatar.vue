<script setup>
import { computed } from "vue"
import { Avatar, AvatarFallback } from "@/Components/ui/avatar"
import { cn } from "@/lib/utils"
import { initials } from "@/lib/format"

const props = defineProps({
  user: { type: Object, default: null },
  class: { type: [Boolean, null, String, Object, Array], required: false, skipCheck: true },
})

const letters = computed(() => initials(props.user))
</script>

<template>
  <Avatar :class="cn('h-8 w-8 rounded-lg', props.class)">
    <AvatarFallback class="rounded-lg bg-muted text-xs font-medium text-muted-foreground">
      {{ letters }}
    </AvatarFallback>
  </Avatar>
</template>
