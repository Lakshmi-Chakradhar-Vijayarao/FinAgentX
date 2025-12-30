from pathlib import Path
from finagentx.orchestration.pipeline import FinAgentXPipeline

pipeline = FinAgentXPipeline(
    signal_store_path=Path("data/signals"),
    model_path=Path("data/metadata/risk_model.joblib")
)

from pathlib import Path
files = list(Path("data/processed").glob("*.txt"))

signal = pipeline.run(
    entity="JPM",
    prev_doc=files[0].read_text(),
    curr_doc=files[1].read_text()
)

print(signal)
