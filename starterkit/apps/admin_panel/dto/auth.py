from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class LoginInputDTO:
    """
    Immutable container for login request data.
    """

    username: str
    password: str
    next_url: str | None


@dataclass(frozen=True)
class LoginResultDTO:
    """
    Result of attempting to log a user in.
    """

    success: bool
    redirect_url: str | None
    user_id: int | None
    username: str | None
    is_staff: bool
    is_superuser: bool
    errors: Mapping[str, Sequence[str]]

