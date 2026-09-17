<script setup>
import { Link } from "@inertiajs/vue3"
import { ArrowLeft } from "lucide-vue-next"
import { Button } from "@/Components/ui/button"
import FlashToaster from "@/Components/admin/FlashToaster.vue"
import ThemeToggle from "@/Components/admin/ThemeToggle.vue"
</script>

<template>
  <div class="relative flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
    <div class="absolute inset-x-0 top-0 flex items-center justify-between p-4 md:p-6">
      <Button as-child variant="ghost" size="sm" class="text-muted-foreground">
        <Link href="/">
          <ArrowLeft class="h-4 w-4" />
          Back to site
        </Link>
      </Button>
      <ThemeToggle />
    </div>
    <div class="w-full max-w-sm md:max-w-4xl">
      <slot />
    </div>
    <FlashToaster />
  </div>
</template>
