
import re
from datetime import datetime
from pymongo import UpdateOne
from config import articles

print("=" * 60)
print("NEWS DATA CLEANING STARTED")
print("=" * 60)


# Clean text fields
def clean_text(value):
    if value is None:
        return None

    if not isinstance(value, str):
        return str(value).strip()

    value = value.strip()
    value = re.sub(r"\s+", " ", value)

    return value if value else None
# Convert date into datetime
def clean_date(value):
    if not value:
        return None

    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d")
    except (ValueError, AttributeError):
        return None
total = articles.count_documents({})
print("Total documents:", total)

batch = []
batch_size = 1000
processed = 0

cursor = articles.find(
    {},
    {
        "headline": 1,
        "category": 1,
        "authors": 1,
        "short_description": 1,
        "date": 1,
        "link": 1
    }
)

for document in cursor:

    headline = clean_text(document.get("headline"))
    category = clean_text(document.get("category"))
    description = clean_text(document.get("short_description"))
    authors = clean_text(document.get("authors"))
    link = clean_text(document.get("link"))

    original_date = document.get("date")
    parsed_date = clean_date(original_date)

    update_data = {
        "headline_clean": headline,
        "category_clean": category.upper() if category else None,
        "description_clean": description,
        "authors_clean": authors,
        "link_clean": link,
        "date_parsed": parsed_date,
        "is_headline_missing": headline is None,
        "is_category_missing": category is None,
        "is_description_missing": description is None,
        "is_author_missing": authors is None,
        "is_date_invalid": parsed_date is None
    }

    batch.append(
        UpdateOne(
            {"_id": document["_id"]},
            {"$set": update_data}
        )
    )

    if len(batch) >= batch_size:
        result = articles.bulk_write(batch, ordered=False)
        processed += result.modified_count
        batch.clear()

        print("Processed:", processed)

# Process remaining documents
if batch:
    result = articles.bulk_write(batch, ordered=False)
    processed += result.modified_count

print("\nDATA CLEANING COMPLETED")
print("Documents updated:", processed)
print("Total documents:", total)
print("=" * 60)
