from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ProblemType(str, Enum):
    DISCLOSURE_CHANGE = "DISCLOSURE_CHANGE"
    RISK_SIGNAL = "RISK_SIGNAL"


@dataclass
class ProblemDefinition:
    problem_type: ProblemType
    entity: str
    time_window: str
    severity_threshold: Optional[str] = "MEDIUM"
