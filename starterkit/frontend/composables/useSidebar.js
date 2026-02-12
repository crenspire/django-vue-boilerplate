import { ref, watch, onMounted } from "vue"

const STORAGE_KEY = "admin-sidebar-open"

function getStored() {
  if (typeof window === "undefined") return true
  const v = window.localStorage.getItem(STORAGE_KEY)
  if (v === "false") return false
  if (v === "true") return true
  return true
}

const sidebarOpen = ref(getStored())

export function useSidebar() {
  onMounted(() => {
    sidebarOpen.value = getStored()
  })

  watch(
    sidebarOpen,
    (value) => {
      if (typeof window !== "undefined") {
        window.localStorage.setItem(STORAGE_KEY, String(value))
      }
    },
    { immediate: false }
  )

  function toggle() {
    sidebarOpen.value = !sidebarOpen.value
  }

  return { sidebarOpen, toggle }
}
