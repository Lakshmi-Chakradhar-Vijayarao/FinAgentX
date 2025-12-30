import json
from pathlib import Path
from dataclasses import asdict


class SignalStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, signal):
        entity_dir = self.root / signal.entity
        entity_dir.mkdir(exist_ok=True)

        path = entity_dir / f"{signal.created_at}.json"
        path.write_text(json.dumps(asdict(signal), indent=2))
