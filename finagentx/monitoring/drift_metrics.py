def drift_rate(signals):
    if not signals:
        return 0.0
    return round(
        sum(1 for s in signals if s.severity == "HIGH") / len(signals),
        3
    )
