import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import mysql.connector
# Create flask app
flask_app = Flask(__name__,template_folder='template')
model = pickle.load(open("model.pkl", "rb"))

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shuvam1234@A",
    database="crop"
)
@flask_app.route("/")
def Home():
    return render_template("crop.html")

@flask_app.route("/predict", methods=["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)[0]

    # Save to DB
    cursor = db.cursor()
    sql = "INSERT INTO crop_predictions (Nitrogen, Phosphorus, Potassium, temperature, humidity, pH, rainfall, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (*float_features, prediction)
    cursor.execute(sql, values)
    db.commit()

    return render_template("crop.html", prediction_text=f"The Predicted Crop is {prediction}")


@flask_app.route('/report')
def report():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM crop_predictions ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    return render_template('report.html', reports=rows)


if __name__ == "__main__":
    flask_app.run(debug=True)