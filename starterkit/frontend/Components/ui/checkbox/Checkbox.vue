<script setup>
import { CheckboxRoot, CheckboxIndicator } from "reka-ui"
import { Check } from "lucide-vue-next"
import { cn } from "@/lib/utils"

const props = defineProps({
  checked: { type: [Boolean, String], required: false },
  defaultChecked: { type: Boolean, required: false },
  disabled: { type: Boolean, required: false },
  class: { type: null, required: false },
  id: { type: String, required: false },
})

const emit = defineEmits(["update:checked"])
</script>

<template>
  <CheckboxRoot
    :id="id"
    :checked="checked"
    :default-checked="defaultChecked"
    :disabled="disabled"
    :class="cn('peer size-4 min-h-0 min-w-0 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground', props.class)"
    @update:checked="emit('update:checked', $event)"
  >
    <CheckboxIndicator class="flex items-center justify-center text-current">
      <Check class="h-4 w-4" />
    </CheckboxIndicator>
  </CheckboxRoot>
</template>
