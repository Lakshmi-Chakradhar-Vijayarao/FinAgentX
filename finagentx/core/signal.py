from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Evidence:
    section: str
    change_type: str
    similarity: Optional[float]


@dataclass
class Signal:
    signal_type: str
    entity: str

    severity: str
    confidence: float
    evidence: List[Evidence]

    risk_score: Optional[float] = None
    risk_band: Optional[str] = None

    # NEW — temporal context
    delta_risk: Optional[float] = None
    trend: Optional[str] = None

    approved: bool = False
    rejection_reason: Optional[str] = None
    governance_notes: List[str] = field(default_factory=list)

    status: str = "GENERATED"

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
 