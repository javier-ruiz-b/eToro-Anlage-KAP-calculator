import pandas as pd
from locale import atof

usdToEurDf = pd.read_csv("BBEX3.D.USD.EUR.BB.AC.000.csv", sep=';', names=['date', 'value', 'comments'])

def findValidRowByDate(date):
    while True:
        rows = usdToEurDf.loc[usdToEurDf['date'] == date]
        if len(rows.index) == 1:
            return rows.iloc[0]

def usdToEur(date, valueInUSD):
    value = ''
    for i in range(0, 3):
        value = usdToEurDf.shift(i)[usdToEurDf['date'] == date].iloc[0]['value']
        if value == ".":
            continue
        break

    value = atof(value)
    return valueInUSD / value

def eurToUsd(date, valueInEUR):
    row = findValidRowByDate(date)
    value = row['value']
    value = atof(value)
    return valueInEUR * value
