
from config import articles

print("=" * 60)
print("DUPLICATE NEWS ARTICLE ANALYSIS")
print("=" * 60)

# Find duplicate article links
pipeline = [
    {
        "$match": {
            "link_clean": {
                "$exists": True,
                "$nin": [None, ""]
            }
        }
    },
    {
        "$group": {
            "_id": "$link_clean",
            "count": {"$sum": 1}
        }
    },
    {
        "$match": {
            "count": {"$gt": 1}
        }
    }
]

duplicates = list(
    articles.aggregate(pipeline, allowDiskUse=True)
)

# Calculate statistics
duplicate_groups = len(duplicates)

extra_documents = sum(
    item["count"] - 1
    for item in duplicates
)

print("\nTotal duplicate link groups:", duplicate_groups)
print("Extra duplicate documents:", extra_documents)

print("\nTOP 10 DUPLICATE LINKS")

for item in duplicates[:10]:
    print("\nLink:", item["_id"])
    print("Occurrences:", item["count"])

print("\nDUPLICATE ANALYSIS COMPLETED")
print("=" * 60)
