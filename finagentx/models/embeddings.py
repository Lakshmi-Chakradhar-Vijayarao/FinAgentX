import hashlib
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, cache_dir: Path = Path("data/metadata/embeddings")):
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _hash(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def encode(self, texts):
        embeddings = []

        for text in texts:
            key = self._hash(text)
            cache_path = self.cache_dir / f"{key}.npy"

            if cache_path.exists():
                emb = np.load(cache_path)
            else:
                emb = self.model.encode(text)
                np.save(cache_path, emb)

            embeddings.append(emb)

        return np.vstack(embeddings)
