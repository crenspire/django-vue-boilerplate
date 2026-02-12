import { createApp, h } from "vue"
import { createInertiaApp } from "@inertiajs/inertia-vue3"
import axios from "axios"
import "./main.css"

// Apply saved theme before first paint to avoid flash
const savedTheme = typeof localStorage !== "undefined" ? localStorage.getItem("admin-theme") : null
if (savedTheme === "dark") document.documentElement.classList.add("dark")
else document.documentElement.classList.remove("dark")

// Configure Axios to send Django CSRF token with all requests
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFToken"

// Eagerly register all page components with Vite's glob import
const pages = import.meta.glob("./Pages/**/*.vue")

createInertiaApp({
  resolve: (name) => {
    const importPage = pages[`./Pages/${name}.vue`]
    if (!importPage) {
      throw new Error(`Unknown Inertia page: ${name}`)
    }
    return importPage()
  },
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
})
