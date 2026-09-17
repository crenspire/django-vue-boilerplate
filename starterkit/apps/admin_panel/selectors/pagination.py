from django.core.paginator import Paginator
from django.db.models import QuerySet

from apps.admin_panel.dto.common import PaginationDTO


def paginate(qs: QuerySet, *, page: int | str | None, page_size: int) -> tuple[list, PaginationDTO]:
    """
    Paginate with Django's Paginator. Invalid page numbers fall back to the first
    page and out-of-range numbers clamp to the last page instead of erroring.
    """
    paginator = Paginator(qs, page_size)
    current = paginator.get_page(page)
    total = paginator.count
    return list(current.object_list), PaginationDTO(
        page=current.number,
        page_size=page_size,
        total=total,
        total_pages=paginator.num_pages if total else 0,
    )
