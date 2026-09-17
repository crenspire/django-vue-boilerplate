import { computed, ref, watch } from "vue"

const STORAGE_KEY = "admin-theme"
const isBrowser = typeof window !== "undefined"

function readStored() {
  try {
    const value = window.localStorage.getItem(STORAGE_KEY)
    return value === "dark" || value === "light" ? value : "system"
  } catch {
    return "system"
  }
}

const media = isBrowser ? window.matchMedia?.("(prefers-color-scheme: dark)") : null
const systemDark = ref(Boolean(media?.matches))
media?.addEventListener?.("change", (event) => (systemDark.value = event.matches))

function resolve(preference) {
  if (preference === "system") return systemDark.value ? "dark" : "light"
  return preference
}

function setClass(resolved) {
  document.documentElement.classList.toggle("dark", resolved === "dark")
}

/** Apply the saved theme (or the OS preference) before the app mounts to avoid a flash. */
export function applyStoredTheme() {
  setClass(resolve(readStored()))
}

// "light" | "dark" | "system"
const theme = ref(isBrowser ? readStored() : "system")
const resolvedTheme = computed(() => resolve(theme.value))

if (isBrowser) {
  watch(resolvedTheme, setClass)
  watch(theme, (value) => {
    try {
      if (value === "system") window.localStorage.removeItem(STORAGE_KEY)
      else window.localStorage.setItem(STORAGE_KEY, value)
    } catch {
      // Storage can be unavailable (private mode); the theme still applies for this session.
    }
  })
}

export function useTheme() {
  function setTheme(value) {
    if (["light", "dark", "system"].includes(value)) theme.value = value
  }

  function toggle() {
    theme.value = resolvedTheme.value === "dark" ? "light" : "dark"
  }

  return { theme, resolvedTheme, setTheme, toggle }
}
