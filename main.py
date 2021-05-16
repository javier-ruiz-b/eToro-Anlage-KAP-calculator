import pandas as pd
import sys
from detailed_table import *
from kap_summary import *
from print_table import *
from locale import setlocale, LC_NUMERIC
setlocale(LC_NUMERIC, 'de_DE.UTF-8')

# nur für KAP:
# https://www.wertpapier-forum.de/topic/58402-steuererkl%C3%A4rung-etoro/
# based on trade.report

accountStatementFilename = " ".join(sys.argv[1:])
closedPositions = pd.read_excel(accountStatementFilename, 'Closed Positions', engine='openpyxl')
transactionsReport = pd.read_excel(accountStatementFilename, 'Transactions Report', engine='openpyxl')

detailedTable = calcDetailedTable(transactionsReport, closedPositions)
print_detailed_table(detailedTable)
detailedTable.to_csv('detailedTable.csv')
calcKapSummary(detailedTable)