
import numpy as np
from flask import Flask, request, url_for, redirect, render_template, jsonify
import pandas as pd
import pickle
import babel.numbers
#from flask_cors import CORS
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
#CORS(app)

lm = LinearRegression()


@app.route('/', methods=['GET'])
def use_template():
    return render_template("index.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():

    job = request.form['1']
    edu = int(request.form['2'])
    experience = request.form['3']


    # creates dataframe from csv
    df = pd.read_csv('salarydata.csv')

    # renames columns
    df.rename(
        columns={'title': 'Job', 'basesalary': 'Salary', 'yearsofexperience': 'Experience', 'Education': 'Degree'},
        inplace=True)

    # drops null rows
    df.dropna(inplace=True)

    # creates new dataframe with only rows in the United States
    us = df[df['location'].apply(lambda x: x.count(',')) == 1]

    # creates new dataframe with salaries between 40k-250k
    # and only up to 20 years of experience
    full = us[(us['Salary'] >= 40000) & (us['Salary'] <= 250000) & (us['Experience'] <= 20) & (us['eduInt'] > 0)]

    select = full[full['Job'] == job].copy()
    select.drop('jobInt', axis=1, inplace=True)

    final = select[select['eduInt'] == edu].copy()
    final.drop('eduInt', axis=1, inplace=True)

    y = final['Salary']
    x = final[['Experience']]

    x_train, x_test, y_train, y_test = train_test_split(x.values, y, test_size=0.3, random_state=101)

    lm.fit(x_train, y_train)

    inn = [experience]
    ina = np.array(inn, dtype=float)

    sal = lm.predict(ina.reshape(1, -1))

    predictions = lm.predict(x_test)

    avgE = metrics.mean_absolute_error(y_test, predictions)

    low = sal[0] - (avgE / 2)
    high = sal[0] + (avgE / 2)

    salRange = str('Expected Salary Range: ' +
                   babel.numbers.format_currency(low, 'USD', locale='en_US') + ' - ' +
                   babel.numbers.format_currency(high, 'USD', locale='en_US'))

    return render_template('result.html', salRange=salRange)


if __name__ == '__main__':
    app.run(debug=True)
