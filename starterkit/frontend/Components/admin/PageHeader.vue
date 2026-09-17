<script setup>
import { Head } from "@inertiajs/vue3"

defineProps({
  title: { type: String, required: true },
  description: { type: String, default: "" },
})
</script>

<template>
  <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
    <Head :title="title" />
    <div class="min-w-0 space-y-1">
      <h1 class="truncate text-2xl font-semibold tracking-tight">{{ title }}</h1>
      <p v-if="description" class="text-sm text-muted-foreground">{{ description }}</p>
    </div>
    <div v-if="$slots.actions" class="flex shrink-0 items-center gap-2">
      <slot name="actions" />
    </div>
  </div>
</template>
