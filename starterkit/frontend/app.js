import { createApp, h } from "vue"
import { createInertiaApp } from "@inertiajs/vue3"
import { applyStoredTheme } from "@/composables/useTheme"
import "@fontsource-variable/geist"
import "./main.css"

// Apply the saved (or system) theme before the first paint to avoid a flash.
applyStoredTheme()

const pages = import.meta.glob("./Pages/**/*.vue")

createInertiaApp({
  title: (title) => (title ? `${title} · Django Inertia Vue` : "Django Inertia Vue"),
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
  // Django's default CSRF cookie/header names (Inertia defaults to Laravel's).
  http: {
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
  },
})
