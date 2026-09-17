<script setup>
import { reactive, watch } from "vue"
import { Link } from "@inertiajs/vue3"
import { ChevronRight } from "lucide-vue-next"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/Components/ui/collapsible"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/Components/ui/sidebar"

const props = defineProps({
  items: { type: Array, required: true },
})

// The layout persists across visits, so expand the active section whenever navigation changes it.
const openSections = reactive({})
watch(
  () => props.items.filter((item) => item.isActive).map((item) => item.title),
  (active) => active.forEach((title) => (openSections[title] = true)),
  { immediate: true },
)
</script>

<template>
  <SidebarGroup>
    <SidebarGroupLabel>Platform</SidebarGroupLabel>
    <SidebarMenu>
      <Collapsible v-for="item in items" :key="item.title" v-model:open="openSections[item.title]" as-child>
        <SidebarMenuItem>
          <SidebarMenuButton as-child :tooltip="item.title" :is-active="item.isActive">
            <Link :href="item.href">
              <component :is="item.icon" />
              <span>{{ item.title }}</span>
            </Link>
          </SidebarMenuButton>
          <template v-if="item.items?.length">
            <CollapsibleTrigger as-child>
              <SidebarMenuAction class="data-[state=open]:rotate-90">
                <ChevronRight />
                <span class="sr-only">Toggle {{ item.title }}</span>
              </SidebarMenuAction>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarMenuSub>
                <SidebarMenuSubItem v-for="sub in item.items" :key="sub.title">
                  <SidebarMenuSubButton as-child :is-active="sub.isActive">
                    <Link :href="sub.href">
                      <span>{{ sub.title }}</span>
                    </Link>
                  </SidebarMenuSubButton>
                </SidebarMenuSubItem>
              </SidebarMenuSub>
            </CollapsibleContent>
          </template>
        </SidebarMenuItem>
      </Collapsible>
    </SidebarMenu>
  </SidebarGroup>
</template>
