<script setup>
import AdminLayout from "@/Layouts/AdminLayout.vue"
import GroupForm from "@/Components/admin/GroupForm.vue"
import PageHeader from "@/Components/admin/PageHeader.vue"

defineOptions({ layout: AdminLayout })

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  permissions_choices: { type: Array, default: () => [] },
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageHeader title="Add group" description="Bundle permissions into a role you can assign to users." />
    <GroupForm action="/admin/groups/create/" :initial="form" :errors="errors" :permissions-choices="permissions_choices" is-create />
  </div>
</template>
