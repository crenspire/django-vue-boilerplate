<script setup>
import AdminLayout from "@/Layouts/AdminLayout.vue"
import PageHeader from "@/Components/admin/PageHeader.vue"
import UserForm from "@/Components/admin/UserForm.vue"

defineOptions({ layout: AdminLayout })

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  groups_choices: { type: Array, default: () => [] },
  can_grant_superuser: { type: Boolean, default: false },
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageHeader title="Add user" description="Create an account and choose what it can access." />
    <UserForm
      action="/admin/users/create/"
      :initial="form"
      :errors="errors"
      :groups-choices="groups_choices"
      :can-grant-superuser="can_grant_superuser"
      is-create
    />
  </div>
</template>
