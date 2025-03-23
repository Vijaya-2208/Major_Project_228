from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import joblib
import re

app = Flask(__name__)
CORS(app)

# Load ML model and TF-IDF vectorizer
model = joblib.load("website_model.pkl")  # Pre-trained classifier
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Extract main text from a webpage
def scrape_website_text(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")
        for script in soup(["script", "style"]):  # Remove JS/CSS
            script.decompose()
        text = " ".join(soup.stripped_strings)
        return text
    except Exception as e:
        return None

@app.route("/categorize", methods=["POST"])
def categorize():
    data = request.json
    url = data.get("url", "")
    if not url.startswith("http"):
        url = "https://" + url

    raw_text = scrape_website_text(url)
    if not raw_text:
        return jsonify({"error": "Could not extract content."}), 400

    # Predict
    X = vectorizer.transform([raw_text])
    category = model.predict(X)[0]
    top_words = get_top_keywords(raw_text)

    return jsonify({
        "url": url,
        "category": category,
        "top_keywords": top_words
    })

def get_top_keywords(text):
    words = re.findall(r"\b[a-z]{4,}\b", text.lower())
    keywords = {}
    for word in words:
        if word in vectorizer.vocabulary_:
            keywords[word] = keywords.get(word, 0) + 1
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, count in sorted_keywords[:10]]  # Top 10 keywords

if __name__ == "__main__":
    app.run(debug=True)
