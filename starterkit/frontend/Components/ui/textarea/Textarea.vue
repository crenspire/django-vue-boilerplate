<script setup>
import { computed } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps({
  defaultValue: {
    type: [String, Number],
    default: undefined,
  },
  modelValue: {
    type: [String, Number],
    default: undefined,
  },
  class: {
    type: [String, Array, Object],
    default: "",
  },
})

const emits = defineEmits(["update:modelValue"])

const modelValue = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emits("update:modelValue", value)
  },
})
</script>

<template>
  <textarea
    v-bind="$attrs"
    v-model="modelValue"
    :default-value="defaultValue"
    :class="
      cn(
        'flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        props.class,
      )
    "
  />
</template>
