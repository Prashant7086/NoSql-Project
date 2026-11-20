
from config import articles

print("=" * 60)
print("MONGODB AGGREGATION ANALYSIS")
print("=" * 60)

# 1. Total articles by category
print("\n1. NEWS ARTICLES BY CATEGORY")

category_pipeline = [
    {
        "$match": {
            "category_clean": {
                "$nin": [None, ""]
            }
        }
    },
    {
        "$group": {
            "_id": "$category_clean",
            "total_articles": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "total_articles": -1
        }
    }
]

category_results = list(
    articles.aggregate(category_pipeline)
)

for item in category_results:
    print(item["_id"], ":", item["total_articles"])


# 2. Top 10 news categories
print("\n2. TOP 10 NEWS CATEGORIES")

for item in category_results[:10]:
    print(item["_id"], ":", item["total_articles"])


# 3. Articles published by year
print("\n3. ARTICLES PUBLISHED BY YEAR")

year_pipeline = [
    {
        "$match": {
            "date_parsed": {"$type": "date"}
        }
    },
    {
        "$group": {
            "_id": {"$year": "$date_parsed"},
            "total_articles": {"$sum": 1}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

year_results = list(
    articles.aggregate(year_pipeline)
)

for item in year_results:
    print(item["_id"], ":", item["total_articles"])


# 4. Articles with missing headlines
print("\n4. MISSING HEADLINE ANALYSIS")

missing_pipeline = [
    {
        "$match": {
            "is_headline_missing": True
        }
    },
    {
        "$count": "missing_headlines"
    }
]

missing_results = list(
    articles.aggregate(missing_pipeline)
)

missing_count = (
    missing_results[0]["missing_headlines"]
    if missing_results else 0
)

print("Missing headlines:", missing_count)


# 5. Top 10 authors by article count
print("\n5. TOP 10 AUTHORS")

author_pipeline = [
    {
        "$match": {
            "authors_clean": {
                "$nin": [None, ""]
            }
        }
    },
    {
        "$group": {
            "_id": "$authors_clean",
            "total_articles": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "total_articles": -1
        }
    },
    {
        "$limit": 10
    }
]

author_results = list(
    articles.aggregate(author_pipeline)
)

for item in author_results:
    print(item["_id"], ":", item["total_articles"])


# 6. Final database statistics
print("\n6. FINAL DATABASE STATISTICS")

print("Total articles:", articles.count_documents({}))
print("Total categories:", len(articles.distinct("category_clean")))

print("\nAGGREGATION ANALYSIS COMPLETED")
print("=" * 60)
