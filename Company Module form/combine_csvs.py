import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / "combined_all.csv"
SEPARATE_DIR = ROOT / "separated_csv"

source_files = sorted(f for f in ROOT.glob("*.csv") if f.name != OUTPUT_FILE.name)

all_columns = ["SourceFile"]
rows = []
rows_by_source = defaultdict(list)

for csv_path in source_files:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for col in reader.fieldnames or []:
            if col not in all_columns:
                all_columns.append(col)
        for record in reader:
            row = {"SourceFile": csv_path.name}
            row.update(record)
            rows.append(row)
            rows_by_source[csv_path.name].append(row)

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_columns)
    writer.writeheader()
    for row in rows:
        writer.writerow({col: row.get(col, "") for col in all_columns})

SEPARATE_DIR.mkdir(exist_ok=True)
for source_name, source_rows in rows_by_source.items():
    out_path = SEPARATE_DIR / source_name
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns)
        writer.writeheader()
        for row in source_rows:
            writer.writerow({col: row.get(col, "") for col in all_columns})

print(
    f"Combined {len(source_files)} files into {OUTPUT_FILE.name} "
    f"with {len(rows)} rows and wrote {len(rows_by_source)} separate files "
    f"to {SEPARATE_DIR.name}."
)
