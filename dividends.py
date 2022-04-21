from exchange_rate import calculateRowsInEur, calculateRowsInUsd

COL_DIVIDENDS_OUT_STOCKS_USD = "Aus. Aktien Dividenden-USD"
COL_DIVIDENDS_OUT_STOCKS_EUR = "Aus. Aktien Dividenden-EUR"
COL_DIVIDENDS_IN_STOCKS_USD = "Inl. Aktien Dividenden-USD"
COL_DIVIDENDS_IN_STOCKS_EUR = "Inl. Aktien Dividenden-EUR"
COL_DIVIDENDS_CFD_USD = "CFD Dividenden-USD"
COL_DIVIDENDS_CFD_EUR = "CFD Dividenden-EUR"
COL_DIVIDENDS_USD = "Total Dividenden-USD"
COL_DIVIDENDS_EUR = "Total Dividenden-EUR"

def calcDividends(accountActivityDf):
    result = {}

    dividendRows = accountActivityDf[accountActivityDf['Type'].str.contains("(?i)dividend$")]
    
    result[COL_DIVIDENDS_EUR] = calculateRowsInEur(dividendRows)
    result[COL_DIVIDENDS_USD] =  calculateRowsInUsd(dividendRows)

    return result
