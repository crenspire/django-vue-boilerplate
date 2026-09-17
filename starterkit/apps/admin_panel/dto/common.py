from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationDTO:
    page: int
    page_size: int
    total: int
    total_pages: int
