
from pymongo import MongoClient

# MongoDB connection URL
MONGO_URI = "mongodb://localhost:27017/"

# Connect to MongoDB
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# Verify connection
try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

    # Create/select database
    db = client["news_analytics_db"]

    # Create/select collection
    articles = db["articles"]

    print("Database:", db.name)
    print("Collection:", articles.name)

except Exception as e:
    print("MongoDB connection failed:", e)
    raise
