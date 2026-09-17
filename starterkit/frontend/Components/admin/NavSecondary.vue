<script setup>
import { SidebarGroup, SidebarGroupContent, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from "@/Components/ui/sidebar"

defineProps({
  items: { type: Array, required: true },
})

const isExternal = (href) => /^https?:\/\//.test(href)
</script>

<template>
  <SidebarGroup>
    <SidebarGroupContent>
      <SidebarMenu>
        <SidebarMenuItem v-for="item in items" :key="item.title">
          <SidebarMenuButton as-child size="sm" :tooltip="item.title">
            <a :href="item.href" :target="isExternal(item.href) ? '_blank' : undefined" :rel="isExternal(item.href) ? 'noopener noreferrer' : undefined">
              <component :is="item.icon" />
              <span>{{ item.title }}</span>
            </a>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarGroupContent>
  </SidebarGroup>
</template>
