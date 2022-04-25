import pandas as pd
import locale
from locale import atof
from exchange_rate import usdToEur, calculateRowsInEur, calculateRowsInUsd
from date import parseDate

COL_OPEN = "Eröffnet"
COL_CLOSED = "Geschlossen"
COL_INSTRUMENT = "Instrument"
COL_TYPE = "Type"
COL_UNITS = "Anteile"
COL_OPEN_RATE = "Öffnungskurs"
COL_CLOSE_RATE = "Schlusskurs"
COL_CLOSE_CURRENCY = "Schlusskurs-Währung"
COL_PROFIT_USD = "Profit-USD"
COL_PROFIT_EUR = "Profit-EUR"
COL_INVERTING_AMOUNT = "Invest. Betrag"
COL_PROFIT_EXCHANGE_RATE = "W-Kurs G/V"
COL_DIVIDENDS_USD = "Dividenden-USD"
COL_DIVIDENDS_EUR = "Dividenden-EUR"
COL_FEES_USD = "Gebühren-USD"
COL_FEES_EUR = "Gebühren-EUR"
COL_REVENUE_USD = "Ertrag-USD"
COL_REVENUE_EUR = "Ertrag-EUR"
COL_ISIN = "ISIN"

def calcDetailedTable(accountActivityDf, closedPositionsDf):
    resultColumns = [COL_OPEN, COL_CLOSED, COL_INSTRUMENT, COL_TYPE, COL_UNITS, COL_OPEN_RATE, COL_CLOSE_RATE, COL_CLOSE_CURRENCY, 
                    COL_PROFIT_USD, COL_PROFIT_EUR, COL_INVERTING_AMOUNT, COL_PROFIT_EXCHANGE_RATE, COL_DIVIDENDS_USD,
                    COL_DIVIDENDS_EUR, COL_FEES_USD, COL_FEES_EUR, COL_REVENUE_USD, COL_REVENUE_EUR, COL_ISIN]
    resultTable = pd.DataFrame(columns=resultColumns, index=closedPositionsDf.index)
    for index, row in closedPositionsDf.iterrows():
        positionId = row['Position ID']
        currency = findCurrencyOfPositionId(accountActivityDf, positionId)
        openDate = parseDate(row['Open Date'])
        closeDate = parseDate(row['Close Date'])
        profitUSD = parseFloat(row['Profit'])
        profitEUR = usdToEur(closeDate, profitUSD)

        amountUSD = parseFloat(row['Amount'])
        amountBeginEUR = usdToEur(openDate, amountUSD)
        amountEndEUR = usdToEur(closeDate, amountUSD)

        wKursGW = amountEndEUR - amountBeginEUR

        dividendRows = dividendRowsOfPosition(accountActivityDf, positionId)
        dividendsUSD = calculateRowsInUsd(dividendRows)
        dividendsEUR = calculateRowsInEur(dividendRows)

        feeRows = feeRowsOfPosition(accountActivityDf, positionId)
        feesUSD = calculateRowsInUsd(feeRows)
        feesEUR = calculateRowsInEur(feeRows)

        revenueEUR = profitEUR + wKursGW + dividendsEUR + feesEUR
        revenueUSD = profitUSD + dividendsUSD + feesUSD

        result = {}
        result[COL_OPEN] = row['Open Date']
        result[COL_CLOSED] = row['Close Date']
        result[COL_INSTRUMENT] = row['Action']
        result[COL_TYPE] = row['Type']
        result[COL_UNITS] = row['Units']
        result[COL_OPEN_RATE] = row['Open Rate']
        result[COL_CLOSE_RATE] = row['Close Rate']
        result[COL_CLOSE_CURRENCY] = currency
        result[COL_PROFIT_USD] = profitUSD
        result[COL_PROFIT_EUR] = profitEUR + wKursGW
        result[COL_INVERTING_AMOUNT] = findInvertingAmountOfPositionId(accountActivityDf, positionId)
        result[COL_PROFIT_EXCHANGE_RATE] = wKursGW
        result[COL_DIVIDENDS_USD] = dividendsUSD
        result[COL_DIVIDENDS_EUR] = dividendsEUR
        result[COL_FEES_USD] = feesUSD
        result[COL_FEES_EUR] = feesEUR
        result[COL_REVENUE_USD] = revenueUSD
        result[COL_REVENUE_EUR] = revenueEUR
        result[COL_ISIN] = row['ISIN']

        resultTable.iloc[index] = result

    return resultTable

    
def dividendRowsOfPosition(accountActivityDf, positionId):
    rows = rowsOfPosition(accountActivityDf, positionId)
    dividendRows = rows[rows['Type'].str.contains("(?i)dividend$")]
    return dividendRows

def feeRowsOfPosition(accountActivityDf, positionId):
    rows = rowsOfPosition(accountActivityDf, positionId)
    return rows[rows['Type'].str.contains("(?i) fee$")]

def parseFloat(value):
    if isinstance(value, float):
        return value
    return atof(value)

def rowsOfPosition(accountActivityDf, positionId):
    return accountActivityDf.loc[(accountActivityDf['Position ID'] == positionId)]

def findCurrencyOfPositionId(accountActivityDf, positionId):
    details = accountActivityDf.loc[accountActivityDf['Position ID'] == positionId].iloc[0]['Details']
    currency = details.split('/')[1]
    return currency

def findInvertingAmountOfPositionId(accountActivityDf, positionId):
    row = accountActivityDf.loc[(accountActivityDf['Position ID'] == positionId) & (accountActivityDf['Type'] == "Open Position")]
    if len(row) != 1:
        print("Warning: Could not find the inverting amount of position ID " + str(positionId))
        return ""


    value = row.iloc[0]['Amount']
    return locale.str(value)

def float2str(value):
    return locale.str(round(value, 2))
    
