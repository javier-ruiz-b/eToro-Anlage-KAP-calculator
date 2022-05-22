from re import S
from numpy import isin
from  transaction_type import TransactionType
import detailed_table
import pandas as pd
from locale import atof
import adjustments
import json

# KAP 18
COL_PROFIT_IN_STOCKS = 'Inl. Aktien G/V'

# KAP 19
COL_PROFIT_STOCKS = 'Aktien G/V'
COL_DIVIDENDS_STOCKS = 'Aktien Dividende'
COL_PROFIT_CFDS = 'CFD G/V'
COL_DIVIDENDS_CFDS = 'CFD Dividende'
COL_FEES_CFDS = 'CFD Gebühren'
COL_PROFIT_ETFS = 'ETF G/V'
COL_ADJUSTMENTS = 'Sonstige Anpassungen'

# KAP 20
COL_PROFIT_ON_SALE_STOCKS = 'Aktien - Enthaltene Gewinne aus Aktienveräußerungen'
COL_PROFIT_ON_SALE_ETFS = 'ETF - Enthaltene Gewinne aus Aktienveräußerungen'

# KAP 21
COL_POSITIVE_FEES_ON_SALE_CFDS = 'CFD positive Gebühren'
COL_PROFIT_ON_SALE_CFDS = 'CFD positive G/W'

# KAP 22
COL_LOSS_ON_SALE_CFDS = 'CFD G/W - darin enthaltene Verluste aus Kapitalerträgen ohne Aktienveräußerung'
COL_LOSS_ON_SALE_ETFS = 'ETF G/W - darin enthaltene Verluste aus Kapitalerträgen ohne Aktienveräußerung'
COL_NEGATIVE_DIVIDENDS_CFDS = 'CFD negative Dividenden'
COL_NEGATIVE_FEES_ON_SALE_CFDS = 'CFD negative Gebuhren'

# KAP 23
COL_LOSS_ON_SALE_STOCKS = 'Aktien G/W - Enthaltene Verluste aus Aktienveräußerungen'

# SO 44
COL_INVERTING_CLOSE_CRYPTO = 'Crypto Schließungspreis'

# SO 45
COL_INVERTING_OPEN_CRYPTO = 'Crypto Öffnungspreis'

# SO 47 und 48
COL_PROFIT_CRYPTO = 'Crypto G/V'

def roundTo2Decimals(dict):
    result = {}
    for key in dict:      
        result[key] = round(dict[key], 2)
    return result

def calcKapSummary(detailedTable, adjustmentsDict):
    result = {}

    stocksAll = detailedTable[(detailedTable['Type'] == 'Stocks')]
    stocksAllProfit = stocksAll[detailed_table.COL_PROFIT_EUR]
    result[COL_PROFIT_ON_SALE_STOCKS] = stocksAllProfit[stocksAllProfit > 0].sum()

    stocks = detailedTable[(detailedTable['Type'] == 'Stocks') & (detailedTable['ISIN'].str.startswith('DE') == False)]
    stocksProfit = stocks[detailed_table.COL_PROFIT_EUR]
    result[COL_PROFIT_STOCKS] = stocksProfit.sum()
    result[COL_LOSS_ON_SALE_STOCKS] = stocksProfit[stocksProfit < 0].sum()
    result[COL_DIVIDENDS_STOCKS] =  stocks[detailed_table.COL_DIVIDENDS_EUR].sum()

    inlandStocks = detailedTable[(detailedTable['Type'] == 'Stocks') & detailedTable['ISIN'].str.startswith('DE')]
    result[COL_PROFIT_IN_STOCKS] = inlandStocks[detailed_table.COL_PROFIT_EUR].sum()

    cfd = detailedTable[(detailedTable['Type'] == 'CFD')]
    cfdProfit = cfd[detailed_table.COL_PROFIT_EUR]
    result[COL_PROFIT_CFDS] = cfdProfit.sum()
    result[COL_PROFIT_ON_SALE_CFDS] = cfdProfit[cfdProfit > 0].sum()
    result[COL_LOSS_ON_SALE_CFDS] = cfdProfit[cfdProfit < 0].sum()
    cfdDividends = cfd[detailed_table.COL_DIVIDENDS_EUR]
    result[COL_DIVIDENDS_CFDS] = cfdDividends.sum()
    result[COL_NEGATIVE_DIVIDENDS_CFDS] = cfdDividends[cfdDividends < 0].sum()
    cfdFees = cfd[detailed_table.COL_FEES_EUR]
    result[COL_FEES_CFDS] = cfdFees.sum()
    result[COL_POSITIVE_FEES_ON_SALE_CFDS] = cfdFees[cfdFees > 0].sum()
    result[COL_NEGATIVE_FEES_ON_SALE_CFDS] = cfdFees[cfdFees < 0].sum()
    
    profitEtf = detailedTable[(detailedTable['Type'] == 'ETF')][detailed_table.COL_PROFIT_EUR]
    result[COL_PROFIT_ETFS] = profitEtf.sum()
    result[COL_PROFIT_ON_SALE_ETFS] = profitEtf[profitEtf > 0].sum()
    result[COL_LOSS_ON_SALE_ETFS] =  profitEtf[profitEtf < 0].sum()
    
    crypto = detailedTable[(detailedTable['Type'] == 'Crypto')]
    result[COL_INVERTING_OPEN_CRYPTO] = crypto[detailed_table.COL_INVERTING_AMOUNT_EUR].sum()
    result[COL_PROFIT_CRYPTO] = crypto[detailed_table.COL_PROFIT_EUR].sum()
    result[COL_INVERTING_CLOSE_CRYPTO] =  result[COL_INVERTING_OPEN_CRYPTO] + result[COL_PROFIT_CRYPTO] 

    result[COL_ADJUSTMENTS] = adjustmentsDict[adjustments.COL_ADJUSTMENTS_EUR]

    # print(json.dumps(roundTo2Decimals(result), ensure_ascii=False, indent=4))
        
    print("\nAnlage KAP")
    kapResult = {}
    kapResult["18. Inländische Kapitalerträge"] = result[COL_PROFIT_IN_STOCKS]
    kapResult["19. Ausländische Kapitalerträge"] = result[COL_PROFIT_STOCKS] + result[COL_DIVIDENDS_STOCKS] + result[COL_PROFIT_CFDS] + result[COL_FEES_CFDS] + result[COL_PROFIT_ETFS] + result[COL_ADJUSTMENTS]
    kapResult["19.   - Ausländische Aktien G/W"] = result[COL_PROFIT_STOCKS] 
    kapResult["19.   - Ausländische Aktien Dividende"] = result[COL_DIVIDENDS_STOCKS]
    kapResult["19.   - Ausländische CFD G/W"] = result[COL_PROFIT_CFDS] 
    kapResult["19.   - Ausländische CFD Dividende"] = result[COL_DIVIDENDS_CFDS]
    kapResult["19.   - Ausländische CFD Gebühren"] = result[COL_FEES_CFDS]
    kapResult["19.   - Ausländische ETF G/W"] = result[COL_PROFIT_ETFS]
    kapResult["19.   - Sonstige Anpassungen"] = result[COL_ADJUSTMENTS]
    kapResult["20. Enthaltene Gewinne aus Aktienveräußerungen"] = result[COL_PROFIT_ON_SALE_STOCKS]
    kapResult["20.   - Aktien G/V (positive Beiträge)"] = result[COL_PROFIT_ON_SALE_STOCKS] 
    kapResult["21. Enthaltene Einkünfte aus Stillhalterprämien und Gewinne aus Termingeschäften"] = result[COL_PROFIT_ON_SALE_CFDS] + result[COL_POSITIVE_FEES_ON_SALE_CFDS]
    kapResult["21.   - CFD G/V (positive Beiträge)"] = result[COL_PROFIT_ON_SALE_CFDS]
    kapResult["21.   - CFD Gebühren (positive Beiträge)"] = result[COL_POSITIVE_FEES_ON_SALE_CFDS]
    kapResult["22. Enthaltene Verluste ohne Verluste aus Aktienveräußerungen"] = result[COL_LOSS_ON_SALE_CFDS] + result[COL_NEGATIVE_DIVIDENDS_CFDS] + result[COL_NEGATIVE_FEES_ON_SALE_CFDS] + result[COL_LOSS_ON_SALE_ETFS]
    kapResult["22.   - CFD G/V (negative Beiträge)"] = result[COL_LOSS_ON_SALE_CFDS] 
    kapResult["22.   - CFD Dividends (negative Beiträge)"] = result[COL_NEGATIVE_DIVIDENDS_CFDS]
    kapResult["22.   - CFD Gebühren (negative Beiträge)"] = result[COL_NEGATIVE_FEES_ON_SALE_CFDS] 
    kapResult["22.   - ETF G/V (negative Beiträge)"] = result[COL_LOSS_ON_SALE_ETFS] 
    kapResult["23. Enthaltene Verluste aus Aktienveräußerungen"] = result[COL_LOSS_ON_SALE_STOCKS]
    kapResult["24. Verluste aus Termingeschäften"] = result[COL_LOSS_ON_SALE_CFDS] + result[COL_NEGATIVE_DIVIDENDS_CFDS] + result[COL_NEGATIVE_FEES_ON_SALE_CFDS] 
    kapResult["24.   - CFD G/V (negative Beiträge)"] = result[COL_LOSS_ON_SALE_CFDS] 
    kapResult["24.   - CFD Dividends (negative Beiträge)"] = result[COL_NEGATIVE_DIVIDENDS_CFDS]
    kapResult["24.   - CFD Gebühren (negative Beiträge)"] = result[COL_NEGATIVE_FEES_ON_SALE_CFDS] 

    print(json.dumps(roundTo2Decimals(kapResult), ensure_ascii=False, indent=4))
    
    print("\nAnlage SO")
    soResult = {}
    ## don't know how to calculate this:
    # soResult["10. Einnahmen aus PI-Zahlungen und Provisionen für Kundenwerbung"] = 0
    # soResult["11. Einnahmen aus Staking und Airdrops von Kryptowährungen"] = 0
    # soResult["12. Summe aus Zeilen 10 + 11"] = 0
    #Die Summe aller Schließungspreise von Trades auf Kryptowährungen und erfolgten Anpassungen hierauf
    soResult["44. Veräußerungspreis oder an dessen Stelle tretender Wert (z. B. gemeiner Wert)"] = result[COL_INVERTING_CLOSE_CRYPTO]
    #Die Summe aller Eröffnungspreise von Trades auf Kryptowährungen
    soResult["45. Anschaffungskosten (ggf. gemindert um Absetzung für Abnutzung) oder an deren Stelle tretender Wert (z. B. Teilwert, gemeiner Wert)"] = result[COL_INVERTING_OPEN_CRYPTO]
    # result[COL_PROFIT_CRYPTO] = result[COL_CLOSING_PRICE_CRYPTO] - result[COL_OPENING_PRICE_CRYPTO]
    soResult["47. Gewinn / Verlust (zu übertragen nach Zeile 48)"] =  result[COL_PROFIT_CRYPTO]

    print(json.dumps(roundTo2Decimals(soResult), ensure_ascii=False, indent=4))

    print( )

