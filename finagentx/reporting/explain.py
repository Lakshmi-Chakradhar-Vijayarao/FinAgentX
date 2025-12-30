def explain(signal) -> str:
    lines = []

    lines.append(f"Entity: {signal.entity}")
    lines.append(f"Severity: {signal.severity}")
    lines.append(f"Risk Band: {signal.risk_band}")
    lines.append(f"Risk Score: {signal.risk_score}")

    if signal.delta_risk is not None:
        lines.append(f"Δ Risk: {signal.delta_risk}")

    if hasattr(signal, "trend"):
        lines.append(f"Trend: {signal.trend}")

    lines.append("")
    lines.append("Explanation:")

    if signal.severity == "HIGH":
        lines.append(
            "The system detected a semantic tail-risk shift in the disclosure. "
            "Although numerical score changes may appear moderate, the system "
            "is operating in a high-risk regime where persistence matters more "
            "than magnitude."
        )

    elif signal.severity == "MEDIUM":
        lines.append(
            "Moderate disclosure changes were detected, indicating emerging risk. "
            "Continued monitoring is recommended."
        )

    else:
        lines.append(
            "No material disclosure risk detected. Current filing aligns with historical patterns."
        )

    return "\n".join(lines)
