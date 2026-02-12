<script setup>
import { Link } from "@inertiajs/inertia-vue3"

defineProps({
  title: { type: String, required: true },
  breadcrumbs: { type: Array, default: () => [] },
})
</script>

<template>
  <div class="flex items-center justify-between">
    <div>
      <nav v-if="breadcrumbs.length" class="flex items-center gap-1.5 text-sm text-muted-foreground mb-1">
        <template v-for="(crumb, i) in breadcrumbs" :key="i">
          <Link :href="crumb.href" class="hover:text-foreground transition-colors">{{ crumb.label }}</Link>
          <span>/</span>
        </template>
        <span class="text-foreground">{{ title }}</span>
      </nav>
      <h1 class="text-2xl font-semibold tracking-tight">{{ title }}</h1>
    </div>
    <div class="flex items-center gap-2">
      <slot name="actions" />
    </div>
  </div>
</template>
