import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

model = pickle.load(open("model.pkl", "rb"))
names = pickle.load(open("names.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    features = [float(x) for x in request.form.values()]
    final_features = [np.array(features)]
    pred = model.predict(final_features)
    output = ("Não extinção do incêndio" if pred[0] == 0 else "Extinção do incêndio") 
    return render_template("index.html", prediction_text="Res: " + str(output))

@app.route("/api", methods=["POST"])
def results():
    data = request.get_json(force=True)
    pred = model.predict([np.array(list(data.values()))])
    output = ("Não extinção do incêndio" if pred[0] == 0 else "Extinção do incêndio")
    return jsonify(output)
