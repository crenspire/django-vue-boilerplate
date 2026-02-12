<script setup>
import { computed } from "vue"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const inputVariants = cva(
  "flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
  {
    variants: {
      size: {
        default: "h-9",
        sm: "h-8",
        lg: "h-10",
      },
    },
    defaultVariants: {
      size: "default",
    },
  },
)

const props = defineProps({
  defaultValue: {
    type: [String, Number],
    default: undefined,
  },
  modelValue: {
    type: [String, Number],
    default: undefined,
  },
  size: { type: String, default: "default" },
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
  <input
    v-bind="$attrs"
    v-model="modelValue"
    :default-value="defaultValue"
    :class="cn(inputVariants({ size: props.size }), props.class)"
  />
</template>
