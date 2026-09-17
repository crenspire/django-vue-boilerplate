<script setup>
import { computed } from "vue"
import { Link, usePage } from "@inertiajs/vue3"
import { ArrowRight, KeyRound, Shield, ShieldCheck, TrendingDown, TrendingUp, UserCheck, UserPlus, Users } from "lucide-vue-next"
import AdminLayout from "@/Layouts/AdminLayout.vue"
import { Badge } from "@/Components/ui/badge"
import { Button } from "@/Components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/Components/ui/card"
import PageHeader from "@/Components/admin/PageHeader.vue"
import UserAvatar from "@/Components/admin/UserAvatar.vue"
import { displayName, timeAgo } from "@/lib/format"

defineOptions({ layout: AdminLayout })

const props = defineProps({
  stats: { type: Object, default: () => ({ users: null, groups: null }) },
  recent_users: { type: Array, default: () => [] },
  top_groups: { type: Array, default: () => [] },
})

const page = usePage()
const me = computed(() => page.props.auth?.user)
const can = computed(() => me.value?.permissions ?? {})

const greeting = computed(() => {
  const hour = new Date().getHours()
  const part = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening"
  return `${part}, ${me.value?.first_name || me.value?.username || "there"}`
})

const percent = (part, whole) => (whole ? Math.round((part / whole) * 100) : 0)

const cards = computed(() => {
  const users = props.stats.users
  const groups = props.stats.groups
  const list = []
  if (users) {
    const delta = users.new_last_30_days - users.new_previous_30_days
    list.push(
      {
        label: "Total users",
        value: users.total,
        icon: Users,
        badge: `${delta >= 0 ? "+" : ""}${delta} vs last period`,
        trend: delta >= 0 ? TrendingUp : TrendingDown,
        headline: `${users.new_last_30_days} joined in the last 30 days`,
        detail: `${users.new_previous_30_days} in the 30 days before`,
      },
      {
        label: "Active accounts",
        value: users.active,
        icon: UserCheck,
        badge: `${percent(users.active, users.total)}% of users`,
        trend: null,
        headline: "Allowed to sign in",
        detail: `${users.total - users.active} inactive ${users.total - users.active === 1 ? "account" : "accounts"}`,
      },
      {
        label: "Staff members",
        value: users.staff,
        icon: ShieldCheck,
        badge: `${percent(users.staff, users.total)}% of users`,
        trend: null,
        headline: "Can open this admin",
        detail: "Access is scoped by permissions",
      },
    )
  }
  if (groups) {
    list.push({
      label: "Groups",
      value: groups.total,
      icon: Shield,
      badge: `${groups.with_members} in use`,
      trend: null,
      headline: "Permission bundles",
      detail: `${groups.total - groups.with_members} without members`,
    })
  }
  return list
})

const maxMembers = computed(() => Math.max(1, ...props.top_groups.map((g) => g.user_count)))
</script>

<template>
  <div class="flex flex-col gap-6">
    <PageHeader title="Dashboard" :description="`${greeting}. Here's an overview of your workspace.`">
      <template #actions>
        <Button v-if="can.add_users" as-child size="sm">
          <Link href="/admin/users/create/">
            <UserPlus class="h-4 w-4" />
            Add user
          </Link>
        </Button>
      </template>
    </PageHeader>

    <div
      v-if="cards.length"
      class="grid grid-cols-1 gap-4 sm:grid-cols-2"
      :class="cards.length >= 4 ? 'xl:grid-cols-4' : 'xl:grid-cols-3'"
    >
      <Card
        v-for="card in cards"
        :key="card.label"
        class="flex flex-col bg-gradient-to-t from-primary/[0.03] to-card shadow-sm dark:bg-card"
      >
        <CardHeader class="relative space-y-1 pb-2">
          <CardDescription class="flex items-center gap-2">
            <component :is="card.icon" class="h-4 w-4" />
            {{ card.label }}
          </CardDescription>
          <CardTitle class="text-3xl font-semibold tabular-nums">{{ card.value }}</CardTitle>
          <div class="absolute right-4 top-4">
            <Badge variant="outline" class="gap-1 rounded-lg px-1.5 text-xs font-normal">
              <component :is="card.trend" v-if="card.trend" class="h-3 w-3" />
              {{ card.badge }}
            </Badge>
          </div>
        </CardHeader>
        <CardFooter class="mt-auto flex-col items-start gap-1 pt-2 text-sm">
          <div class="line-clamp-1 flex gap-2 font-medium">{{ card.headline }}</div>
          <div class="text-muted-foreground">{{ card.detail }}</div>
        </CardFooter>
      </Card>
    </div>

    <div class="grid gap-4 lg:grid-cols-7">
      <Card v-if="can.view_users" class="shadow-sm" :class="can.view_groups ? 'lg:col-span-4' : 'lg:col-span-7'">
        <CardHeader class="flex flex-row items-start justify-between space-y-0">
          <div class="space-y-1.5">
            <CardTitle class="text-base font-semibold">Recent sign-ups</CardTitle>
            <CardDescription>The newest accounts in your workspace.</CardDescription>
          </div>
          <Button as-child variant="outline" size="sm">
            <Link href="/admin/users/?order_by=-date_joined">
              View all
              <ArrowRight class="h-4 w-4" />
            </Link>
          </Button>
        </CardHeader>
        <CardContent>
          <p v-if="!recent_users.length" class="py-8 text-center text-sm text-muted-foreground">No users yet.</p>
          <ul v-else class="divide-y">
            <li v-for="u in recent_users" :key="u.id" class="flex items-center gap-3 py-3 first:pt-0 last:pb-0">
              <UserAvatar :user="u" class="h-9 w-9" />
              <div class="grid min-w-0 flex-1 leading-tight">
                <Link v-if="can.change_users && (me.is_superuser || !u.is_superuser)" :href="`/admin/users/${u.id}/edit/`" class="truncate text-sm font-medium hover:underline">
                  {{ displayName(u) }}
                </Link>
                <span v-else class="truncate text-sm font-medium">{{ displayName(u) }}</span>
                <span class="truncate text-xs text-muted-foreground">{{ u.email || `@${u.username}` }}</span>
              </div>
              <Badge v-if="u.is_superuser" variant="secondary" class="hidden font-normal sm:inline-flex">Superuser</Badge>
              <Badge v-else-if="u.is_staff" variant="outline" class="hidden font-normal sm:inline-flex">Staff</Badge>
              <span class="w-24 shrink-0 text-right text-xs text-muted-foreground">{{ timeAgo(u.date_joined) }}</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <Card v-if="can.view_groups" class="shadow-sm" :class="can.view_users ? 'lg:col-span-3' : 'lg:col-span-7'">
        <CardHeader class="flex flex-row items-start justify-between space-y-0">
          <div class="space-y-1.5">
            <CardTitle class="text-base font-semibold">Groups by members</CardTitle>
            <CardDescription>Where your users get their permissions.</CardDescription>
          </div>
          <Button as-child variant="outline" size="sm">
            <Link href="/admin/groups/">
              View all
              <ArrowRight class="h-4 w-4" />
            </Link>
          </Button>
        </CardHeader>
        <CardContent>
          <p v-if="!top_groups.length" class="py-8 text-center text-sm text-muted-foreground">No groups yet.</p>
          <ul v-else class="space-y-4">
            <li v-for="g in top_groups" :key="g.id" class="space-y-2">
              <div class="flex items-center justify-between gap-2 text-sm">
                <span class="truncate font-medium">{{ g.name }}</span>
                <span class="flex shrink-0 items-center gap-3 text-xs text-muted-foreground">
                  <span class="flex items-center gap-1"><Users class="h-3 w-3" />{{ g.user_count }}</span>
                  <span class="flex items-center gap-1"><KeyRound class="h-3 w-3" />{{ g.permission_count }}</span>
                </span>
              </div>
              <div class="h-2 overflow-hidden rounded-full bg-muted" role="progressbar" :aria-valuenow="g.user_count" :aria-valuemax="maxMembers" :aria-label="`${g.name} members`">
                <div class="h-full rounded-full bg-primary transition-all" :style="{ width: `${Math.max(2, (g.user_count / maxMembers) * 100)}%` }" />
              </div>
            </li>
          </ul>
        </CardContent>
      </Card>

      <Card v-if="!can.view_users && !can.view_groups" class="lg:col-span-7">
        <CardContent class="flex flex-col items-center gap-2 py-10 text-center">
          <Shield class="h-6 w-6 text-muted-foreground" />
          <p class="font-medium">No admin permissions yet</p>
          <p class="text-sm text-muted-foreground">Your account has staff access. Ask a superuser to add you to a group.</p>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
