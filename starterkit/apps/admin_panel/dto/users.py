from dataclasses import dataclass
from typing import List, Mapping, Sequence


@dataclass(frozen=True)
class UserListItemDTO:
    id: int
    username: str
    email: str
    is_staff: bool
    is_superuser: bool
    is_active: bool


@dataclass(frozen=True)
class UserDetailDTO:
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_staff: bool
    is_superuser: bool
    is_active: bool
    group_ids: List[int]
    group_names: List[str]


@dataclass(frozen=True)
class UserFormInputDTO:
    username: str
    email: str
    first_name: str
    last_name: str
    is_staff: bool
    is_superuser: bool
    is_active: bool
    group_ids: List[int]
    password: str | None  # None = don't change; "" = clear; non-empty = set


@dataclass(frozen=True)
class UserFormResultDTO:
    success: bool
    user_id: int | None
    errors: Mapping[str, Sequence[str]]
