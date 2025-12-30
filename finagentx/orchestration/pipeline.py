from pathlib import Path
from finagentx.engines.disclosure_engine import DisclosureChangeEngine
from finagentx.engines.validation_engine import ValidationEngine
from finagentx.storage.signal_store import SignalStore
from finagentx.models.risk_model import RiskModel
from finagentx.features.disclosure_features import build_risk_feature_vector
from finagentx.monitoring.risk_memory import RiskMemory
from finagentx.reporting.explain import explain
from finagentx.policy.policy_engine import PolicyEngine


class FinAgentXPipeline:
    def __init__(self, signal_store_path: Path, model_path: Path):
        self.disclosure_engine = DisclosureChangeEngine()
        self.validation_engine = ValidationEngine()
        self.signal_store = SignalStore(signal_store_path)

        self.risk_model = RiskModel()
        self.risk_model.load(model_path)

        self.risk_memory = RiskMemory(Path("data/risk_memory"))
        self.policy = PolicyEngine(Path("configs/policy.yaml"))

    def run(self, entity: str, prev_doc: str, curr_doc: str):
        signal = self.disclosure_engine.build_signal(entity, prev_doc, curr_doc)

        features = build_risk_feature_vector(signal)
        risk_score = self.risk_model.predict(features)
        signal.risk_score = round(float(risk_score), 3)

        if risk_score > 0.75:
            signal.risk_band = "HIGH"
        elif risk_score > 0.40:
            signal.risk_band = "MEDIUM"
        else:
            signal.risk_band = "LOW"

        signal.delta_risk = self.risk_memory.compute_delta(entity, signal.risk_score)
        signal.trend = self.risk_memory.trend(entity)

        signal = self.validation_engine.validate(signal)

        self.signal_store.save(signal)
        self.risk_memory.append(entity, {
            "timestamp": signal.created_at,
            "risk_score": signal.risk_score,
            "risk_band": signal.risk_band,
            "severity": signal.severity
        })

        signal.explanation = explain(signal)
        return signal
