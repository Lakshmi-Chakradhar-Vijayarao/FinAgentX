import numpy as np
import re

RISK_KEYWORDS = [
    "credit risk", "liquidity", "default", "counterparty",
    "macroeconomic", "interest rate", "volatility",
    "capital adequacy", "regulatory", "stress"
]


def compute_severity(evidence):
    if not evidence:
        return "LOW"

    # Immediate escalation on deep tail drift
    for e in evidence:
        if e.similarity is not None and e.similarity < 0.50:
            return "HIGH"

    drifted = sum(
        1 for e in evidence
        if e.similarity is not None and e.similarity < 0.75
    )

    if drifted >= 3:
        return "HIGH"
    if drifted >= 1:
        return "MEDIUM"
    return "LOW"


def compute_confidence(evidence):
    if not evidence:
        return 0.25

    scores = [
        1.0 - e.similarity
        for e in evidence
        if e.similarity is not None
    ]

    return float(min(sum(scores) / len(scores), 1.0))


def compute_length_delta(prev_text, curr_text):
    if not prev_text:
        return 1.0
    return (len(curr_text) - len(prev_text)) / max(len(prev_text), 1)


def compute_risk_keyword_density(text):
    text = text.lower()
    return sum(len(re.findall(k, text)) for k in RISK_KEYWORDS)


def build_risk_feature_vector(signal) -> np.ndarray:
    return np.array([
        min(len(signal.evidence), 5) / 5.0,
        min(signal.num_sections_compared, 20) / 20.0,
        max(1.0 - signal.avg_similarity, 0.0),
        max(1.0 - signal.min_similarity, 0.0),  # tail risk
        np.clip(signal.avg_length_delta, -1.0, 1.0),
        min(signal.risk_keyword_hits, 20) / 20.0,
        signal.confidence
    ], dtype=float)
