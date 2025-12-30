from pathlib import Path
from datetime import datetime


class Document:
    def __init__(self, entity, doc_type, period, text):
        self.entity = entity
        self.doc_type = doc_type
        self.period = period
        self.text = text
        self.ingested_at = datetime.utcnow().isoformat()


class DocumentLoader:
    def load(self, path: Path) -> Document:
        # infer entity / doc type from path
        return Document(
            entity=path.parts[-3],
            doc_type=path.parts[-2],
            period=path.parts[-1],
            text=path.read_text(errors="ignore")
        )
