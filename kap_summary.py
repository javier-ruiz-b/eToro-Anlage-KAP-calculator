from  transaction_type import TransactionType
import detailed_table
import pandas as pd
from locale import atof
import json

# KAP 19
COL_PROFIT_STOCKS = 'Aktien G/V'
COL_DIVIDENDS_STOCKS = 'Aktien Dividende'
COL_PROFIT_CFDS = 'CFD G/V'
COL_FEES_CFDS = 'CFD Gebühren'

# KAP 20
COL_PROFIT_ON_SALE_STOCKS = 'Aktien - Enthaltene Gewinne aus Aktienveräußerungen'
COL_PROFIT_ON_SALE_CFDS = 'CFD - Enthaltene Gewinne aus Aktienveräußerungen'

# KAP 22
COL_LOSS_ON_SALE_CFDS = 'CFD G/W - darin enthaltene Verluste aus Kapitalerträgen ohne Aktienveräußerung'
COL_FEES_ON_SALE_CFDS = 'CFD Gebühren - darin enthaltene Verluste aus Kapitalerträgen ohne Aktienveräußerung'

# KAP 23
COL_LOSS_ON_SALE_STOCKS = 'Aktien G/W - Enthaltene Verluste aus Aktienveräußerungen'

def roundTo2Decimals(dict):
    result = {}
    for key in dict:      
        result[key] = round(dict[key], 2)
    return result

def calcKapSummary(detailedTable):
    resultColumns = [COL_PROFIT_STOCKS, COL_DIVIDENDS_STOCKS, COL_PROFIT_CFDS, COL_FEES_CFDS,
                    COL_PROFIT_ON_SALE_STOCKS, COL_LOSS_ON_SALE_CFDS, COL_FEES_ON_SALE_CFDS, 
                    COL_LOSS_ON_SALE_STOCKS]
    resultTable = pd.DataFrame(columns=resultColumns)
    result = {}
    result[COL_PROFIT_STOCKS] = 0
    result[COL_DIVIDENDS_STOCKS] = 0
    result[COL_PROFIT_CFDS] = 0
    result[COL_FEES_CFDS] = 0
    result[COL_PROFIT_ON_SALE_STOCKS] = 0
    result[COL_PROFIT_ON_SALE_CFDS] = 0
    result[COL_LOSS_ON_SALE_CFDS] = 0
    result[COL_FEES_ON_SALE_CFDS] = 0
    result[COL_LOSS_ON_SALE_STOCKS] = 0

    for index, row in detailedTable.iterrows():
        revenueEUR = row[detailed_table.COL_REVENUE_EUR]
        dividend = row[detailed_table.COL_DIVIDENDS_EUR]
        fees = row[detailed_table.COL_FEES_EUR]
        if row[detailed_table.COL_TYPE] == TransactionType.Stocks:
            result[COL_PROFIT_STOCKS] += revenueEUR - dividend
            result[COL_DIVIDENDS_STOCKS] += dividend
            if revenueEUR > 0:
                result[COL_PROFIT_ON_SALE_STOCKS] += revenueEUR - dividend
            else:
                result[COL_LOSS_ON_SALE_STOCKS] += revenueEUR - dividend

        elif row[detailed_table.COL_TYPE] == TransactionType.CFD:
            result[COL_PROFIT_CFDS] += revenueEUR - fees
            result[COL_FEES_CFDS] += fees
            result[COL_FEES_ON_SALE_CFDS] += fees
            if revenueEUR > 0:
                result[COL_PROFIT_ON_SALE_CFDS] += revenueEUR - fees
            else:
                result[COL_LOSS_ON_SALE_CFDS] += revenueEUR - fees
        # elif row[detailed_table.COL_TYPE] == TransactionType.Crypto:
        # elif row[detailed_table.COL_TYPE] == TransactionType.ETF:
        else:
            raise Exception("unimplemented type:"+ row[detailed_table.COL_TYPE] )
            
    # print(json.dumps(result, indent=1))
    print(json.dumps(roundTo2Decimals(result), ensure_ascii=False, indent=4))
        
    kapResult = {}
    kapResult["19. Ausländische Kapitalerträge"] = result[COL_PROFIT_STOCKS] + result[COL_DIVIDENDS_STOCKS] + result[COL_PROFIT_CFDS] + result[COL_FEES_CFDS]
    kapResult["20. Enthaltene Gewinne aus Aktienveräußerungen"] = result[COL_PROFIT_ON_SALE_STOCKS] + result[COL_PROFIT_ON_SALE_CFDS]
    kapResult["22. Enthaltene Verluste ohne Verluste aus Aktienveräußerungen"] = result[COL_LOSS_ON_SALE_CFDS] + result[COL_FEES_ON_SALE_CFDS]
    kapResult["23. Enthaltene Verluste aus Aktienveräußerungen"] = result[COL_LOSS_ON_SALE_STOCKS]

    print("\nAnlage KAP")    
    print(json.dumps(roundTo2Decimals(kapResult), ensure_ascii=False, indent=4))