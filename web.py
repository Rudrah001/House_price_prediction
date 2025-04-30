from flask import Flask, render_template, request
import joblib
import numpy as np

# import warnings
# from sklearn.exceptions import InconsistentVersionWarning

# warnings.simplefilter("ignore", InconsistentVersionWarning)

app = Flask(__name__)

model = joblib.load('price_predictor.joblib')

numerical_features = ["area", "bedrooms", "bathrooms", "stories", "parking"]
binary_features = {
    "mainroad": ["No", "Yes"],
    "guestroom": ["No", "Yes"],
    "basement": ["No", "Yes"],
    "hotwaterheating": ["No", "Yes"],
    "airconditioning": ["No", "Yes"],
    "prefarea": ["No", "Yes"]
}
furnishing_options = ["Unfurnished", "Semi-furnished", "Furnished"]

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html",
                           numerical_features=numerical_features,
                           binary_features=binary_features,
                           furnishing_options=furnishing_options)

@app.route('/predict', methods=["POST"])
def predict():
    try:
        input_data = []

        for feature in numerical_features:
            input_data.append(float(request.form[feature]))

        for feature in binary_features:
            input_data.append(1 if request.form[feature] == "Yes" else 0)

        status = request.form["furnishingstatus"]
        if status == "Unfurnished":
            input_data.append(0)
        elif status == "Semi-furnished":
            input_data.append(1)
        else:
            input_data.append(2)

        prediction = model.predict([input_data])[0]
        adjusted_price = prediction + 1000000
        price = f"₹ {int(adjusted_price):,}"

        # print("\n\n=== PREDICTION DEBUG OUTPUT ===")
        # print(f"Input Features: {input_data}")
        # print(f"Raw Prediction: {prediction}")
        # print(f"Formatted Price: {price}")
        # print(f"adjusted Price: {adjusted_price}")
        # print("=============================\n\n")

        return f"<h3>Estimated House Price</h3><p style='font-size: 24px; font-weight: bold;'>{price}</p>"

    except Exception as e:
        return f"<h3 style='color:red;'>Error</h3><p>Invalid input. Please enter correct values.</p>"

predict()

if __name__ == "__main__":
    app.run(debug=True)