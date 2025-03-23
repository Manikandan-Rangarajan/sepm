# flask-api/app.py
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('sentiment_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json.get('text', '')
    prediction = model.predict([data])[0]
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(port=5001)
