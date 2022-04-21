from exchange_rate import calculateRowsInEur, calculateRowsInUsd

COL_FEES_USD = "Total Gebühren-USD"
COL_FEES_EUR = "Total Gebühren-EUR"

def calcFees(accountActivityDf):
    result = {}

    feesRows = accountActivityDf[accountActivityDf['Type'].str.contains("(?i)fee$")]
    feesUSD = calculateRowsInUsd(feesRows)
    feesEUR = calculateRowsInEur(feesRows)
    
    result[COL_FEES_USD] = feesEUR
    result[COL_FEES_EUR] = feesUSD

    return result
