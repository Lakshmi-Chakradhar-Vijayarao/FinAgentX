import numpy as np
from pathlib import Path
from finagentx.models.risk_model import RiskModel

weights = np.array([
    0.30,  # evidence
    0.10,  # coverage
    0.15,  # avg drift
    0.35,  # tail drift
    0.05,  # length delta
    0.05,  # keywords
    0.00   # confidence (gating only)
])

model = RiskModel(weights=weights)
model.save(Path("data/metadata/risk_model.joblib"))

print("✅ Monotonic tail-aware risk scorecard saved (production-grade).")
