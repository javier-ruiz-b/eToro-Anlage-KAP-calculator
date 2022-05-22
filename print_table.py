
from detailed_table import *
from locale import atof

def get_date(date_and_time):
    return date_and_time.split(" ")[0]

def limit_string(value, count):
    return " ".join(value.split(" ")[0:count])

def roundstr(value, count):
    if isinstance(value, str):
        value = atof(value)
    return locale.str(round(value, count))

def print_detailed_table(table):
    result = table.copy()
    result = result.sort_values(by=[COL_OPEN_TIMESTAMP])
    result[COL_OPEN] = result[COL_OPEN].apply(lambda x: get_date(x))
    result[COL_CLOSED] = result[COL_CLOSED].apply(lambda x: get_date(x))
    result[COL_INSTRUMENT] = result[COL_INSTRUMENT].apply(lambda x: limit_string(x, 3))

    sum_columns = [COL_PROFIT_EUR, COL_PROFIT_EXCHANGE_RATE, COL_DIVIDENDS_EUR, COL_FEES_EUR, COL_REVENUE_EUR]
    # result.loc['total'] = result[sum_columns].sum()
    for column in sum_columns:        
        result[column] = result[column].apply(lambda x: roundstr(x, 2))
    
    show_columns = [COL_OPEN, COL_CLOSED, COL_INSTRUMENT, COL_TYPE, COL_UNITS, COL_PROFIT_EUR, COL_PROFIT_EXCHANGE_RATE, COL_DIVIDENDS_EUR, COL_FEES_EUR, COL_REVENUE_EUR]
    print(result[show_columns].to_string(index=False))
    print()