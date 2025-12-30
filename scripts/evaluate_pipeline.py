from pathlib import Path
from finagentx.orchestration.pipeline import FinAgentXPipeline

PIPELINE = FinAgentXPipeline(
    signal_store_path=Path("data/signals"),
    model_path=Path("data/metadata/risk_model.joblib")
)

BASE = Path("data/processed/full-submission.txt").read_text()

TESTS = {
    "BASELINE": Path("data/processed/full-submission.txt").read_text(),
    "MODERATE_STRESS": Path("data/stress_tests/moderate_stress.txt").read_text(),
    "SEVERE_STRESS": Path("data/stress_tests/severe_stress.txt").read_text()
}

print("\n=== STRESS TEST RESULTS ===")
for name, doc in TESTS.items():
    signal = PIPELINE.run(
        entity="JPM",
        prev_doc=BASE,
        curr_doc=doc
    )

    print({
        "scenario": name,
        "severity": signal.severity,
        "confidence": signal.confidence,
        "risk_score": signal.risk_score,
        "risk_band": signal.risk_band,
        "approved": signal.approved,
        "governance_notes": signal.governance_notes
    })
