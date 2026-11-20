
from config import articles

# Total records
total = articles.count_documents({})

print("DATABASE:", "news_analytics_db")
print("COLLECTION:", "articles")
print("TOTAL NEWS ARTICLES:", total)

# Display first 5 documents
print("\nFIRST 5 NEWS ARTICLES:\n")

for article in articles.find().limit(5):
    print(article)
    print("-" * 60)

# Count categories
categories = articles.distinct("category")

print("\nTOTAL CATEGORIES:", len(categories))
print("CATEGORIES:", categories)

print("\nCLEANED DOCUMENT VERIFICATION")

sample = articles.find_one(
    {"headline_clean": {"$ne": None}}
)

print("Original headline:")
print(sample.get("headline"))

print("\nCleaned headline:")
print(sample.get("headline_clean"))

print("\nCleaned category:")
print(sample.get("category_clean"))

print("\nParsed date:")
print(sample.get("date_parsed"))