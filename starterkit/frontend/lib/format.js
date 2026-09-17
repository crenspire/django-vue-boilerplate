/** "First Last", else username, else email. */
export function displayName(user) {
  if (!user) return "User"
  const full = user.full_name || [user.first_name, user.last_name].filter(Boolean).join(" ")
  return full || user.username || user.email || "User"
}

/** Two-letter initials for avatars. */
export function initials(user) {
  if (!user) return "U"
  const name = displayName(user)
  const parts = name.split(/[\s._@-]+/).filter(Boolean)
  const letters = parts.length > 1 ? parts[0][0] + parts[1][0] : name.slice(0, 2)
  return letters.toUpperCase()
}

const relative = new Intl.RelativeTimeFormat(undefined, { numeric: "auto" })
const UNITS = [
  ["year", 60 * 60 * 24 * 365],
  ["month", 60 * 60 * 24 * 30],
  ["week", 60 * 60 * 24 * 7],
  ["day", 60 * 60 * 24],
  ["hour", 60 * 60],
  ["minute", 60],
]

/** "3 days ago", "just now". */
export function timeAgo(iso) {
  if (!iso) return "Never"
  const seconds = (new Date(iso).getTime() - Date.now()) / 1000
  for (const [unit, size] of UNITS) {
    if (Math.abs(seconds) >= size) return relative.format(Math.round(seconds / size), unit)
  }
  return "just now"
}

const dateFormat = new Intl.DateTimeFormat(undefined, { dateStyle: "medium" })

export function formatDate(iso) {
  return iso ? dateFormat.format(new Date(iso)) : "—"
}
