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

COL_PROFIT_ON_SALE_CFDS = 'CFD - Enthaltene Gewinne aus Aktienveräußerungen'
COL_PROFIT_ON_SALE_ETFS = 'ETF - Enthaltene Gewinne aus Aktienveräußerungen'

# KAP 22
COL_LOSS_ON_SALE_CFDS = 'CFD G/W - darin enthaltene Verluste aus Kapitalerträgen ohne Aktienveräußerung'
COL_FEES_ON_SALE_CFDS = 'CFD Gebühren - darin enthaltene Verluste aus Kapitalerträgen ohne Aktienveräußerung'
COL_LOSS_ON_SALE_ETFS = 'ETF G/W - darin enthaltene Verluste aus Kapitalerträgen ohne Aktienveräußerung'

# KAP 23
COL_LOSS_ON_SALE_STOCKS = 'Aktien G/W - Enthaltene Verluste aus Aktienveräußerungen'

# SO 44
COL_CLOSING_PRICE_CRYPTO = 'Crypto Schließungspreis'

# SO 45
COL_OPENING_PRICE_CRYPTO = 'Crypto Eröffnungsspreis'

# SO 47 und 48
COL_PROFIT_CRYPTO = 'Crypto G/V'

def roundTo2Decimals(dict):
    result = {}
    for key in dict:      
        result[key] = round(dict[key], 2)
    return result

def calcKapSummary(detailedTable, adjustmentsDict):
    result = {}
    result[COL_PROFIT_STOCKS] = 0
    result[COL_DIVIDENDS_STOCKS] = 0
    result[COL_PROFIT_ON_SALE_STOCKS] = 0
    result[COL_LOSS_ON_SALE_STOCKS] = 0

    result[COL_PROFIT_IN_STOCKS] = 0

    result[COL_PROFIT_CFDS] = 0
    result[COL_DIVIDENDS_CFDS] = 0
    result[COL_FEES_CFDS] = 0
    result[COL_PROFIT_ON_SALE_CFDS] = 0
    result[COL_LOSS_ON_SALE_CFDS] = 0
    result[COL_FEES_ON_SALE_CFDS] = 0

    result[COL_PROFIT_ETFS] = 0
    result[COL_PROFIT_ON_SALE_ETFS] = 0
    result[COL_LOSS_ON_SALE_ETFS] = 0

    result[COL_OPENING_PRICE_CRYPTO] = 0
    result[COL_CLOSING_PRICE_CRYPTO] = 0

    result[COL_ADJUSTMENTS] = adjustmentsDict[adjustments.COL_ADJUSTMENTS_EUR]


    for _, row in detailedTable.iterrows():
        revenueEUR = row[detailed_table.COL_REVENUE_EUR]
        dividend = row[detailed_table.COL_DIVIDENDS_EUR]
        fees = row[detailed_table.COL_FEES_EUR]
        type = row[detailed_table.COL_TYPE]
        if type == TransactionType.Stocks:
            isin = row[detailed_table.COL_ISIN]
            if isin.startswith('DE'):
                result[COL_PROFIT_IN_STOCKS] += revenueEUR - dividend
            else:
                result[COL_PROFIT_STOCKS] += revenueEUR - dividend
                result[COL_DIVIDENDS_STOCKS] += dividend
                if revenueEUR > 0:
                    result[COL_PROFIT_ON_SALE_STOCKS] += revenueEUR - dividend
                else:
                    result[COL_LOSS_ON_SALE_STOCKS] += revenueEUR - dividend

        elif type == TransactionType.CFD:
            result[COL_PROFIT_CFDS] += revenueEUR - fees - dividend
            result[COL_DIVIDENDS_CFDS] += dividend
            result[COL_FEES_CFDS] += fees
            result[COL_FEES_ON_SALE_CFDS] += fees
            if revenueEUR > 0:
                result[COL_PROFIT_ON_SALE_CFDS] += revenueEUR - fees - dividend
            else:
                result[COL_LOSS_ON_SALE_CFDS] += revenueEUR - fees - dividend

        elif type == TransactionType.ETF:
            result[COL_PROFIT_ETFS] += revenueEUR - fees
            if revenueEUR > 0:
                result[COL_PROFIT_ON_SALE_ETFS] += revenueEUR - fees
            else:
                result[COL_LOSS_ON_SALE_ETFS] += revenueEUR - fees

        elif type == TransactionType.Crypto:
            instrument = row[detailed_table.COL_INSTRUMENT].lower()
            if instrument.startswith("buy "):
                if revenueEUR > 0:
                    result[COL_OPENING_PRICE_CRYPTO] += -revenueEUR
                else:
                    result[COL_CLOSING_PRICE_CRYPTO] += revenueEUR
            elif instrument.startswith("sell "):
                print("Warning: sell crypto not implemented")
            else:
                print("Warning: Unknown prefix. expecting buy or sell: "+ instrument)
        else:
            print("Warning: unimplemented type:"+ row[detailed_table.COL_TYPE])
            #raise Exception("unimplemented type:"+ row[detailed_table.COL_TYPE] )
            


    # print(json.dumps(result, indent=1))
    print(json.dumps(roundTo2Decimals(result), ensure_ascii=False, indent=4))
        
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
    kapResult["20. Enthaltene Gewinne aus Aktienveräußerungen"] = result[COL_PROFIT_ON_SALE_STOCKS] + result[COL_PROFIT_ON_SALE_CFDS]
    kapResult["22. Enthaltene Verluste ohne Verluste aus Aktienveräußerungen"] = result[COL_LOSS_ON_SALE_CFDS] + result[COL_FEES_ON_SALE_CFDS]
    kapResult["23. Enthaltene Verluste aus Aktienveräußerungen"] = result[COL_LOSS_ON_SALE_STOCKS]

    print(json.dumps(roundTo2Decimals(kapResult), ensure_ascii=False, indent=4))
    
    print("\nAnlage SO")
    soResult = {}
    # soResult["10. Einnahmen aus PI-Zahlungen und Provisionen für Kundenwerbung"] = 0
    # soResult["11. Einnahmen aus Staking und Airdrops von Kryptowährungen"] = 0
    # soResult["12. Summe aus Zeilen 10 + 11"] = 0
    #Die Summe aller Schließungspreise von Trades auf Kryptowährungen und erfolgten Anpassungen hierauf
    soResult["44. Veräußerungspreis oder an dessen Stelle tretender Wert (z. B. gemeiner Wert)"] = result[COL_CLOSING_PRICE_CRYPTO]
    #Die Summe aller Eröffnungspreise von Trades auf Kryptowährungen
    soResult["45. Anschaffungskosten (ggf. gemindert um Absetzung für Abnutzung) oder an deren Stelle tretender Wert (z. B. Teilwert, gemeiner Wert)"] = result[COL_OPENING_PRICE_CRYPTO]
    result[COL_PROFIT_CRYPTO] = result[COL_CLOSING_PRICE_CRYPTO] - result[COL_OPENING_PRICE_CRYPTO]
    soResult["47. Gewinn / Verlust (zu übertragen nach Zeile 48)"] = result[COL_PROFIT_CRYPTO]

    print(json.dumps(roundTo2Decimals(soResult), ensure_ascii=False, indent=4))
