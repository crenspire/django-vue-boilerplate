<script setup>
import AuthLayout from "@/Layouts/AuthLayout.vue"
import { Button } from "@/Components/ui/button"
import { Input } from "@/Components/ui/input"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/Components/ui/card"
import { Alert, AlertDescription } from "@/Components/ui/alert"
import FormField from "@/Components/admin/FormField.vue"
import { useForm } from "@inertiajs/inertia-vue3"
import { AlertCircle } from "lucide-vue-next"

defineOptions({ layout: AuthLayout })

const props = defineProps({
  form: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) },
})

const loginForm = useForm({
  username: props.form?.username ?? "",
  password: props.form?.password ?? "",
  next: props.form?.next ?? "/admin/",
})
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Sign in</CardTitle>
      <CardDescription>Enter your credentials to access the admin panel</CardDescription>
    </CardHeader>
    <CardContent>
      <Alert v-if="errors?.non_field_errors?.length" variant="destructive" class="mb-6">
        <AlertCircle class="h-4 w-4" />
        <AlertDescription>
          <span v-for="(msg, i) in errors.non_field_errors" :key="i">{{ msg }}</span>
        </AlertDescription>
      </Alert>

      <form @submit.prevent="loginForm.post('/admin/login/')" class="space-y-4">
        <input type="hidden" name="next" :value="loginForm.next" />

        <FormField label="Username" html-for="username" :error="errors?.username?.[0]">
          <Input
            id="username"
            v-model="loginForm.username"
            type="text"
            autocomplete="username"
            placeholder="Enter your username"
            :class="{ 'border-destructive': errors?.username?.length }"
          />
        </FormField>

        <FormField label="Password" html-for="password" :error="errors?.password?.[0]">
          <Input
            id="password"
            v-model="loginForm.password"
            type="password"
            autocomplete="current-password"
            placeholder="Enter your password"
            :class="{ 'border-destructive': errors?.password?.length }"
          />
        </FormField>

        <Button type="submit" class="w-full" :disabled="loginForm.processing">
          Sign in
        </Button>
      </form>
    </CardContent>
  </Card>
</template>
