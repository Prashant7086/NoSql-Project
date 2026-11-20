# 📰 MongoDB-Powered News Category Prediction System

## 📌 Project Overview

The **News Category Prediction System** is a Machine Learning-based application that automatically predicts the category of a news headline using Natural Language Processing (NLP).

The project uses **TF-IDF Vectorization** for text feature extraction and **Logistic Regression** for news classification. MongoDB is integrated to store prediction history, including news headlines, predicted categories, confidence scores, and timestamps.

The application provides an interactive dashboard developed using Streamlit.

## 🎯 Project Objectives

- Automatically classify news headlines into appropriate categories.
- Apply Natural Language Processing techniques for text processing.
- Implement Logistic Regression for news classification.
- Use TF-IDF to convert textual data into numerical features.
- Integrate MongoDB for storing prediction history.
- Display prediction confidence and top five possible categories.
- Provide an interactive dashboard for users.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard |
| MongoDB | NoSQL database |
| PyMongo | MongoDB connectivity |
| Scikit-learn | Machine Learning |
| TF-IDF | Text feature extraction |
| Logistic Regression | News classification |
| Joblib | Saving and loading trained models |
| Pandas | Data manipulation |

## ⚙️ Project Architecture

1. User enters a news headline.
2. TF-IDF converts the headline into numerical features.
3. Logistic Regression predicts the news category.
4. The system calculates prediction confidence.
5. The top five possible categories are displayed.
6. Prediction details are saved in MongoDB.
7. Recent prediction history is displayed on the dashboard.

## 📂 Project Structure

```text
NoSql Project/
│
├── Model/
│   ├── tfidf_vectorizer.pkl
│   └── logistic_regression_model.pkl
│
├── Visualisation/
│   └── analytics_dashboard.py
│
├── config.py
├── predict_news.py
├── requirements.txt
└── README.md
```

*Note: Update the structure if your actual project contains additional folders or files.*

## 📦 Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Alternatively, download the project and open its folder in VS Code.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the main packages:

```bash
pip install streamlit pymongo pandas numpy scikit-learn joblib
```

### 5. Configure MongoDB

Make sure MongoDB is running and configure your MongoDB connection in `config.py`.

The application uses:

- Database: `news_analytics_db`
- Collection: `articles`
- Prediction History Collection: `prediction_logs`

### 6. Run the Application

Execute the following command in the VS Code terminal:

```bash
python -m streamlit run Visualisation/analytics_dashboard.py
```

The dashboard will open in your browser.

## 🧠 Machine Learning Model

**Algorithm:** Logistic Regression

**Feature Extraction:** TF-IDF Vectorization

The trained model uses the following files:

- `tfidf_vectorizer.pkl`: Converts news headlines into numerical features.
- `logistic_regression_model.pkl`: Predicts the news category.

### Prediction Process

The user enters a news headline, which is transformed using the trained TF-IDF vectorizer. The Logistic Regression model processes the transformed data and predicts its category.

The system also calculates prediction probabilities and displays the five highest-probability categories.

## 🗄️ MongoDB Integration

MongoDB is used to maintain prediction history.

Each prediction record contains:

| Field | Description |
|---|---|
| headline | User-entered news headline |
| predicted_category | Predicted news category |
| confidence | Prediction confidence percentage |
| model | Machine Learning algorithm used |
| created_at | Date and time of prediction |

### Example MongoDB Document

```json
{
  "headline": "Scientists discover a new technology",
  "predicted_category": "Technology",
  "confidence": 92.45,
  "model": "Logistic Regression",
  "created_at": "2026-11-05T13:30:00"
}
```

*The values above are illustrative.*

## 📊 Application Features

1. **Headline Input:** Users can enter any news headline.
2. **Category Prediction:** Predicts the category using Logistic Regression.
3. **Confidence Score:** Displays the highest prediction probability.
4. **Top 5 Categories:** Shows five possible categories with their probabilities.
5. **MongoDB Storage:** Automatically saves prediction records.
6. **Prediction History:** Displays the latest ten predictions.

## 🔍 Example Prediction

**Input:**

```text
India wins the international cricket championship.
```

**Illustrative Output:**

```text
Predicted Category: Sports
Prediction Confidence: 94.25%

Prediction History: Saved Successfully
```

Actual predictions and confidence scores depend on the trained model.

## ⚠️ Limitations

- Prediction accuracy depends on the quality of the training dataset.
- The model may not correctly classify complex or ambiguous headlines.
- Prediction confidence is not a guarantee of correctness.
- The system classifies news categories; it does not detect fake news or verify factual accuracy.

## 🚀 Future Enhancements

- Integrate advanced NLP models such as BERT.
- Add more news categories.
- Improve prediction accuracy through model optimization.
- Develop a complete prediction analytics dashboard.
- Add user authentication.
- Implement real-time news collection and classification.
- Add visual reports showing category-wise prediction trends.

## 👨‍💻 Project Information

**Project Name:** MongoDB-Powered News Category Prediction System

**Domain:** NoSQL Database and Machine Learning

**Machine Learning Algorithm:** Logistic Regression

**Database:** MongoDB

**Frontend:** Streamlit

## 📝 Conclusion

This project demonstrates the integration of Machine Learning, Natural Language Processing, and NoSQL database technology to develop an automated news category prediction system.

By combining TF-IDF, Logistic Regression, Streamlit, and MongoDB, the application provides an interactive platform for classifying news headlines and maintaining prediction history.