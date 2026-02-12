from dataclasses import dataclass
from typing import List, Mapping, Sequence


@dataclass(frozen=True)
class GroupListItemDTO:
    id: int
    name: str
    user_count: int
    permission_count: int


@dataclass(frozen=True)
class GroupDetailDTO:
    id: int
    name: str
    permission_ids: List[int]
    permission_codenames: List[str]
    user_ids: List[int]
    user_usernames: List[str]


@dataclass(frozen=True)
class GroupFormInputDTO:
    name: str
    permission_ids: List[int]


@dataclass(frozen=True)
class GroupFormResultDTO:
    success: bool
    group_id: int | None
    errors: Mapping[str, Sequence[str]]
