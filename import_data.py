
import json
from pathlib import Path
from config import articles

# Exact dataset path
DATASET_PATH = Path(
    r"C:\Users\prash\Downloads\NoSql Project\DataSet\News_Category_Dataset_v3.json"
)

# Check whether dataset exists
if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

# Prevent duplicate imports
existing = articles.count_documents({})

if existing > 0:
    print(f"Collection already contains {existing} documents.")
    print("Import cancelled to prevent duplicates.")
    raise SystemExit

batch_size = 1000
batch = []
total_inserted = 0

print("Starting JSON dataset import...")

with open(DATASET_PATH, "r", encoding="utf-8") as file:

    for line_number, line in enumerate(file, start=1):

        if not line.strip():
            continue

        try:
            document = json.loads(line)
            batch.append(document)

            if len(batch) >= batch_size:
                result = articles.insert_many(batch)
                total_inserted += len(result.inserted_ids)
                batch.clear()

                print(f"Inserted: {total_inserted}")

        except json.JSONDecodeError:
            print(f"Invalid JSON at line {line_number}")

# Insert remaining documents
if batch:
    result = articles.insert_many(batch)
    total_inserted += len(result.inserted_ids)

print("\nIMPORT COMPLETED SUCCESSFULLY")
print("Total documents inserted:", total_inserted)
print("MongoDB collection:", articles.name)
