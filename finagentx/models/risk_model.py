import joblib
import numpy as np
from pathlib import Path


class RiskModel:
    """
    Deterministic monotonic risk scorecard.
    No black-box ML. Fully auditable.
    """

    FEATURE_NAMES = [
        "evidence",
        "coverage",
        "avg_drift",
        "tail_drift",
        "length_delta",
        "keyword_density",
        "confidence"
    ]

    def __init__(self, weights: np.ndarray | None = None):
        self.weights = np.array(weights if weights is not None else [
            0.25,  # evidence
            0.10,  # coverage
            0.15,  # avg drift
            0.25,  # tail drift (CRITICAL)
            0.10,  # length delta
            0.10,  # keyword density
            0.05   # confidence
        ], dtype=float)

        self.weights /= self.weights.sum()  # normalize

    def train(self, X=None, y=None):
        return self  # no fitting required

    def predict(self, features: np.ndarray) -> float:
        score = float(np.dot(self.weights, features))
        return round(max(min(score, 1.0), 0.0), 3)

    def save(self, path: Path):
        joblib.dump(self.weights, path)

    def load(self, path: Path):
        self.weights = joblib.load(path)
