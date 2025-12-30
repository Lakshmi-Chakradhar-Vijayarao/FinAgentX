import numpy as np
from typing import List
from finagentx.models.embeddings import EmbeddingModel
from finagentx.features.section_parser import SectionParser
from finagentx.features.disclosure_features import (
    compute_severity,
    compute_confidence,
    compute_length_delta,
    compute_risk_keyword_density
)
from finagentx.core.signal import Signal, Evidence


def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
        if len(words[i:i + chunk_size]) > 50
    ]


class DisclosureChangeEngine:
    def __init__(self, drift_threshold: float = 0.85):
        self.embedder = EmbeddingModel()
        self.parser = SectionParser()
        self.drift_threshold = drift_threshold

    def build_signal(self, entity: str, prev_doc: str, curr_doc: str) -> Signal:
        prev_sections = self.parser.parse(prev_doc)
        curr_sections = self.parser.parse(curr_doc)

        evidence = []
        similarities = []
        length_deltas = []
        keyword_hits = 0

        # --- SECTION MODE ---
        if prev_sections and curr_sections:
            for section, curr_text in curr_sections.items():
                prev_text = prev_sections.get(section)
                if not prev_text:
                    evidence.append(Evidence(section, "NEW_SECTION", None))
                    keyword_hits += compute_risk_keyword_density(curr_text)
                    continue

                emb = self.embedder.encode([prev_text, curr_text])
                sim = float(np.dot(emb[0], emb[1]))
                similarities.append(sim)

                length_deltas.append(
                    compute_length_delta(prev_text, curr_text)
                )
                keyword_hits += compute_risk_keyword_density(curr_text)

                if sim < self.drift_threshold:
                    evidence.append(Evidence(section, "SEMANTIC_DRIFT", sim))

        # --- CHUNK FALLBACK ---
        else:
            prev_chunks = chunk_text(prev_doc)
            curr_chunks = chunk_text(curr_doc)

            if prev_chunks and curr_chunks:
                n = min(len(prev_chunks), len(curr_chunks))
                embeddings = self.embedder.encode(
                    prev_chunks[:n] + curr_chunks[:n]
                )

                for i in range(n):
                    sim = float(
                        np.dot(embeddings[i], embeddings[i + n])
                    )
                    similarities.append(sim)

                length_deltas.append(
                    compute_length_delta(prev_doc, curr_doc)
                )
                keyword_hits = compute_risk_keyword_density(curr_doc)

                if min(similarities) < self.drift_threshold:
                    evidence.append(
                        Evidence("DOCUMENT", "SEMANTIC_TAIL_DRIFT", min(similarities))
                    )

        severity = compute_severity(evidence)
        confidence = compute_confidence(evidence)

        # Confidence floor for unstructured drift
        if not evidence and similarities:
            confidence = 0.25

        signal = Signal(
            signal_type="DISCLOSURE_CHANGE",
            entity=entity,
            severity=severity,
            confidence=confidence,
            evidence=evidence
        )

        # Aggregated features
        signal.num_sections_compared = len(similarities)
        signal.avg_similarity = float(np.mean(similarities)) if similarities else 1.0
        signal.min_similarity = float(np.min(similarities)) if similarities else 1.0
        signal.avg_length_delta = float(np.mean(length_deltas)) if length_deltas else 0.0
        signal.risk_keyword_hits = keyword_hits

        return signal
