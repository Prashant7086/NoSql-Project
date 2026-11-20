
import streamlit as st
import joblib
from datetime import datetime
from pathlib import Path
from config import articles

# ---------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION
# ---------------------------------------

st.set_page_config(
    page_title="News Category Predictor",
    page_icon="📰",
    layout="wide"
)

# ---------------------------------------
# 2. PROJECT PATHS
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent

VECTORIZER_PATH = BASE_DIR / "Model" / "tfidf_vectorizer.pkl"
MODEL_PATH = BASE_DIR / "Model" / "logistic_regression_model.pkl"

# ---------------------------------------
# 3. LOAD TRAINED MODELS
# ---------------------------------------

@st.cache_resource
def load_models():

    vectorizer = joblib.load(VECTORIZER_PATH)
    model = joblib.load(MODEL_PATH)

    return vectorizer, model


try:
    vectorizer, model = load_models()
    models_loaded = True

except Exception as e:
    st.error(f"Error loading Machine Learning models: {e}")
    models_loaded = False

# ---------------------------------------
# 4. MONGODB CONNECTION
# ---------------------------------------

try:
    prediction_logs = articles.database["prediction_logs"]

    articles.database.command("ping")
    mongodb_connected = True

except Exception as e:
    prediction_logs = None
    mongodb_connected = False
    st.warning(f"MongoDB connection issue: {e}")

# ---------------------------------------
# 5. DASHBOARD HEADER
# ---------------------------------------

st.title("📰 News Category Prediction System")

st.write(
    "Predict the category of a news headline "
    "using Machine Learning, NLP and MongoDB."
)

st.divider()

# ---------------------------------------
# 6. SYSTEM STATUS
# ---------------------------------------

col1, col2 = st.columns(2)

with col1:
    if models_loaded:
        st.success("Machine Learning Model: Loaded")
    else:
        st.error("Machine Learning Model: Not Loaded")

with col2:
    if mongodb_connected:
        st.success("MongoDB: Connected")
    else:
        st.warning("MongoDB: Offline")

# ---------------------------------------
# 7. NEWS HEADLINE INPUT
# ---------------------------------------

st.subheader("Enter News Headline")

headline = st.text_area(
    "News Headline",
    placeholder="Example: Scientists discover a new technology...",
    height=120
)

# ---------------------------------------
# 8. PREDICTION FUNCTIONALITY
# ---------------------------------------

if st.button(
    "🔍 Predict News Category",
    type="primary",
    disabled=not models_loaded
):

    if not headline.strip():

        st.warning("Please enter a news headline.")

    else:

        try:

            # Convert headline into TF-IDF features
            transformed = vectorizer.transform(
                [headline.strip()]
            )

            # Predict news category
            prediction = model.predict(transformed)[0]

            # Calculate prediction probabilities
            probabilities = model.predict_proba(transformed)[0]

            confidence = float(max(probabilities)) * 100

            st.success("Prediction completed successfully!")

            # -----------------------------------
            # DISPLAY MAIN PREDICTION
            # -----------------------------------

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Predicted Category",
                    str(prediction)
                )

            with col2:
                st.metric(
                    "Prediction Confidence",
                    f"{confidence:.2f}%"
                )

            st.divider()

            # -----------------------------------
            # TOP 5 CATEGORIES
            # -----------------------------------

            st.subheader("📊 Top 5 Predicted Categories")

            top_indices = probabilities.argsort()[-5:][::-1]

            for index in top_indices:

                category = model.classes_[index]
                probability = probabilities[index] * 100

                st.write(
                    f"**{category}** — {probability:.2f}%"
                )

                st.progress(float(probability / 100))

            # -----------------------------------
            # SAVE PREDICTION IN MONGODB
            # -----------------------------------

            if mongodb_connected:

                prediction_logs.insert_one({

                    "headline": headline.strip(),

                    "predicted_category": str(prediction),

                    "confidence": confidence,

                    "model": "Logistic Regression",

                    "created_at": datetime.now()

                })

                st.success(
                    "Prediction history saved successfully in MongoDB!"
                )

            else:

                st.warning(
                    "Prediction completed, but history was not saved "
                    "because MongoDB is offline."
                )

        except Exception as e:

            st.error(f"Prediction error: {e}")

# ---------------------------------------
# 9. RECENT PREDICTION HISTORY
# ---------------------------------------

st.divider()

st.subheader("📚 Recent Prediction History")

if mongodb_connected:

    try:

        history = list(
            prediction_logs.find(
                {},
                {"_id": 0}
            ).sort("_id", -1).limit(10)
        )

        if history:

            st.dataframe(
                history,
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No prediction history available yet.")

    except Exception as e:

        st.error(f"Unable to retrieve prediction history: {e}")

else:

    st.info("Prediction history is unavailable because MongoDB is offline.")

# ---------------------------------------
# 10. FOOTER
# ---------------------------------------

st.divider()

st.caption(
    "News Category Prediction System | "
    "Python | Streamlit | Machine Learning | MongoDB"
)
