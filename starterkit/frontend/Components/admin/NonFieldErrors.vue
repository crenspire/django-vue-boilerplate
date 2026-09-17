<script setup>
import { Alert, AlertDescription } from "@/Components/ui/alert"
import { AlertCircle } from "lucide-vue-next"

defineProps({
  errors: { type: Object, default: () => ({}) },
})
</script>

<template>
  <Alert v-if="errors?.non_field_errors?.length" variant="destructive">
    <AlertCircle class="h-4 w-4" />
    <AlertDescription>
      <p v-for="(msg, i) in errors.non_field_errors" :key="i">{{ msg }}</p>
    </AlertDescription>
  </Alert>
</template>
