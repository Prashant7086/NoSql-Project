
import streamlit as st
import pandas as pd
import pymongo
import altair as alt
from pathlib import Path
# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="News Analytics Dashboard",
    page_icon="📰",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "Model"

# ---------------------------------
# MONGODB CONNECTION
# ---------------------------------

@st.cache_resource
def connect_mongodb():
    client = pymongo.MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000
    )
    client.admin.command("ping")
    db = client["news_analytics_db"]
    return db["articles"]

try:
    articles = connect_mongodb()
    st.success("Connected to MongoDB successfully!")
except Exception as e:
    st.error(f"MongoDB connection failed: {e}")
    st.stop()

# ---------------------------------
# DASHBOARD HEADER
# ---------------------------------

st.title("📰 News Analytics Dashboard")
st.markdown(
    "### News Category Analysis & Machine Learning Performance"
)
st.divider()

# ---------------------------------
# DATABASE STATISTICS
# ---------------------------------

total_articles = articles.count_documents({})

categories = articles.distinct(
    "category_clean",
    {"category_clean": {"$exists": True, "$ne": None}}
)

total_categories = len(categories)

col1, col2, col3 = st.columns(3)

col1.metric("Total News Articles", f"{total_articles:,}")
col2.metric("Total Categories", total_categories)
col3.metric(
    "Average Articles per Category",
    f"{total_articles / total_categories:,.0f}"
    if total_categories else "0"
)

st.divider()

# ---------------------------------
# CATEGORY DISTRIBUTION
# ---------------------------------

st.subheader("1. News Category Distribution")

category_data = list(
    articles.aggregate([
        {
            "$match": {
                "category_clean": {
                    "$exists": True,
                    "$ne": None
                }
            }
        },
        {
            "$group": {
                "_id": "$category_clean",
                "total": {"$sum": 1}
            }
        },
        {"$sort": {"total": -1}}
    ])
)

category_df = pd.DataFrame(category_data)

if not category_df.empty:
    category_df.columns = ["Category", "Articles"]

    chart = alt.Chart(category_df).mark_bar().encode(
        x=alt.X("Articles:Q", title="Number of Articles"),
        y=alt.Y(
            "Category:N",
            sort="-x",
            title="News Category"
        ),
        tooltip=["Category", "Articles"]
    ).properties(height=650)

    st.altair_chart(chart, use_container_width=True)

# ---------------------------------
# TOP 10 CATEGORIES
# ---------------------------------

st.subheader("2. Top 10 News Categories")

if not category_df.empty:
    top10 = category_df.head(10)

    chart = alt.Chart(top10).mark_arc(
        innerRadius=65
    ).encode(
        theta=alt.Theta("Articles:Q"),
        color=alt.Color("Category:N"),
        tooltip=["Category", "Articles"]
    )

    st.altair_chart(chart, use_container_width=True)

# ---------------------------------
# MODEL PERFORMANCE
# ---------------------------------

st.divider()
st.subheader("3. Machine Learning Model Comparison")
comparison_path = MODEL_DIR / "model_comparison.csv"
if comparison_path.exists():
    model_df = pd.read_csv(comparison_path)
    st.dataframe(
        model_df.style.format({
            "accuracy": "{:.2%}",
            "precision": "{:.2%}",
            "recall": "{:.2%}",
            "f1_score": "{:.2%}"
        }),
        use_container_width=True
    )
    melted = model_df.melt(
        id_vars="model",
        value_vars=[
            "accuracy",
            "precision",
            "recall",
            "f1_score"
        ],
        var_name="Metric",
        value_name="Score"
    )

    performance_chart = alt.Chart(melted).mark_bar().encode(
        x=alt.X("Metric:N"),
        y=alt.Y("Score:Q", scale=alt.Scale(domain=[0, 1])),
        color="model:N",
        xOffset="model:N",
        tooltip=["model", "Metric", "Score"]
    ).properties(height=400)

    st.altair_chart(
        performance_chart,
        use_container_width=True
    )

    best_model = model_df.loc[
        model_df["accuracy"].idxmax()
    ]

    st.success(
        f"Best Performing Model: {best_model['model']} "
        f"({best_model['accuracy']:.2%} Accuracy)"
    )

else:
    st.warning("Model comparison CSV not found.")

# ---------------------------------
# CATEGORY DATA TABLE
# ---------------------------------

st.divider()
st.subheader("4. Complete Category Statistics")

if not category_df.empty:
    st.dataframe(
        category_df,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------
# FOOTER
# ---------------------------------

st.divider()

st.caption(
    "News Analytics & Classification System | "
    "MongoDB + PyMongo + Machine Learning + Streamlit"
)
