from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class TodoQuery:
    status: str | None = None
    priority: str | None = None


@dataclass(frozen=True, slots=True)
class TodoData:
    id: int
    title: str
    description: str
    status: str
    status_label: str
    priority: str
    priority_label: str
    due_date: date | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
