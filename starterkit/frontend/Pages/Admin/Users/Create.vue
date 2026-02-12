<script setup>
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Button } from "@/Components/ui/button"
import { Input } from "@/Components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/Components/ui/card"
import { Checkbox } from "@/Components/ui/checkbox"
import { Separator } from "@/Components/ui/separator"
import { Alert, AlertDescription } from "@/Components/ui/alert"
import FormField from "@/Components/admin/FormField.vue"
import PageHeader from "@/Components/admin/PageHeader.vue"
import { Link, useForm } from "@inertiajs/inertia-vue3"
import { AlertCircle } from "lucide-vue-next"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  groups_choices: { type: Array, default: () => [] },
})

const form = useForm({
  username: props.form?.username ?? "",
  email: props.form?.email ?? "",
  first_name: props.form?.first_name ?? "",
  last_name: props.form?.last_name ?? "",
  is_staff: props.form?.is_staff ?? false,
  is_superuser: props.form?.is_superuser ?? false,
  is_active: props.form?.is_active ?? true,
  group_ids: props.form?.group_ids ?? [],
  password: props.form?.password ?? "",
})

function toggleGroup(id) {
  const idx = form.group_ids.indexOf(id)
  if (idx > -1) {
    form.group_ids.splice(idx, 1)
  } else {
    form.group_ids.push(id)
  }
}
</script>

<template>
  <div class="space-y-6">
    <PageHeader
      title="Add user"
      :breadcrumbs="[{ label: 'Users', href: '/admin/users/' }]"
    />

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
        <CardTitle class="text-lg">User details</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="form.post('/admin/users/create/')" class="space-y-6">
          <div class="grid grid-cols-2 gap-4">
            <FormField label="Username" html-for="username" :error="errors?.username?.[0]" required>
              <Input id="username" v-model="form.username" type="text" :class="{ 'border-destructive': errors?.username?.length }" />
            </FormField>
            <FormField label="Password" html-for="password" :error="errors?.password?.[0]" required>
              <Input id="password" v-model="form.password" type="password" :class="{ 'border-destructive': errors?.password?.length }" />
            </FormField>
          </div>

          <FormField label="Email" html-for="email">
            <Input id="email" v-model="form.email" type="email" />
          </FormField>

          <div class="grid grid-cols-2 gap-4">
            <FormField label="First name" html-for="first_name">
              <Input id="first_name" v-model="form.first_name" type="text" />
            </FormField>
            <FormField label="Last name" html-for="last_name">
              <Input id="last_name" v-model="form.last_name" type="text" />
            </FormField>
          </div>

          <Separator />

          <div class="space-y-3">
            <p class="text-sm font-medium">Permissions</p>
            <div class="flex flex-wrap gap-6">
              <label class="flex items-center gap-2 cursor-pointer">
                <Checkbox :checked="form.is_staff" @update:checked="form.is_staff = $event" />
                <span class="text-sm">Staff status</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <Checkbox :checked="form.is_superuser" @update:checked="form.is_superuser = $event" />
                <span class="text-sm">Superuser</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <Checkbox :checked="form.is_active" @update:checked="form.is_active = $event" />
                <span class="text-sm">Active</span>
              </label>
            </div>
          </div>

          <Separator />

          <div class="space-y-3">
            <p class="text-sm font-medium">Groups</p>
            <Card class="max-h-48 overflow-y-auto">
              <CardContent class="p-3 space-y-2">
                <p v-if="!groups_choices.length" class="text-sm text-muted-foreground">No groups available.</p>
                <label v-for="g in groups_choices" :key="g.id" class="flex items-center gap-2 cursor-pointer">
                  <Checkbox
                    :checked="form.group_ids.includes(g.id)"
                    @update:checked="toggleGroup(g.id)"
                  />
                  <span class="text-sm">{{ g.name }}</span>
                </label>
              </CardContent>
            </Card>
          </div>

          <div class="flex gap-2 pt-2">
            <Button type="submit" :disabled="form.processing">Save</Button>
            <Link href="/admin/users/">
              <Button variant="outline" type="button">Cancel</Button>
            </Link>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
