import csv
from pathlib import Path
from collections import deque
from typing import Dict, List


class RiskMemory:
    """
    Lightweight temporal memory for risk evolution.
    Optimized for single-entity demo and fast execution.
    """

    WINDOW = 3  # industry-standard rolling window

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, entity: str) -> Path:
        return self.root / f"{entity}.csv"

    def append(self, entity: str, record: Dict):
        path = self._path(entity)
        exists = path.exists()

        with path.open("a", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["timestamp", "risk_score", "risk_band", "severity"]
            )
            if not exists:
                writer.writeheader()
            writer.writerow(record)

    def last_n(self, entity: str) -> List[float]:
        path = self._path(entity)
        if not path.exists():
            return []

        rows = list(csv.DictReader(path.open()))
        scores = [float(r["risk_score"]) for r in rows]
        return scores[-self.WINDOW:]

    def compute_delta(self, entity: str, current: float):
        scores = self.last_n(entity)
        if not scores:
            return None
        return round(current - scores[-1], 3)

    def trend(self, entity: str) -> str:
        scores = self.last_n(entity)
        if len(scores) < 3:
            return "INSUFFICIENT_DATA"

        a, b, c = scores
        if a < b < c:
            return "ACCELERATING"
        if a > b > c:
            return "COOLING"
        if all(s >= 0.5 for s in scores):
            return "PERSISTENT_HIGH"
        if c - b > 0.3:
            return "SPIKE"
        return "STABLE"
