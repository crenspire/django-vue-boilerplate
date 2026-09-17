import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

/** Add or remove `id` from an array of ids in place (for checkbox lists). */
export function toggleId(ids, id, checked) {
  const index = ids.indexOf(id)
  if (checked && index === -1) ids.push(id)
  if (!checked && index !== -1) ids.splice(index, 1)
}
