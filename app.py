import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/entry", methods=['POST', 'GET'])
def entry_page():
    if request.form['page'] == 'mpa':
        return render_template("indexMPA.html")
    else:
        return render_template("indexGBM.html")
    
# @app.route("/predict", methods=["POST"])
# def predict():
#     float_features = [float(x) for x in request.form.values()]
#     float_features.remove(float_features[-1])
#     features = [np.array(float_features)]
#     if request.form['page'] == '0':
#         prediction = modelGBM.predict(features)
#         if prediction == 0:
#             return render_template("indexGBM.html", prediction_text = "permohonan pinjaman ditolak")
#     else:
#         prediction = modelMPA.predict(features)
#         if prediction == 0:
#             return render_template("indexMPA.html", prediction_text = "permohonan pinjaman ditolak")

@app.route("/predictgbm", methods=["POST"])
def predictgbm():
    modelGBM = pickle.load(open("modelGBM.pkl", "rb"))
    cat = []
    cat.append(request.form['Gender'])
    cat.append(request.form['Married'])
    cat.append(request.form['Education'])
    cat.append(request.form['Self_Employed'])
    cat.append(request.form['Credit_History'])
    if request.form['Dependents'] == 'nol':
        cat.append(1)
        cat.append(0)
        cat.append(0)
        cat.append(0)
    elif request.form['Dependents'] == 'satu':
        cat.append(0)
        cat.append(1)
        cat.append(0)
        cat.append(0)
    elif request.form['Dependents'] == 'dua':
        cat.append(0)
        cat.append(0)
        cat.append(1)
        cat.append(0)
    else:
        cat.append(0)
        cat.append(0)
        cat.append(0)
        cat.append(1)
    if request.form['Property_Area'] == 'rural':
        cat.append(1)
        cat.append(0)
        cat.append(0)
    elif request.form['Property_Area'] == 'semi':
        cat.append(0)
        cat.append(1)
        cat.append(0)
    else:
        cat.append(0)
        cat.append(0)
        cat.append(1)
    cat.append(request.form['ApplicantIncome'])
    cat.append(request.form['CoapplicantIncome'])
    cat.append(request.form['LoanAmount'])
    data=cat.copy()
    # float_features=[]
    # for i in range(len(data)):
        # float_features.append(float(data[i]))    
    float_features = [float(x) for x in data]
    features = [np.array(float_features)]
    # features = [np.array(cat)]
    prediction = modelGBM.predict(features)
    # return render_template("indexGBM.html", prediction_text = "{}".format(prediction))
    if prediction == 0:
        return render_template("indexGBM.html", prediction_text = "permohonan pinjaman ditolak")
    else:
        return render_template("indexGBM.html", prediction_text = "permohonan pinjaman diterima")

@app.route("/predictmpa", methods=["POST"])
def predictmpa():
    modelMPA = pickle.load(open("modelMPA.pkl", "rb"))
    cat = []
    # cat.append(request.form['Gender'])
    # cat.append(request.form['Married'])
    # cat.append(request.form['Education'])
    cat.append(request.form['Self_Employed'])
    cat.append(request.form['Credit_History'])
    if request.form['Dependents'] == 'satu':
        cat.append(1)
    else:
        cat.append(0)
    if request.form['Property_Area'] == 'rural':
        cat.append(1)
    else:
        cat.append(0)
    cat.append(request.form['ApplicantIncome'])
    cat.append(request.form['CoapplicantIncome'])
    cat.append(request.form['LoanAmount'])
    data=cat.copy()
    # float_features=[]
    # for i in range(len(data)):
        # float_features.append(float(data[i]))    
    float_features = [float(x) for x in data]
    features = [np.array(float_features)]
    # features = [np.array(cat)]
    prediction = modelMPA.predict(features)
    # return render_template("indexGBM.html", prediction_text = "{}".format(prediction))
    if prediction == 0:
        return render_template("indexMPA.html", prediction_text = "permohonan pinjaman ditolak")
    else:
        return render_template("indexMPA.html", prediction_text = "permohonan pinjaman diterima")
    
if __name__ == "__main__":
    app.run(debug=True)