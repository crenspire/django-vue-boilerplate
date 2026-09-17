<script setup>
import { ref } from "vue"
import { Head, useForm } from "@inertiajs/vue3"
import { AlertCircle, Eye, EyeOff, Loader2 } from "lucide-vue-next"
import AuthLayout from "@/Layouts/AuthLayout.vue"
import { Alert, AlertDescription } from "@/Components/ui/alert"
import { Button } from "@/Components/ui/button"
import { Card, CardContent } from "@/Components/ui/card"
import { Input } from "@/Components/ui/input"
import { Label } from "@/Components/ui/label"
import AppLogo from "@/Components/admin/AppLogo.vue"

defineOptions({ layout: AuthLayout })

const props = defineProps({
  form: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) },
})

const loginForm = useForm({
  username: props.form?.username ?? "",
  password: "",
  next: props.form?.next ?? "/admin/",
})

const showPassword = ref(false)

function submit() {
  loginForm.post("/admin/login/", {
    onFinish: () => loginForm.reset("password"),
  })
}

const highlights = [
  { label: "Django 6", detail: "Auth, permissions & ORM" },
  { label: "Inertia v3", detail: "Server routing, SPA feel" },
  { label: "Vue 3", detail: "Composition API + Vite" },
  { label: "shadcn-vue", detail: "Accessible components" },
]
</script>

<template>
  <Head title="Sign in" />
  <div class="flex flex-col gap-6">
    <Card class="overflow-hidden p-0 shadow-lg">
      <CardContent class="grid p-0 md:grid-cols-2">
        <form class="p-6 md:p-10" novalidate @submit.prevent="submit">
          <div class="flex flex-col gap-6">
            <div class="flex flex-col items-center gap-3 text-center">
              <AppLogo class="size-10 rounded-xl" />
              <div class="space-y-1">
                <h1 class="text-2xl font-semibold tracking-tight">Welcome back</h1>
                <p class="text-balance text-sm text-muted-foreground">Sign in to your admin account to continue</p>
              </div>
            </div>

            <Alert v-if="errors?.non_field_errors?.length" variant="destructive">
              <AlertCircle class="h-4 w-4" />
              <AlertDescription>
                <p v-for="(msg, i) in errors.non_field_errors" :key="i">{{ msg }}</p>
              </AlertDescription>
            </Alert>

            <div class="grid gap-2">
              <Label for="username">Username</Label>
              <Input
                id="username"
                v-model="loginForm.username"
                type="text"
                autocomplete="username"
                placeholder="Enter your username"
                autofocus
                :aria-invalid="Boolean(errors?.username?.length)"
                :class="{ 'border-destructive focus-visible:ring-destructive': errors?.username?.length }"
              />
              <p v-if="errors?.username?.length" class="text-sm text-destructive">{{ errors.username[0] }}</p>
            </div>

            <div class="grid gap-2">
              <Label for="password">Password</Label>
              <div class="relative">
                <Input
                  id="password"
                  v-model="loginForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  class="pr-10"
                  :aria-invalid="Boolean(errors?.password?.length)"
                  :class="{ 'border-destructive focus-visible:ring-destructive': errors?.password?.length }"
                />
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 flex w-10 items-center justify-center rounded-r-md text-muted-foreground hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  :aria-pressed="showPassword"
                  @click="showPassword = !showPassword"
                >
                  <EyeOff v-if="showPassword" class="h-4 w-4" />
                  <Eye v-else class="h-4 w-4" />
                </button>
              </div>
              <p v-if="errors?.password?.length" class="text-sm text-destructive">{{ errors.password[0] }}</p>
            </div>

            <Button type="submit" class="w-full" :disabled="loginForm.processing">
              <Loader2 v-if="loginForm.processing" class="h-4 w-4 animate-spin" />
              {{ loginForm.processing ? "Signing in…" : "Sign in" }}
            </Button>

            <p class="text-center text-xs text-muted-foreground">
              Only active staff accounts can sign in. Ask a superuser if you need access.
            </p>
          </div>
        </form>

        <div class="relative hidden overflow-hidden bg-zinc-950 text-zinc-50 md:block">
          <!-- Decorative grid + glow; purely presentational. -->
          <div
            class="absolute inset-0 opacity-[0.15] [background-image:linear-gradient(to_right,#fff_1px,transparent_1px),linear-gradient(to_bottom,#fff_1px,transparent_1px)] [background-size:32px_32px] [mask-image:radial-gradient(ellipse_at_center,black_30%,transparent_75%)]"
            aria-hidden="true"
          />
          <div class="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-violet-600/30 blur-3xl" aria-hidden="true" />
          <div class="absolute -bottom-32 -left-16 h-72 w-72 rounded-full bg-indigo-500/20 blur-3xl" aria-hidden="true" />

          <div class="relative flex h-full flex-col justify-between p-10">
            <div class="flex items-center gap-2 text-sm font-medium">
              <AppLogo class="size-7 rounded-md bg-zinc-50" />
              Django Inertia
            </div>

            <div class="space-y-6">
              <blockquote class="space-y-2">
                <p class="text-lg font-medium leading-relaxed">
                  “One codebase, one server. Django keeps routing and auth, Vue and shadcn-vue make the interface a pleasure to use.”
                </p>
                <footer class="text-sm text-zinc-400">Django Inertia Vue starter kit</footer>
              </blockquote>
              <dl class="grid grid-cols-2 gap-3">
                <div
                  v-for="item in highlights"
                  :key="item.label"
                  class="rounded-lg border border-white/10 bg-white/5 p-3 backdrop-blur"
                >
                  <dt class="text-sm font-medium">{{ item.label }}</dt>
                  <dd class="mt-0.5 text-xs text-zinc-400">{{ item.detail }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
