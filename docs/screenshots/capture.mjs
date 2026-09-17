/**
 * Regenerates the screenshots in this folder.
 *
 * Prerequisites (see docs/screenshots/README.md):
 *   - A Django server with demo data (`manage.py seed_demo`) serving the built frontend.
 *   - `puppeteer-core` installed somewhere Node can resolve from the current directory.
 *   - A local Chrome/Chromium (set CHROME_PATH if it is not in the default macOS location).
 *
 * Usage (from the repository root):
 *   node docs/screenshots/capture.mjs
 */
import { execFileSync } from "node:child_process"
import { createRequire } from "node:module"
import path from "node:path"
import { fileURLToPath } from "node:url"

const require = createRequire(path.join(process.cwd(), "noop.js"))
const { default: puppeteer } = await import(require.resolve("puppeteer-core"))

const BASE = process.env.BASE_URL ?? "http://localhost:8000"
const CHROME_PATH = process.env.CHROME_PATH ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
const OUT = path.dirname(fileURLToPath(import.meta.url))

// Log the demo accounts in by creating Django sessions directly (no passwords typed).
const sessionScript = `
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
keys = []
for name in ("admin", "manager"):
    user = get_user_model().objects.get(username=name)
    store = SessionStore()
    store[SESSION_KEY] = str(user.pk)
    store[BACKEND_SESSION_KEY] = "django.contrib.auth.backends.ModelBackend"
    store[HASH_SESSION_KEY] = user.get_session_auth_hash()
    store.create()
    keys.append(store.session_key)
print(" ".join(keys))
`
const output = execFileSync("uv", ["run", "python", "starterkit/manage.py", "shell", "-c", sessionScript], { encoding: "utf8" })
const [ADMIN, MANAGER] = output.trim().split("\n").pop().split(" ")

const desktop = { width: 1440, height: 900, deviceScaleFactor: 2 }
const mobile = { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
const host = new URL(BASE).hostname

const browser = await puppeteer.launch({
  executablePath: CHROME_PATH,
  headless: true,
  args: ["--hide-scrollbars", "--force-color-profile=srgb"],
})

const problems = []

async function openByLinkText(page, text) {
  const href = await page.$$eval("tbody a[href*='/edit/']", (links, t) => links.find((a) => a.textContent.includes(t))?.getAttribute("href"), text)
  if (!href) throw new Error(`No edit link containing "${text}"`)
  await page.goto(`${BASE}${href}`, { waitUntil: "networkidle0" })
}

async function shot(name, url, { theme = "light", session = ADMIN, viewport = desktop, sidebar = "true", before } = {}) {
  const context = await browser.createBrowserContext()
  const page = await context.newPage()
  await page.setViewport(viewport)
  await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: theme }])
  await page.evaluateOnNewDocument((t) => localStorage.setItem("admin-theme", t), theme)
  const cookies = [{ name: "sidebar_state", value: sidebar, domain: host, path: "/" }]
  if (session) cookies.push({ name: "sessionid", value: session, domain: host, path: "/" })
  await context.setCookie(...cookies)
  page.on("console", (m) => ["error", "warning"].includes(m.type()) && problems.push(`${name}: ${m.text()}`))
  page.on("pageerror", (e) => problems.push(`${name}: ${e}`))

  await page.goto(`${BASE}${url}`, { waitUntil: "networkidle0" })
  await page.evaluate(() => document.fonts.ready)
  if (before) await before(page)
  await new Promise((resolve) => setTimeout(resolve, 400))
  await page.screenshot({ path: path.join(OUT, `${name}.png`) })
  console.log(`✓ ${name}`)
  await context.close()
}

await shot("landing-light", "/", { session: null })
await shot("landing-dark", "/", { session: null, theme: "dark" })
await shot("login-light", "/admin/login/", { session: null })
await shot("login-dark", "/admin/login/", { session: null, theme: "dark" })
await shot("dashboard-light", "/admin/")
await shot("dashboard-dark", "/admin/", { theme: "dark" })
await shot("users-light", "/admin/users/")
await shot("users-dark", "/admin/users/", { theme: "dark" })
await shot("user-edit-light", "/admin/users/?search=olivia", { before: (page) => openByLinkText(page, "Olivia Martin") })
await shot("groups-light", "/admin/groups/")
await shot("group-edit-light", "/admin/groups/", { before: (page) => openByLinkText(page, "Group admins") })
await shot("command-menu-dark", "/admin/users/", {
  theme: "dark",
  before: async (page) => {
    await page.keyboard.down("Meta")
    await page.keyboard.press("k")
    await page.keyboard.up("Meta")
    await page.waitForSelector("[role=listbox]")
    await page.keyboard.type("add")
  },
})
await shot("sidebar-collapsed-light", "/admin/", { sidebar: "false" })
await shot("manager-dashboard-light", "/admin/", { session: MANAGER })
await shot("mobile-login", "/admin/login/", { viewport: mobile, session: null })
await shot("mobile-dashboard", "/admin/", { viewport: mobile })
await shot("mobile-sidebar", "/admin/", {
  viewport: mobile,
  before: async (page) => {
    await page.click("[data-sidebar=trigger]")
    await page.waitForSelector("[data-mobile=true]")
    await new Promise((resolve) => setTimeout(resolve, 600))
  },
})
await shot("mobile-users", "/admin/users/", { viewport: mobile, theme: "dark" })

await browser.close()

if (problems.length) {
  console.error(`\nConsole problems:\n${problems.join("\n")}`)
  process.exitCode = 1
}
