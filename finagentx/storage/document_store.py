from typing import Dict, List
from pathlib import Path


class DocumentStore:
    def __init__(self, root: Path):
        self.root = root

    def list_versions(self, entity: str) -> List[Path]:
        entity_path = self.root / entity
        return sorted(entity_path.glob("*")) if entity_path.exists() else []

    def load_document(self, path: Path) -> str:
        return path.read_text()
