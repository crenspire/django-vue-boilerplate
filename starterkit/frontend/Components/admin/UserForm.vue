<script setup>
import { computed, ref } from "vue"
import { Link, useForm } from "@inertiajs/vue3"
import { Loader2, Search } from "lucide-vue-next"
import { Button } from "@/Components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/Components/ui/card"
import { Checkbox } from "@/Components/ui/checkbox"
import { Input } from "@/Components/ui/input"
import CheckboxCard from "@/Components/admin/CheckboxCard.vue"
import FormField from "@/Components/admin/FormField.vue"
import NonFieldErrors from "@/Components/admin/NonFieldErrors.vue"
import { toggleId } from "@/lib/utils"

const props = defineProps({
  action: { type: String, required: true },
  initial: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  groupsChoices: { type: Array, default: () => [] },
  canGrantSuperuser: { type: Boolean, default: false },
  isSelf: { type: Boolean, default: false },
  isCreate: { type: Boolean, default: false },
})

const form = useForm({
  username: props.initial.username ?? "",
  email: props.initial.email ?? "",
  first_name: props.initial.first_name ?? "",
  last_name: props.initial.last_name ?? "",
  is_staff: props.initial.is_staff ?? false,
  is_superuser: props.initial.is_superuser ?? false,
  is_active: props.initial.is_active ?? true,
  group_ids: [...(props.initial.group_ids ?? [])],
  password: "",
})

function submit() {
  form.post(props.action, {
    preserveScroll: true,
    onFinish: () => form.reset("password"),
  })
}

const flags = computed(() => [
  { key: "is_active", label: "Active", description: "Can sign in to the application." },
  { key: "is_staff", label: "Staff", description: "Can open this admin panel." },
  {
    key: "is_superuser",
    label: "Superuser",
    description: props.canGrantSuperuser ? "Has every permission without assigning them." : "Only superusers can grant this.",
  },
])

function flagDisabled(key) {
  return props.isSelf || (key === "is_superuser" && !props.canGrantSuperuser)
}

const groupQuery = ref("")
const filteredGroups = computed(() => {
  const q = groupQuery.value.trim().toLowerCase()
  return q ? props.groupsChoices.filter((g) => g.name.toLowerCase().includes(q)) : props.groupsChoices
})

function fieldError(name) {
  return props.errors?.[name]?.[0]
}
</script>

<template>
  <form class="flex flex-col gap-6" novalidate @submit.prevent="submit">
    <NonFieldErrors :errors="errors" />

    <div class="grid items-start gap-6 lg:grid-cols-5">
      <Card class="shadow-sm lg:col-span-3">
        <CardHeader>
          <CardTitle class="text-base font-semibold">Profile</CardTitle>
          <CardDescription>Sign-in details and how this person appears in the admin.</CardDescription>
        </CardHeader>
        <CardContent class="grid gap-5">
          <div class="grid gap-5 sm:grid-cols-2">
            <FormField label="Username" html-for="username" :error="fieldError('username')" required hint="Letters, digits and @/./+/-/_ only.">
              <Input id="username" v-model="form.username" autocomplete="off" :aria-invalid="Boolean(fieldError('username'))" :class="{ 'border-destructive': fieldError('username') }" />
            </FormField>
            <FormField
              label="Password"
              html-for="password"
              :error="fieldError('password')"
              :required="isCreate"
              :hint="isCreate ? 'At least 8 characters, not too common.' : 'Leave blank to keep the current password.'"
            >
              <Input id="password" v-model="form.password" type="password" autocomplete="new-password" :aria-invalid="Boolean(fieldError('password'))" :class="{ 'border-destructive': fieldError('password') }" />
            </FormField>
          </div>
          <FormField label="Email" html-for="email" :error="fieldError('email')">
            <Input id="email" v-model="form.email" type="email" placeholder="name@example.com" :aria-invalid="Boolean(fieldError('email'))" :class="{ 'border-destructive': fieldError('email') }" />
          </FormField>
          <div class="grid gap-5 sm:grid-cols-2">
            <FormField label="First name" html-for="first_name" :error="fieldError('first_name')">
              <Input id="first_name" v-model="form.first_name" />
            </FormField>
            <FormField label="Last name" html-for="last_name" :error="fieldError('last_name')">
              <Input id="last_name" v-model="form.last_name" />
            </FormField>
          </div>
        </CardContent>
      </Card>

      <div class="grid gap-6 lg:col-span-2">
        <Card class="shadow-sm">
          <CardHeader>
            <CardTitle class="text-base font-semibold">Access</CardTitle>
            <CardDescription>
              {{ isSelf ? "You can't change the status of your own account." : "Control whether this account can sign in and use the admin." }}
            </CardDescription>
          </CardHeader>
          <CardContent class="grid gap-3">
            <CheckboxCard
              v-for="flag in flags"
              :id="flag.key"
              :key="flag.key"
              v-model="form[flag.key]"
              :label="flag.label"
              :description="flag.description"
              :disabled="flagDisabled(flag.key)"
            />
          </CardContent>
        </Card>

        <Card class="shadow-sm">
          <CardHeader>
            <div class="flex items-center justify-between gap-2">
              <CardTitle class="text-base font-semibold">Groups</CardTitle>
              <span class="text-xs text-muted-foreground">{{ form.group_ids.length }} selected</span>
            </div>
            <CardDescription>Members inherit every permission of their groups.</CardDescription>
          </CardHeader>
          <CardContent class="grid gap-3">
            <p v-if="!groupsChoices.length" class="rounded-lg border border-dashed p-4 text-center text-sm text-muted-foreground">No groups yet.</p>
            <template v-else>
              <div v-if="groupsChoices.length > 6" class="relative">
                <Search class="pointer-events-none absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input v-model="groupQuery" placeholder="Filter groups…" class="h-8 pl-8" />
              </div>
              <div class="max-h-64 overflow-y-auto rounded-lg border">
                <label
                  v-for="g in filteredGroups"
                  :key="g.id"
                  :for="`group-${g.id}`"
                  class="flex items-center gap-3 border-b px-3 py-2.5 text-sm last:border-b-0"
                  :class="g.assignable || form.group_ids.includes(g.id) ? 'cursor-pointer hover:bg-accent/50' : 'cursor-not-allowed opacity-60'"
                  :title="g.assignable ? '' : 'You can only add groups whose permissions you also have.'"
                >
                  <Checkbox
                    :id="`group-${g.id}`"
                    :model-value="form.group_ids.includes(g.id)"
                    :disabled="!g.assignable && !form.group_ids.includes(g.id)"
                    @update:model-value="(checked) => toggleId(form.group_ids, g.id, checked)"
                  />
                  <span class="truncate">{{ g.name }}</span>
                </label>
                <p v-if="!filteredGroups.length" class="p-3 text-center text-sm text-muted-foreground">No matching groups.</p>
              </div>
            </template>
            <p v-if="fieldError('group_ids')" class="text-sm text-destructive">{{ fieldError("group_ids") }}</p>
          </CardContent>
        </Card>
      </div>
    </div>

    <div class="flex items-center justify-end gap-2 border-t pt-6">
      <Button as-child variant="outline">
        <Link href="/admin/users/">Cancel</Link>
      </Button>
      <Button type="submit" :disabled="form.processing">
        <Loader2 v-if="form.processing" class="h-4 w-4 animate-spin" />
        {{ isCreate ? "Create user" : "Save changes" }}
      </Button>
    </div>
  </form>
</template>
