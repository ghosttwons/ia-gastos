from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    date: str
    description: str
    amount: float
    method: Optional[str] = None
    category: Optional[str] = None

@dataclass
class Bill:
    name: str
    amount: float
    due_day: int
    category: Optional[str] = None
    notify_days_before: int = 0
