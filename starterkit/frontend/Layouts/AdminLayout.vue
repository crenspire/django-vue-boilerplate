<script setup>
import { ref } from "vue"
import { SidebarInset, SidebarProvider } from "@/Components/ui/sidebar"
import AppSidebar from "@/Components/admin/AppSidebar.vue"
import CommandMenu from "@/Components/admin/CommandMenu.vue"
import FlashToaster from "@/Components/admin/FlashToaster.vue"
import SiteHeader from "@/Components/admin/SiteHeader.vue"

const commandOpen = ref(false)
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <SiteHeader @open-command="commandOpen = true" />
      <div class="flex flex-1 flex-col gap-6 p-4 md:p-6">
        <slot />
      </div>
    </SidebarInset>
    <CommandMenu v-model:open="commandOpen" />
    <FlashToaster />
  </SidebarProvider>
</template>
