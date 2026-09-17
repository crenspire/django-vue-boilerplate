<script setup>
import { ref } from "vue"
import { router } from "@inertiajs/vue3"
import { Loader2, TriangleAlert } from "lucide-vue-next"
import { Button } from "@/Components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/Components/ui/dialog"

// Controlled with v-model:open. Render it outside dropdown menus: menu content
// unmounts when the menu closes, which would take an embedded dialog with it.
const open = defineModel("open", { type: Boolean, default: false })

const props = defineProps({
  title: { type: String, default: "Are you sure?" },
  description: { type: String, default: "This action cannot be undone." },
  deleteUrl: { type: String, default: null },
})

const processing = ref(false)

function confirmDelete() {
  if (!props.deleteUrl) return
  router.post(props.deleteUrl, {}, {
    onStart: () => (processing.value = true),
    onFinish: () => {
      processing.value = false
      open.value = false
    },
  })
}
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="sm:max-w-md">
      <DialogHeader class="gap-2 sm:flex-row sm:items-start sm:gap-4 sm:space-y-0">
        <div class="mx-auto flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-destructive/10 sm:mx-0">
          <TriangleAlert class="h-5 w-5 text-destructive" />
        </div>
        <div class="space-y-1.5 text-center sm:text-left">
          <DialogTitle>{{ title }}</DialogTitle>
          <DialogDescription>{{ description }}</DialogDescription>
        </div>
      </DialogHeader>
      <DialogFooter class="gap-2 sm:gap-0">
        <Button variant="outline" @click="open = false">Cancel</Button>
        <Button variant="destructive" :disabled="processing" @click="confirmDelete">
          <Loader2 v-if="processing" class="h-4 w-4 animate-spin" />
          {{ processing ? "Deleting…" : "Delete" }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
