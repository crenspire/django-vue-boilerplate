<script setup>
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Link } from "@inertiajs/inertia-vue3"
import { Button } from "@/Components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/Components/ui/card"
import PageHeader from "@/Components/admin/PageHeader.vue"
import { Users, Shield, ArrowRight } from "lucide-vue-next"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  stats: { type: Object, default: () => ({ user_count: 0, group_count: 0 }) },
})
</script>

<template>
  <div class="space-y-8">
    <PageHeader title="Dashboard" />

    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Total Users</CardTitle>
          <Users class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ stats.user_count }}</div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Total Groups</CardTitle>
          <Shield class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ stats.group_count }}</div>
        </CardContent>
      </Card>
    </div>

    <div class="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle class="text-base">Manage Users</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground mb-4">Create, edit, and manage user accounts and permissions.</p>
          <Link href="/admin/users/">
            <Button variant="outline" size="sm">
              View Users
              <ArrowRight class="h-4 w-4 ml-2" />
            </Button>
          </Link>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle class="text-base">Manage Groups</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground mb-4">Organize users into groups and assign permissions.</p>
          <Link href="/admin/groups/">
            <Button variant="outline" size="sm">
              View Groups
              <ArrowRight class="h-4 w-4 ml-2" />
            </Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
