import hashlib
from pathlib import Path
from datetime import datetime


class SnapshotManager:
    def __init__(self, base_path: Path):
        self.base_path = base_path

    def create_snapshot(self, entity: str, content: str) -> Path:
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        hash_id = hashlib.md5(content.encode()).hexdigest()

        snapshot_path = self.base_path / entity / timestamp
        snapshot_path.mkdir(parents=True, exist_ok=True)

        file_path = snapshot_path / f"{hash_id}.txt"
        file_path.write_text(content)

        return file_path
