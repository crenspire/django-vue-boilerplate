<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from "vue"
import { router } from "@inertiajs/vue3"
import { CornerDownLeft, Laptop, Moon, Plus, Search, Sun } from "lucide-vue-next"
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/Components/ui/dialog"
import { useAdminNav } from "@/composables/useAdminNav"
import { useTheme } from "@/composables/useTheme"
import { cn } from "@/lib/utils"

const open = defineModel("open", { type: Boolean, default: false })

const { main, secondary, can } = useAdminNav()
const { setTheme } = useTheme()

const query = ref("")
const activeIndex = ref(0)
const inputRef = ref(null)

const groups = computed(() => {
  const pages = main.value.flatMap((item) => [
    { label: item.title, icon: item.icon, run: () => router.visit(item.href) },
  ])
  const actions = [
    can.value.add_users && { label: "Add user", icon: Plus, run: () => router.visit("/admin/users/create/") },
    can.value.add_groups && { label: "Add group", icon: Plus, run: () => router.visit("/admin/groups/create/") },
  ].filter(Boolean)
  const links = secondary.map((item) => ({ label: item.title, icon: item.icon, run: () => window.open(item.href, item.href.startsWith("http") ? "_blank" : "_self") }))
  const theme = [
    { label: "Light theme", icon: Sun, run: () => setTheme("light") },
    { label: "Dark theme", icon: Moon, run: () => setTheme("dark") },
    { label: "System theme", icon: Laptop, run: () => setTheme("system") },
  ]

  const q = query.value.trim().toLowerCase()
  const match = (item) => !q || item.label.toLowerCase().includes(q)
  return [
    { heading: "Pages", items: pages.filter(match) },
    { heading: "Actions", items: actions.filter(match) },
    { heading: "Links", items: links.filter(match) },
    { heading: "Theme", items: theme.filter(match) },
  ].filter((group) => group.items.length)
})

const flat = computed(() => groups.value.flatMap((group) => group.items))

const listRef = ref(null)

watch(query, () => (activeIndex.value = 0))
watch(activeIndex, () =>
  nextTick(() => listRef.value?.querySelector('[aria-selected="true"]')?.scrollIntoView({ block: "nearest" })),
)
watch(open, (value) => {
  if (value) {
    query.value = ""
    activeIndex.value = 0
    nextTick(() => inputRef.value?.focus())
  }
})

function run(item) {
  open.value = false
  item.run()
}

function onKeydown(event) {
  const count = flat.value.length
  if (!count) return
  if (event.key === "ArrowDown") {
    event.preventDefault()
    activeIndex.value = (activeIndex.value + 1) % count
  } else if (event.key === "ArrowUp") {
    event.preventDefault()
    activeIndex.value = (activeIndex.value - 1 + count) % count
  } else if (event.key === "Enter") {
    event.preventDefault()
    run(flat.value[activeIndex.value])
  }
}

function indexOf(item) {
  return flat.value.indexOf(item)
}

function onGlobalKeydown(event) {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault()
    open.value = !open.value
  }
}

onMounted(() => window.addEventListener("keydown", onGlobalKeydown))
onUnmounted(() => window.removeEventListener("keydown", onGlobalKeydown))
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="gap-0 overflow-hidden p-0 shadow-lg sm:max-w-lg [&>button]:hidden">
      <DialogTitle class="sr-only">Command menu</DialogTitle>
      <DialogDescription class="sr-only">Search pages and run actions.</DialogDescription>
      <div class="flex items-center border-b px-3">
        <Search class="mr-2 h-4 w-4 shrink-0 opacity-50" />
        <input
          ref="inputRef"
          v-model="query"
          class="flex h-11 w-full bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground"
          placeholder="Type a command or search…"
          role="combobox"
          aria-expanded="true"
          @keydown="onKeydown"
        />
      </div>
      <div ref="listRef" class="max-h-[320px] overflow-y-auto overflow-x-hidden p-1" role="listbox">
        <p v-if="!flat.length" class="py-6 text-center text-sm text-muted-foreground">No results found.</p>
        <div v-for="group in groups" :key="group.heading" class="overflow-hidden p-1 text-foreground">
          <div class="px-2 py-1.5 text-xs font-medium text-muted-foreground">{{ group.heading }}</div>
          <button
            v-for="item in group.items"
            :key="item.label"
            type="button"
            role="option"
            :aria-selected="indexOf(item) === activeIndex"
            :class="cn(
              'relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none [&>svg]:size-4 [&>svg]:shrink-0',
              indexOf(item) === activeIndex && 'bg-accent text-accent-foreground',
            )"
            @mousemove="activeIndex = indexOf(item)"
            @click="run(item)"
          >
            <component :is="item.icon" class="text-muted-foreground" />
            {{ item.label }}
          </button>
        </div>
      </div>
      <div class="flex items-center justify-end gap-3 border-t bg-muted/40 px-3 py-2 text-xs text-muted-foreground">
        <span class="flex items-center gap-1"><kbd class="rounded border bg-background px-1 font-mono">↑</kbd><kbd class="rounded border bg-background px-1 font-mono">↓</kbd> navigate</span>
        <span class="flex items-center gap-1"><kbd class="rounded border bg-background px-1 font-mono"><CornerDownLeft class="inline h-3 w-3" /></kbd> select</span>
        <span class="flex items-center gap-1"><kbd class="rounded border bg-background px-1 font-mono">esc</kbd> close</span>
      </div>
    </DialogContent>
  </Dialog>
</template>
