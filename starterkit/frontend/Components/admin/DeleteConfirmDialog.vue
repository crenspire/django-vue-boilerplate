<script setup>
import { ref } from "vue"
import { Inertia } from "@inertiajs/inertia"
import { Button } from "@/Components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/Components/ui/dialog"

const props = defineProps({
  title: { type: String, default: "Are you sure?" },
  description: { type: String, default: "This action cannot be undone." },
  deleteUrl: { type: String, required: true },
})

const open = ref(false)
const processing = ref(false)

function confirmDelete() {
  processing.value = true
  Inertia.post(props.deleteUrl, {}, {
    onFinish: () => {
      processing.value = false
      open.value = false
    },
  })
}
</script>

<template>
  <Dialog v-model:open="open">
    <slot :open="() => (open = true)" />
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{{ title }}</DialogTitle>
        <DialogDescription>{{ description }}</DialogDescription>
      </DialogHeader>
      <DialogFooter>
        <Button variant="outline" @click="open = false">Cancel</Button>
        <Button variant="destructive" :disabled="processing" @click="confirmDelete">
          {{ processing ? "Deleting..." : "Delete" }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
