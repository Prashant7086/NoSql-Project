
import os
import json
import joblib
import pandas as pd

from config import articles

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

print("=" * 65)
print("NEWS CATEGORY PREDICTION - MACHINE LEARNING")
print("=" * 65)

# ------------------------------------------------
# STEP 1: FETCH DATA FROM MONGODB
# ------------------------------------------------

print("\nSTEP 1: FETCHING DATA FROM MONGODB")
cursor = articles.find(
    {
        "headline_clean": {"$type": "string", "$ne": ""},
        "category_clean": {"$type": "string", "$ne": ""}
    },
    {
        "_id": 0,
        "headline_clean": 1,
        "category_clean": 1
    }
)
df = pd.DataFrame(list(cursor))
print("Available records:", len(df))
# Remove missing values and duplicates
df.dropna(inplace=True)
df.drop_duplicates(
    subset=["headline_clean"],
    inplace=True
)
df = df[
    (df["headline_clean"].str.strip() != "") &
    (df["category_clean"].str.strip() != "")
]

print("Clean records:", len(df))
print("News categories:", df["category_clean"].nunique())

# ------------------------------------------------
# STEP 2: PREPARE DATA
# ------------------------------------------------

print("\nSTEP 2: PREPARING DATA")

X = df["headline_clean"].astype(str)
y = df["category_clean"].astype(str)

# Select stratified sample for manageable training

if len(df) > 60000:

    X, _, y, _ = train_test_split(
        X,
        y,
        train_size=60000,
        stratify=y,
        random_state=42
    )

print("Records selected for training:", len(X))

# Split into training and testing data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# ------------------------------------------------
# STEP 3: TEXT VECTORIZATION
# ------------------------------------------------

print("\nSTEP 3: TF-IDF VECTORIZATION")

vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 2),
    min_df=2,
    stop_words="english"
)

X_train_vectorized = vectorizer.fit_transform(X_train)

X_test_vectorized = vectorizer.transform(X_test)

print("TF-IDF training shape:", X_train_vectorized.shape)
print("TF-IDF testing shape:", X_test_vectorized.shape)

# ------------------------------------------------
# STEP 4: MULTINOMIAL NAIVE BAYES
# ------------------------------------------------

print("\nSTEP 4: MULTINOMIAL NAIVE BAYES")

nb_model = MultinomialNB()

nb_model.fit(
    X_train_vectorized,
    y_train
)

nb_predictions = nb_model.predict(
    X_test_vectorized
)

# ------------------------------------------------
# STEP 5: LOGISTIC REGRESSION
# ------------------------------------------------

print("\nSTEP 5: LOGISTIC REGRESSION")

lr_model = LogisticRegression(
    max_iter=200,
    solver="lbfgs",
    n_jobs=-1
)

lr_model.fit(
    X_train_vectorized,
    y_train
)

lr_predictions = lr_model.predict(
    X_test_vectorized
)

# ------------------------------------------------
# STEP 6: MODEL EVALUATION
# ------------------------------------------------
def evaluate_model(name, actual, predicted):
    accuracy = accuracy_score(actual, predicted)
    precision = precision_score(
        actual,
        predicted,
        average="weighted",
        zero_division=0
    )
    recall = recall_score(
        actual,
        predicted,
        average="weighted",
        zero_division=0
    )
    f1 = f1_score(
        actual,
        predicted,
        average="weighted",
        zero_division=0
    )

    print("\n", name)
    print("-" * 50)
    print("Accuracy:", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1 Score:", round(f1, 4))
    print("\nClassification Report:")
    print(
        classification_report(
            actual,
            predicted,
            zero_division=0
        )
    )

    return {
        "model": name,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }


nb_results = evaluate_model(
    "Multinomial Naive Bayes",
    y_test,
    nb_predictions
)

lr_results = evaluate_model(
    "Logistic Regression",
    y_test,
    lr_predictions
)

# ------------------------------------------------
# STEP 7: COMPARE MODELS
# ------------------------------------------------

print("\nSTEP 7: MODEL COMPARISON")

results = [nb_results, lr_results]
comparison = pd.DataFrame(results)
print(comparison.to_string(index=False))
best_model = max(
    results,
    key=lambda x: x["f1_score"]
)

print("\nBEST PERFORMING MODEL:", best_model["model"])

# ------------------------------------------------
# STEP 8: SAVE MODELS
# ------------------------------------------------

os.makedirs("Model", exist_ok=True)

joblib.dump(
    vectorizer,
    "Model/tfidf_vectorizer.pkl"
)
joblib.dump(
    nb_model,
    "Model/naive_bayes_model.pkl"
)
joblib.dump(
    lr_model,
    "Model/logistic_regression_model.pkl"
)
# Save evaluation results
with open("Model/model_results.json", "w") as file:
    json.dump(
        results,
        file,
        indent=4
    )

comparison.to_csv(
    "Model/model_comparison.csv",
    index=False
)

# ------------------------------------------------
# STEP 9: SAVE TEST PREDICTIONS
# ------------------------------------------------
print("\nSTEP 9: SAVING TEST PREDICTIONS")
prediction_data = pd.DataFrame({
    "headline": X_test.to_numpy(),
    "actual_category": y_test.to_numpy(),
    "naive_bayes_prediction": nb_predictions,
    "logistic_regression_prediction": lr_predictions
})

prediction_data.to_csv(
    "Model/test_predictions.csv",
    index=False
)

print("Test predictions saved successfully!")

print(
    "Total test records:",
    len(prediction_data)
)

# ------------------------------------------------
# STEP 10: SAVE CLASSIFICATION REPORTS
# ------------------------------------------------
print("\nSTEP 10: SAVING CLASSIFICATION REPORTS")

nb_report = classification_report(
    y_test,
    nb_predictions,
    zero_division=0,
    output_dict=True
)
lr_report = classification_report(
    y_test,
    lr_predictions,
    zero_division=0,
    output_dict=True
)
with open("Model/classification_reports.json", "w") as file:

    json.dump(
        {
            "Multinomial Naive Bayes": nb_report,
            "Logistic Regression": lr_report
        },
        file,
        indent=4
    )

print("Classification reports saved successfully!")

# ------------------------------------------------
# FINAL OUTPUT
# ------------------------------------------------

print("\nALL FILES SAVED SUCCESSFULLY")

print("\nGenerated Files:")

print("1. tfidf_vectorizer.pkl")
print("2. naive_bayes_model.pkl")
print("3. logistic_regression_model.pkl")
print("4. model_results.json")
print("5. model_comparison.csv")
print("6. test_predictions.csv")
print("7. classification_reports.json")

print("\nMACHINE LEARNING COMPLETED")

print("=" * 65)
