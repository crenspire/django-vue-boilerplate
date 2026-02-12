import { ref, watch, onMounted } from "vue"

const STORAGE_KEY = "admin-theme"

function getStored() {
  if (typeof window === "undefined") return "light"
  return window.localStorage.getItem(STORAGE_KEY) || "light"
}

function setClass(theme) {
  if (typeof document === "undefined") return
  const root = document.documentElement
  if (theme === "dark") {
    root.classList.add("dark")
  } else {
    root.classList.remove("dark")
  }
}

const theme = ref(getStored())

export function useTheme() {
  onMounted(() => {
    setClass(theme.value)
  })

  watch(
    theme,
    (value) => {
      setClass(value)
      if (typeof window !== "undefined") {
        window.localStorage.setItem(STORAGE_KEY, value)
      }
    },
    { immediate: false }
  )

  function toggle() {
    theme.value = theme.value === "dark" ? "light" : "dark"
  }

  function setTheme(value) {
    if (value === "dark" || value === "light") theme.value = value
  }

  return { theme, toggle, setTheme }
}
