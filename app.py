from flask import Flask, request, url_for, redirect, render_template
import pandas as pd
import pickle
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app = Flask(__name__)

model = pickle.load(open("salary_model.pkl", "rb"))


@app.route('/')
def use_template():
    return render_template("index.html")


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    input_one = request.form['1']
    input_two = request.form['2']
    input_three = request.form['3']

    setup_df = pd.DataFrame([pd.Series([input_one])])
    salary_prediction = model.pred(setup_df)
    output = salary_prediction
    return render_template(f'Predicted salary is {output}')


if __name__ == '__main__':
    app.run(debug=True)
