from finagentx.core.signal import Signal


def generate_report(signal: Signal) -> str:
    lines = []

    lines.append(f"Entity: {signal.entity}")
    lines.append(f"Severity: {signal.severity}")
    lines.append(f"Risk Band: {signal.risk_band}")
    lines.append(f"Risk Score: {signal.risk_score}")
    lines.append(f"Confidence: {round(signal.confidence, 3)}")

    if signal.delta_risk is not None:
        lines.append(f"Risk Delta (rolling): {signal.delta_risk}")

    if signal.trend:
        lines.append(f"Trend: {signal.trend}")

    if signal.evidence:
        lines.append("\nEvidence:")
        for e in signal.evidence:
            lines.append(
                f"- {e.section}: {e.change_type} "
                f"(similarity={round(e.similarity,3) if e.similarity else 'N/A'})"
            )

    lines.append("\nGovernance Notes:")
    for note in signal.governance_notes:
        lines.append(f"- {note}")

    return "\n".join(lines)
