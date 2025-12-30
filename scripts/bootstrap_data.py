from pathlib import Path

RAW = Path("data/raw/sec")
OUT = Path("data/processed")
OUT.mkdir(exist_ok=True)

for txt in RAW.rglob("*.txt"):
    content = txt.read_text(errors="ignore")
    clean = " ".join(content.split())

    if len(clean) < 5000:
        continue  # drop junk filings

    out = OUT / txt.name
    out.write_text(clean)

print("✅ Data normalized and filtered.")
