from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TodoQuery:
    status: str | None = None
    priority: str | None = None
