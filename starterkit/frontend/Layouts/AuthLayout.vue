<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
    <div class="w-full max-w-md px-4">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-semibold text-foreground">Admin Panel</h1>
        <p class="text-sm text-muted-foreground mt-1">Sign in to manage your application</p>
      </div>
      <slot />
    </div>
  </div>
</template>
