from exchange_rate import calculateRowsInEur, calculateRowsInUsd

COL_ADJUSTMENTS_USD = "Sonstige Anpassungen USD"
COL_ADJUSTMENTS_EUR = "Sonstige Anpassungen EUR"

def calcAdjustments(accountActivityDf):
    result = {}

    adjustmentRows = accountActivityDf[accountActivityDf['Type'].str.contains("(?i)adjustment$")]
    
    result[COL_ADJUSTMENTS_EUR] = calculateRowsInEur(adjustmentRows)
    result[COL_ADJUSTMENTS_USD] = calculateRowsInUsd(adjustmentRows)

    return result