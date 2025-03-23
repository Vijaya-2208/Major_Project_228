import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import joblib

data = pd.read_csv("website_data.csv")

X = data["Content"]
y = data["Category"]

vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vectorized = vectorizer.fit_transform(X)

model = SVC(probability=True)
model.fit(X_vectorized, y)

# Save model and vectorizer
joblib.dump(model, "website_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Model trained and saved.")
