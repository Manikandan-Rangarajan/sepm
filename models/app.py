import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from scraper import scrape_reviews
from http import HTTPStatus

app = Flask(__name__)
CORS(app)

# Load models
def load_models(model_path='sentiment_model1.pkl', vectorizer_path='vectorizer1.pkl'):
    try:
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            print("Error: Model or vectorizer files not found.")
            return None, None
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        print("Models loaded successfully.")
        return model, vectorizer
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None

MODEL, VECTORIZER = load_models()

# Helper: Validate URL
def validate_url(url):
    return isinstance(url, str) and url.startswith(('http://', 'https://'))

# API: Predict Sentiment
@app.route('/predict', methods=['POST'])
def scrape_and_analyze():
    if not MODEL or not VECTORIZER:
        print("Models not available.")
        return jsonify({"error": "Models not available"}), HTTPStatus.SERVICE_UNAVAILABLE

    data = request.get_json()
    product_url = data.get('url')

    if not product_url or not validate_url(product_url):
        print("Invalid or missing URL.")
        return jsonify({"error": "Invalid or missing URL"}), HTTPStatus.BAD_REQUEST

    try:
        start_time = time.time()
        print(f"Scraping reviews from URL: {product_url}")
        reviews_data = scrape_reviews(product_url, "span[data-hook='review-body']", 'i[data-hook="review-star-rating"]')

        if 'error' in reviews_data:
            print(f"Scraping error: {reviews_data['error']}")
            return jsonify(reviews_data), HTTPStatus.BAD_REQUEST

        reviews = reviews_data.get('reviews', [])
        if not reviews:
            print("No reviews found.")
            return jsonify({"error": "No reviews found"}), HTTPStatus.NOT_FOUND

        # Predict Sentiments
        vectorized_reviews = VECTORIZER.transform(reviews)
        raw_predictions = MODEL.predict(vectorized_reviews)
        
        # Map integer predictions to string labels
        sentiment_map = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
        predictions = [sentiment_map.get(pred, 'Unknown') for pred in raw_predictions]
        
        # Debug: Print predictions to verify
        print(f"Raw predictions: {list(raw_predictions)}")
        print(f"Mapped predictions: {predictions}")

        sentiment_counts = {
            "Positive": sum(pred == 'Positive' for pred in predictions),
            "Negative": sum(pred == 'Negative' for pred in predictions),
            "Neutral": sum(pred == 'Neutral' for pred in predictions)
        }

        processing_time = round(time.time() - start_time, 2)
        print(f"Sentiment analysis completed in {processing_time} seconds.")
        return jsonify({
            "sentiment_counts": sentiment_counts,
            "total_reviews": len(reviews),
            "processing_time": processing_time
        })
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR

# API: Health Check
@app.route('/health', methods=['GET'])
def health_check():
    status = "healthy" if MODEL and VECTORIZER else "unhealthy"
    print(f"Health check: {status}")
    return jsonify({
        "status": status,
        "model_loaded": bool(MODEL),
        "vectorizer_loaded": bool(VECTORIZER)
    }), HTTPStatus.OK

if __name__ == '__main__':
    print("Starting Flask server on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
