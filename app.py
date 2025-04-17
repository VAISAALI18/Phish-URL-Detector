from flask import Flask, render_template, request
import pickle
from FeatureExtraction import FeatureExtraction

app = Flask(__name__)

# Load the trained model
try:
    with open('pickle/model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    model = None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    confidence = None
    error = None

    if request.method == 'POST':
        url = request.form['url']
        if url.strip():
            try:
                extractor = FeatureExtraction(url)
                features = extractor.getFeaturesList()

                if model:
                    prediction = model.predict([features])[0]
                    proba = model.predict_proba([features])[0]
                    confidence = round(max(proba) * 100, 2)

                    result = "Legitimate ✅" if prediction == 1 else "Phishing ⚠️"
                else:
                    error = "Model could not be loaded."
            except Exception as e:
                error = f"Error during prediction: {e}"
        else:
            error = "Please enter a valid URL."

    return render_template('index.html', result=result, confidence=confidence, error=error)

if __name__ == '__main__':
    app.run(debug=True)
