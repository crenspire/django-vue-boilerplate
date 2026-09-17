import { computed, ref } from "vue"
import { router } from "@inertiajs/vue3"

const DEFAULT_PAGE_SIZE = 25

/**
 * Search, sort and pagination state for server-driven admin tables.
 * Every change is a GET visit so the URL stays shareable.
 */
export function useListQuery(baseUrl, props, defaultOrder) {
  const search = ref(props.filters?.search ?? "")
  const orderBy = computed(() => props.filters?.order_by ?? defaultOrder)

  function params(overrides = {}) {
    const pageSize = props.pagination?.page_size
    const query = {
      search: props.filters?.search || undefined,
      order_by: orderBy.value !== defaultOrder ? orderBy.value : undefined,
      page_size: pageSize && pageSize !== DEFAULT_PAGE_SIZE ? pageSize : undefined,
      ...overrides,
    }
    if (query.page_size === DEFAULT_PAGE_SIZE) query.page_size = undefined
    if (query.page === 1) query.page = undefined
    return Object.fromEntries(Object.entries(query).filter(([, value]) => value !== undefined && value !== ""))
  }

  function visit(query) {
    router.get(baseUrl, query, { preserveState: true, preserveScroll: true })
  }

  function url(query) {
    const qs = new URLSearchParams(query).toString()
    return qs ? `${baseUrl}?${qs}` : baseUrl
  }

  return {
    search,
    orderBy,
    doSearch: () => visit(params({ search: search.value, page: undefined })),
    clearSearch: () => visit(params({ search: undefined, page: undefined })),
    sort: (value) => visit(params({ order_by: value, page: undefined })),
    pageUrl: (page, extra = {}) => url(params({ page, ...extra })),
  }
}
