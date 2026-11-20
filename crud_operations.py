
from config import articles
from datetime import datetime
import uuid

print("=" * 60)
print("MONGODB CRUD OPERATIONS")
print("=" * 60)

# Unique ID for our test document
test_id = str(uuid.uuid4())

# -------------------------------------------------
# 1. CREATE OPERATION
# -------------------------------------------------

print("\n1. CREATE OPERATION")

test_article = {
    "project_test_id": test_id,
    "headline": "Artificial Intelligence Transforming Technology",
    "category": "TECH",
    "authors": "Project Test",
    "short_description": "This is a test document for MongoDB CRUD operations.",
    "date": "2026-11-03",
    "created_at": datetime.now()
}

result = articles.insert_one(test_article)

print("Document inserted successfully!")
print("Inserted ID:", result.inserted_id)


# -------------------------------------------------
# 2. READ OPERATION
# -------------------------------------------------

print("\n2. READ OPERATION")

record = articles.find_one({
    "project_test_id": test_id
})

if record:
    print("Document retrieved successfully!")
    print("Headline:", record["headline"])
    print("Category:", record["category"])
else:
    print("Document not found!")


# -------------------------------------------------
# 3. UPDATE OPERATION
# -------------------------------------------------

print("\n3. UPDATE OPERATION")

update_result = articles.update_one(
    {"project_test_id": test_id},
    {
        "$set": {
            "category": "ARTIFICIAL INTELLIGENCE",
            "headline": "AI Transforming the Future"
        }
    }
)

print("Matched documents:", update_result.matched_count)
print("Modified documents:", update_result.modified_count)

updated_record = articles.find_one({
    "project_test_id": test_id
})

print("Updated headline:", updated_record["headline"])
print("Updated category:", updated_record["category"])


# -------------------------------------------------
# 4. DELETE OPERATION
# -------------------------------------------------

print("\n4. DELETE OPERATION")

delete_result = articles.delete_one({
    "project_test_id": test_id
})

print("Documents deleted:", delete_result.deleted_count)

# Verify deletion
check = articles.find_one({
    "project_test_id": test_id
})

if check is None:
    print("Test document deleted successfully!")
else:
    print("Test document still exists!")


# -------------------------------------------------
# FINAL SUMMARY
# -------------------------------------------------

print("\nCRUD OPERATIONS COMPLETED")
print("=" * 60)
