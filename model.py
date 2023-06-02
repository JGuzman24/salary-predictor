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
    return job

def setJob(jobs):
    global select
    select = full[full['Job'] == jobs].copy()
    select.drop('jobInt', axis=1, inplace=True)


def getEdu(deg):
    global final

    if deg == 1:
        return "BS"
    elif deg == 2:
        return "MS"
    elif deg == 3:
        return "PhD"

def setEdu(edu):
    global final
    final = select[select['eduInt'] == edu].copy()
    final.drop('eduInt', axis=1, inplace=True)


def getExp():
    runModel()
    print("Please enter Experience between 0-20")

    xp = input()
    return xp


def predict(model, experience):
    inn = [experience]
    ina = np.array(inn, dtype=float)

    sal = model.predict(ina.reshape(1, -1))
    """predictions = model.predict(x_test)

    avgE = metrics.mean_absolute_error(y_test, predictions)
    low = sal[0] - (avgE / 2)
    high = sal[0] + (avgE / 2)

    # print('Expected Salary: ' + babel.numbers.format_currency(sal[0], 'USD', locale='en_US'))
    # print('Average error: ' + babel.numbers.format_currency(avgE, 'USD', locale='en_US'))
    # print()"""

    salRange = str('Approved Salary Range: ' +
          babel.numbers.format_currency(low, 'USD', locale='en_US') + ' - ' +
          babel.numbers.format_currency(high, 'USD', locale='en_US'))
    return salRange


def runModel():
    global final
    global y
    global x
    global lm
    global x_train
    global x_test
    global y_train
    global y_test
    if final.empty:
        return
    y = final['Salary']
    x = final[['Experience']]

    x_train, x_test, y_train, y_test = train_test_split(x.values, y, test_size=0.3, random_state=101)

    lm.fit(x_train, y_train)

    return lm




def saveModels():
    for j in jobs:
        for i in range(3):
            startFresh()
            setJob(j)
            setEdu(i+1)
            m = runModel()
            print(f"i is{i}")
            filename = str(j+'+'+getEdu(i+1))
            print(filename)
            pickle.dump(m, open(f'models/{filename}.pkl', "wb"))





def startFresh():
    global full
    global degree
    global select
    global final
    global x
    global y
    global lm
    global exp
    global x_train
    global x_test
    global y_train
    global y_test
    global Experience


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
Experience = 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startFresh()

    jobs = full['Job'].unique()
    edus = full['Degree'].unique()

    for j in jobs:
        print(j)


    job = getJob()
    edu = getEdu(1)
    filepath = str(job+'+'+edu)

    ml = pickle.load(open(f"models/{filepath}.pkl", "rb"))

    print(predict(ml, getExp()))

    # runModel()
    # output = predict(xp)

    # print(output)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
