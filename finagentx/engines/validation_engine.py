from finagentx.core.signal import Signal


class ValidationEngine:
    """
    Governance layer = final decision authority.
    """

    def validate(self, signal: Signal) -> Signal:
        notes = []

        # Clamp confidence
        if signal.confidence > 1.0:
            signal.confidence = 1.0
            notes.append("Confidence clamped to 1.0")

        # Severity always wins
        if signal.severity == "HIGH":
            signal.risk_band = "HIGH"
            notes.append("Escalated to HIGH due to disclosure severity")

        elif signal.severity == "MEDIUM" and signal.risk_band == "LOW":
            signal.risk_band = "MEDIUM"
            notes.append("Escalated to MEDIUM due to disclosure severity")

        # Explain contradictions (do not override)
        if signal.severity == "HIGH" and signal.risk_score < 0.4:
            notes.append("High disclosure severity with moderate ML risk — reviewed")

        signal.approved = True
        signal.status = "VALIDATED"

        if not notes:
            notes.append("Signal passed governance checks")

        signal.governance_notes = notes
        return signal
