<script setup>
import { computed, ref } from "vue"
import { usePage } from "@inertiajs/vue3"
import { Trash2 } from "lucide-vue-next"
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Button } from "@/Components/ui/button"
import DeleteConfirmDialog from "@/Components/admin/DeleteConfirmDialog.vue"
import GroupForm from "@/Components/admin/GroupForm.vue"
import PageHeader from "@/Components/admin/PageHeader.vue"

defineOptions({ layout: AdminLayout })

defineProps({
  group: { type: Object, required: true },
  form: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  permissions_choices: { type: Array, default: () => [] },
})

const page = usePage()
const canDelete = computed(() => page.props.auth?.user?.permissions?.delete_groups)
const confirmOpen = ref(false)
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageHeader :title="group.name" description="Edit the group name and the permissions it grants.">
      <template #actions>
        <Button v-if="canDelete" variant="outline" size="sm" class="text-destructive hover:bg-destructive/10 hover:text-destructive" @click="confirmOpen = true">
          <Trash2 class="h-4 w-4" />
          Delete group
        </Button>
      </template>
    </PageHeader>

    <GroupForm
      :key="group.id"
      :action="`/admin/groups/${group.id}/edit/`"
      :initial="form"
      :errors="errors"
      :permissions-choices="permissions_choices"
      :members="group.user_usernames"
    />

    <DeleteConfirmDialog
      v-model:open="confirmOpen"
      :delete-url="`/admin/groups/${group.id}/delete/`"
      title="Delete group?"
      :description="`Members of '${group.name}' will lose the permissions it grants. This action cannot be undone.`"
    />
  </div>
</template>
