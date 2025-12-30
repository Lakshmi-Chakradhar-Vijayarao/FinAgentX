import yaml
from pathlib import Path


class PolicyEngine:
    """
    Minimal, auditable policy engine.
    """

    def __init__(self, policy_path: Path):
        if policy_path.exists():
            self.rules = yaml.safe_load(policy_path.read_text()) or {}
        else:
            self.rules = {}

    def evaluate(self, signal):
        actions = []

        for rule in self.rules.get("rules", []):
            cond = rule.get("if", {})
            matched = True

            for key, val in cond.items():
                if not hasattr(signal, key) or getattr(signal, key) != val:
                    matched = False

            if matched:
                actions.append(rule.get("then", {}))

        return actions
