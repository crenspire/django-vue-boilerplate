<script setup>
import { ref } from "vue"
import { Trash2 } from "lucide-vue-next"
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Button } from "@/Components/ui/button"
import DeleteConfirmDialog from "@/Components/admin/DeleteConfirmDialog.vue"
import PageHeader from "@/Components/admin/PageHeader.vue"
import UserAvatar from "@/Components/admin/UserAvatar.vue"
import UserForm from "@/Components/admin/UserForm.vue"
import { displayName } from "@/lib/format"

defineOptions({ layout: AdminLayout })

defineProps({
  user: { type: Object, required: true },
  form: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  groups_choices: { type: Array, default: () => [] },
  can_grant_superuser: { type: Boolean, default: false },
  can_delete: { type: Boolean, default: false },
  is_self: { type: Boolean, default: false },
})

const confirmOpen = ref(false)
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center gap-4">
      <UserAvatar :user="user" class="h-12 w-12 text-base" />
      <PageHeader
        class="flex-1"
        :title="displayName(user)"
        :description="`@${user.username}${user.email ? ` · ${user.email}` : ''}${is_self ? ' · This is you' : ''}`"
      >
        <template #actions>
          <Button v-if="can_delete" variant="outline" size="sm" class="text-destructive hover:bg-destructive/10 hover:text-destructive" @click="confirmOpen = true">
            <Trash2 class="h-4 w-4" />
            Delete user
          </Button>
        </template>
      </PageHeader>
    </div>

    <!-- Keyed by id so switching users re-initialises the form. -->
    <UserForm
      :key="user.id"
      :action="`/admin/users/${user.id}/edit/`"
      :initial="form"
      :errors="errors"
      :groups-choices="groups_choices"
      :can-grant-superuser="can_grant_superuser"
      :is-self="is_self"
    />

    <DeleteConfirmDialog
      v-model:open="confirmOpen"
      :delete-url="`/admin/users/${user.id}/delete/`"
      title="Delete user?"
      :description="`This permanently deletes '${user.username}' and removes them from all groups. This action cannot be undone.`"
    />
  </div>
</template>
