from pathlib import Path
import re
from finagentx.features.disclosure_features import compute_risk_keyword_density

BASE_FILE = Path("data/processed/full-submission.txt")
OUT_DIR = Path("data/stress_tests")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 1500  # characters

MODERATE_STRESS = """
[STRESS SCENARIO – MODERATE]

The Company has experienced increased exposure to credit risk due to tightening
financial conditions. Market volatility and interest rate fluctuations may
adversely affect liquidity and funding costs. Management continues to monitor
counterparty exposure and macroeconomic uncertainty.
"""

SEVERE_STRESS = """
[STRESS SCENARIO – SEVERE]

The Company faces significant liquidity pressure driven by adverse macroeconomic
conditions. Credit deterioration across counterparties has increased default
risk. Prolonged market volatility, reduced capital adequacy, and regulatory
constraints may materially impair the Company’s ability to meet its obligations.
Stress scenarios indicate heightened risk of funding shortfalls under sustained
economic downturns.
"""


def chunk_text(text: str, size: int):
    return [text[i:i + size] for i in range(0, len(text), size)]


def choose_chunk(chunks):
    scored = []
    for idx, chunk in enumerate(chunks):
        score = len(chunk) + 500 * compute_risk_keyword_density(chunk)
        scored.append((score, idx))
    scored.sort(reverse=True)
    return scored[0][1]


base_text = BASE_FILE.read_text()
chunks = chunk_text(base_text, CHUNK_SIZE)

if not chunks:
    raise RuntimeError("No chunks generated")

target_idx = choose_chunk(chunks)

print(f"Injecting stress into chunk #{target_idx}")

def inject(chunks, idx, stress):
    chunks[idx] = chunks[idx] + "\n\n" + stress
    return "".join(chunks)

(Path("data/stress_tests/moderate_stress.txt")).write_text(
    inject(chunks.copy(), target_idx, MODERATE_STRESS)
)

(Path("data/stress_tests/severe_stress.txt")).write_text(
    inject(chunks.copy(), target_idx, SEVERE_STRESS)
)

print("✅ Stress injected into semantic chunk successfully.")
