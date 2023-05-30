# This is a sample Python script.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import babel.numbers
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pickle

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def getJob():
    global select

    for j in jobs:
        print(j)
    print("Please enter job from above list")
    job = str(input())
    select = full[full['Job'] == job].copy()
    select.drop('jobInt', axis=1, inplace=True)
    getEdu()


def getEdu():
    global final

    print(select)

    print("Please enter degree: ")
    deg = int(input())

    final = select[select['eduInt'] == deg].copy()
    final.drop('eduInt', axis=1, inplace=True)
    getExp()


def getExp():
    runModel()
    print("Please enter Experience between 0-20")

    xp = input()
    inn = [xp]
    ina = np.array(inn, dtype=float)

    sal = lm.predict(ina.reshape(1, -1))
    avgE = metrics.mean_absolute_error(y_test, predictions)
    low = sal[0] - (avgE / 2)
    high = sal[0] + (avgE / 2)

    print('Expected Salary: ' + babel.numbers.format_currency(sal[0], 'USD', locale='en_US'))
    print('Average error: ' + babel.numbers.format_currency(avgE, 'USD', locale='en_US'))
    print()

    print('Approved Salary Range: ' +
          babel.numbers.format_currency(low, 'USD', locale='en_US') + ' - ' +
          babel.numbers.format_currency(high, 'USD', locale='en_US'))


def runModel():
    global final
    global y
    global x
    global lm
    global predictions
    global x_train
    global x_test
    global y_train
    global y_test
    y = final['Salary']
    x = final[['Experience']]

    x_train, x_test, y_train, y_test = train_test_split(x.values, y, test_size=0.3, random_state=101)

    lm.fit(x_train, y_train)
    predictions = lm.predict(x_test)

    pickle.dump(lm, open('salary_model.pkl', "wb"))


def showPlots(plots=False):
    if plots:
        sns.lmplot(x='Experience', y='Salary', data=final)
        sns.pairplot(final)
        sns.jointplot(x='Experience', y='Salary', data=final, kind='hex')


degree = ["Bachelor's Degree", "Master's Degree", 'PhD']
select = pd.DataFrame()
final = pd.DataFrame()
x = 0
y = 0
lm = LinearRegression()
exp = 0
x_train = []
x_test = []
y_train = []
y_test = []
predictions = []
Experience = 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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
    full = us[(us['Salary'] >= 40000) & (us['Salary'] <= 250000) & (us['Experience'] <= 20)]

    jobs = full['Job'].unique()

    getJob()
    runModel()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/