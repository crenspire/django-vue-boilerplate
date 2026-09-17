<script setup>
import { computed, ref } from "vue"
import { Link, useForm } from "@inertiajs/vue3"
import { Loader2, Search } from "lucide-vue-next"
import { Button } from "@/Components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/Components/ui/card"
import { Checkbox } from "@/Components/ui/checkbox"
import { Input } from "@/Components/ui/input"
import FormField from "@/Components/admin/FormField.vue"
import NonFieldErrors from "@/Components/admin/NonFieldErrors.vue"
import { toggleId } from "@/lib/utils"

const props = defineProps({
  action: { type: String, required: true },
  initial: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  permissionsChoices: { type: Array, default: () => [] },
  members: { type: Array, default: () => [] },
  isCreate: { type: Boolean, default: false },
})

const form = useForm({
  name: props.initial.name ?? "",
  permission_ids: [...(props.initial.permission_ids ?? [])],
})

const query = ref("")

// "auth.add_group" -> app "auth", label "Add group"
function describe(permission) {
  const [app, codename] = permission.codename.split(".")
  const [action, ...model] = codename.split("_")
  return { app, label: `${action.charAt(0).toUpperCase()}${action.slice(1)} ${model.join(" ")}` }
}

const sections = computed(() => {
  const q = query.value.trim().toLowerCase()
  const byApp = new Map()
  for (const permission of props.permissionsChoices) {
    const { app, label } = describe(permission)
    if (q && !`${permission.codename} ${label}`.toLowerCase().includes(q)) continue
    if (!byApp.has(app)) byApp.set(app, [])
    byApp.get(app).push({ ...permission, label })
  }
  return [...byApp.entries()].map(([app, items]) => ({
    app,
    items,
    selected: items.filter((p) => form.permission_ids.includes(p.id)).length,
  }))
})

function setSection(section, checked) {
  for (const permission of section.items) {
    if (permission.assignable || !checked) toggleId(form.permission_ids, permission.id, checked)
  }
}

function sectionState(section) {
  if (section.selected === 0) return false
  return section.selected === section.items.length ? true : "indeterminate"
}

function fieldError(name) {
  return props.errors?.[name]?.[0]
}
</script>

<template>
  <form class="flex flex-col gap-6" novalidate @submit.prevent="form.post(action, { preserveScroll: true })">
    <NonFieldErrors :errors="errors" />

    <div class="grid items-start gap-6 lg:grid-cols-5">
      <div class="grid gap-6 lg:col-span-2">
        <Card class="shadow-sm">
          <CardHeader>
            <CardTitle class="text-base font-semibold">Details</CardTitle>
            <CardDescription>A short, descriptive name such as “Editors” or “Support”.</CardDescription>
          </CardHeader>
          <CardContent class="grid gap-5">
            <FormField label="Name" html-for="name" :error="fieldError('name')" required>
              <Input id="name" v-model="form.name" :aria-invalid="Boolean(fieldError('name'))" :class="{ 'border-destructive': fieldError('name') }" />
            </FormField>
            <dl class="grid grid-cols-2 gap-3 text-sm">
              <div class="rounded-lg border p-3">
                <dt class="text-xs text-muted-foreground">Permissions</dt>
                <dd class="text-xl font-semibold tabular-nums">{{ form.permission_ids.length }}</dd>
              </div>
              <div class="rounded-lg border p-3">
                <dt class="text-xs text-muted-foreground">Members</dt>
                <dd class="text-xl font-semibold tabular-nums">{{ members.length }}</dd>
              </div>
            </dl>
          </CardContent>
        </Card>

        <Card v-if="!isCreate" class="shadow-sm">
          <CardHeader>
            <CardTitle class="text-base font-semibold">Members</CardTitle>
            <CardDescription>Manage membership from each user's page.</CardDescription>
          </CardHeader>
          <CardContent>
            <p v-if="!members.length" class="rounded-lg border border-dashed p-4 text-center text-sm text-muted-foreground">No members yet.</p>
            <div v-else class="flex flex-wrap gap-2">
              <span v-for="name in members" :key="name" class="rounded-md border bg-muted/40 px-2 py-1 text-xs font-medium">{{ name }}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card class="shadow-sm lg:col-span-3">
        <CardHeader>
          <div class="flex items-center justify-between gap-2">
            <CardTitle class="text-base font-semibold">Permissions</CardTitle>
            <span class="text-xs text-muted-foreground">{{ form.permission_ids.length }} of {{ permissionsChoices.length }} selected</span>
          </div>
          <CardDescription>Grouped by app. You can only add permissions you hold yourself.</CardDescription>
        </CardHeader>
        <CardContent class="grid gap-4">
          <div class="relative">
            <Search class="pointer-events-none absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input v-model="query" placeholder="Filter permissions…" class="h-9 pl-8" />
          </div>
          <div class="max-h-[28rem] space-y-4 overflow-y-auto pr-1">
            <p v-if="!sections.length" class="p-4 text-center text-sm text-muted-foreground">No matching permissions.</p>
            <section v-for="section in sections" :key="section.app" class="overflow-hidden rounded-lg border">
              <label class="flex cursor-pointer items-center gap-3 border-b bg-muted/40 px-3 py-2">
                <Checkbox :model-value="sectionState(section)" @update:model-value="(checked) => setSection(section, checked === true)" />
                <span class="text-sm font-medium capitalize">{{ section.app }}</span>
                <span class="ml-auto text-xs text-muted-foreground">{{ section.selected }}/{{ section.items.length }}</span>
              </label>
              <div class="grid sm:grid-cols-2">
                <label
                  v-for="p in section.items"
                  :key="p.id"
                  :for="`perm-${p.id}`"
                  class="flex items-center gap-3 px-3 py-2 text-sm"
                  :class="p.assignable || form.permission_ids.includes(p.id) ? 'cursor-pointer hover:bg-accent/50' : 'cursor-not-allowed opacity-60'"
                  :title="p.codename"
                >
                  <Checkbox
                    :id="`perm-${p.id}`"
                    :model-value="form.permission_ids.includes(p.id)"
                    :disabled="!p.assignable && !form.permission_ids.includes(p.id)"
                    @update:model-value="(checked) => toggleId(form.permission_ids, p.id, checked)"
                  />
                  <span class="truncate">{{ p.label }}</span>
                </label>
              </div>
            </section>
          </div>
          <p v-if="fieldError('permission_ids')" class="text-sm text-destructive">{{ fieldError("permission_ids") }}</p>
        </CardContent>
      </Card>
    </div>

    <div class="flex items-center justify-end gap-2 border-t pt-6">
      <Button as-child variant="outline">
        <Link href="/admin/groups/">Cancel</Link>
      </Button>
      <Button type="submit" :disabled="form.processing">
        <Loader2 v-if="form.processing" class="h-4 w-4 animate-spin" />
        {{ isCreate ? "Create group" : "Save changes" }}
      </Button>
    </div>
  </form>
</template>
