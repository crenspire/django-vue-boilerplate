<script setup>
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Button } from "@/Components/ui/button"
import { Input } from "@/Components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/Components/ui/card"
import { Checkbox } from "@/Components/ui/checkbox"
import { Alert, AlertDescription } from "@/Components/ui/alert"
import FormField from "@/Components/admin/FormField.vue"
import PageHeader from "@/Components/admin/PageHeader.vue"
import DeleteConfirmDialog from "@/Components/admin/DeleteConfirmDialog.vue"
import { Link, useForm } from "@inertiajs/inertia-vue3"
import { AlertCircle, Trash2 } from "lucide-vue-next"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  group: { type: Object, required: true },
  form: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  permissions_choices: { type: Array, default: () => [] },
})

const form = useForm({
  name: props.form?.name ?? "",
  permission_ids: Array.isArray(props.form?.permission_ids) ? [...props.form.permission_ids] : [],
})

function togglePermission(id) {
  const idx = form.permission_ids.indexOf(id)
  if (idx > -1) {
    form.permission_ids.splice(idx, 1)
  } else {
    form.permission_ids.push(id)
  }
}
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      :title="`Edit ${group?.name}`"
      :breadcrumbs="[{ label: 'Groups', href: '/admin/groups/' }]"
    >
      <template #actions>
        <DeleteConfirmDialog
          :delete-url="`/admin/groups/${group?.id}/delete/`"
          title="Delete group"
          :description="`Are you sure you want to delete '${group?.name}'? This action cannot be undone.`"
        >
          <template #default="{ open }">
            <Button variant="destructive" @click="open">
              <Trash2 class="h-4 w-4 mr-2" />
              Delete group
            </Button>
          </template>
        </DeleteConfirmDialog>
      </template>
    </PageHeader>

    <Alert v-if="Object.keys(errors).length" variant="destructive">
      <AlertCircle class="h-4 w-4" />
      <AlertDescription>
        <ul class="list-disc list-inside">
          <li v-for="(msgs, key) in errors" :key="key">
            {{ key }}: {{ Array.isArray(msgs) ? msgs[0] : msgs }}
          </li>
        </ul>
      </AlertDescription>
    </Alert>

    <Card class="max-w-2xl">
      <CardHeader>
        <CardTitle class="text-lg">Group details</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="form.post(`/admin/groups/${group?.id}/edit/`)" class="space-y-6">
          <FormField label="Name" html-for="name" :error="errors?.name?.[0]" required>
            <Input id="name" v-model="form.name" type="text" :class="{ 'border-destructive': errors?.name?.length }" />
          </FormField>

          <div class="space-y-3">
            <p class="text-sm font-medium">Permissions</p>
            <Card class="max-h-60 overflow-y-auto">
              <CardContent class="p-3 space-y-2">
                <p v-if="!permissions_choices.length" class="text-sm text-muted-foreground">No permissions available.</p>
                <label v-for="p in permissions_choices" :key="p.id" class="flex items-center gap-2 cursor-pointer">
                  <Checkbox
                    :checked="form.permission_ids.includes(p.id)"
                    @update:checked="togglePermission(p.id)"
                  />
                  <span class="text-sm font-mono">{{ p.codename }}</span>
                </label>
              </CardContent>
            </Card>
          </div>

          <div class="flex gap-2 pt-2">
            <Button type="submit" :disabled="form.processing">Save</Button>
            <Link href="/admin/groups/">
              <Button variant="outline" type="button">Cancel</Button>
            </Link>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
