import pandas as pd
import locale
from locale import atof
from exchange_rate import usdToEur, eurToUsd

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

TYPE_STOCK = "Aktien"
TYPE_CFD = "CFD"

def calcDetailedTable(transactionsReportDf, closedPositionsDf):
    resultColumns = [COL_OPEN, COL_CLOSED, COL_INSTRUMENT, COL_TYPE, COL_UNITS, COL_OPEN_RATE, COL_CLOSE_RATE, COL_CLOSE_CURRENCY, 
                    COL_PROFIT_USD, COL_PROFIT_EUR, COL_INVERTING_AMOUNT, COL_PROFIT_EXCHANGE_RATE, COL_DIVIDENDS_USD,
                    COL_DIVIDENDS_EUR, COL_FEES_USD, COL_FEES_EUR, COL_REVENUE_USD, COL_REVENUE_EUR]
    # resultColumns = ["Eröffnet", "Geschlossen", "Instrument", "Anteile", "Öffnungskurs", "Schlusskurs", "Schlusskurs-Währung",
    #             "Profit-USD", "Profit-EUR", "Invest. Betrag", "W-Kurs G/V", "Dividenden-USD", "Dividenden-EUR", "Gebühren-USD", "Gebühren-EUR", "Ertrag-USD", "Ertrag-EUR"]
    resultTable = pd.DataFrame(columns=resultColumns, index=closedPositionsDf.index)
    for index, row in closedPositionsDf.iterrows():
        positionId = row['Position ID']
        currency = findCurrencyOfPositionId(transactionsReportDf, positionId)
        openDate = parseDate(row['Open Date'])
        closeDate = parseDate(row['Close Date'])
        profitUSD = atof(row['Profit'])
        profitEUR = usdToEur(closeDate, profitUSD)

        amountUSD = atof(row['Amount'])
        amountBeginEUR = usdToEur(openDate, amountUSD)
        amountEndEUR = usdToEur(closeDate, amountUSD)

        wKursGW = amountEndEUR - amountBeginEUR

        dividendRows = dividendRowsOfPosition(transactionsReportDf, positionId)
        dividendsUSD = calculateRowsInUsd(dividendRows)
        dividendsEUR = calculateRowsInEur(dividendRows)

        feeRows = feeRowsOfPosition(transactionsReportDf, positionId)
        feesUSD = calculateRowsInUsd(feeRows)
        feesEUR = calculateRowsInEur(feeRows)

        revenueEUR = profitEUR + wKursGW + dividendsEUR + feesEUR
        revenueUSD = profitUSD + dividendsUSD + feesUSD

        result = {}
        result[COL_OPEN] = row['Open Date']
        result[COL_CLOSED] = row['Close Date']
        result[COL_INSTRUMENT] = row['Action']
        result[COL_TYPE] = TYPE_STOCK if (row['Is Real'] == "Real") else TYPE_CFD
        result[COL_UNITS] = row['Units']
        result[COL_OPEN_RATE] = row['Open Rate']
        result[COL_CLOSE_RATE] = row['Close Rate']
        result[COL_CLOSE_CURRENCY] = currency
        result[COL_PROFIT_USD] = profitUSD
        result[COL_PROFIT_EUR] = profitEUR
        result[COL_INVERTING_AMOUNT] = findInvertingAmountOfPositionId(transactionsReportDf, positionId)
        result[COL_PROFIT_EXCHANGE_RATE] = wKursGW
        result[COL_DIVIDENDS_USD] = dividendsUSD
        result[COL_DIVIDENDS_EUR] = dividendsEUR
        result[COL_FEES_USD] = feesUSD
        result[COL_FEES_EUR] = feesEUR
        result[COL_REVENUE_USD] = revenueUSD
        result[COL_REVENUE_EUR] = revenueEUR

        resultTable.iloc[index] = result

    return resultTable
    
def dividendRowsOfPosition(transactionsReportDf, positionId):
    return transactionsReportDf.loc[(transactionsReportDf['Position ID'] == positionId) & (
        transactionsReportDf['Details'] == "Payment caused by dividend")]

def feeRowsOfPosition(transactionsReportDf, positionId):
    return transactionsReportDf.loc[(transactionsReportDf['Position ID'] == positionId) & (
        transactionsReportDf['Details'] == "Over night fee")]

def findCurrencyOfPositionId(transactionsReportDf, positionId):
    details = transactionsReportDf.loc[transactionsReportDf['Position ID'] == positionId].iloc[0]['Details']
    currency = details.split('/')[1]
    return currency

def findInvertingAmountOfPositionId(transactionsReportDf, positionId):
    value = transactionsReportDf.loc[(transactionsReportDf['Position ID'] == positionId) & (transactionsReportDf['Type'] == "Open Position")].iloc[0]['Amount']
    return locale.str(value)

def parseDate(date):
    ddmmyyDate = date.split(" ")[0].split(".")
    return ddmmyyDate[2] + "-" + ddmmyyDate[1] + "-" + ddmmyyDate[0]

def calculateRowsInEur(rows):
    result = 0.0
    for _, row in rows.iterrows():
        amountUSD = row.loc['Amount']
        date = row.loc['Date'].split(" ")[0]
        result += usdToEur(date, amountUSD)
    return result

def calculateRowsInUsd(rows):
    result = 0.0
    for _, row in rows.iterrows():
        result += row.loc['Amount']
    return result

def float2str(value):
    return locale.str(round(value, 2))
    
