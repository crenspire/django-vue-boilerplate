<script setup>
import { watch } from "vue"
import { usePage } from "@inertiajs/vue3"
import { toast } from "vue-sonner"
import { Toaster } from "@/Components/ui/sonner"
import { useTheme } from "@/composables/useTheme"
import "vue-sonner/style.css"

// Django `messages` arrive as page.flash.messages (inertia-django 2.x) and are shown as toasts.
const page = usePage()
const { resolvedTheme } = useTheme()

const show = {
  success: toast.success,
  error: toast.error,
  warning: toast.warning,
  info: toast.info,
}

watch(
  () => page.flash?.messages,
  (messages) => {
    for (const { level, message } of messages ?? []) {
      ;(show[level] ?? toast)(message)
    }
  },
  { immediate: true },
)
</script>

<template>
  <Toaster :theme="resolvedTheme" position="bottom-right" close-button />
</template>
