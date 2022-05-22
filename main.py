import pandas as pd
import sys
from detailed_table import *
from kap_summary import *
from print_table import *
from locale import setlocale, LC_NUMERIC
from adjustments import calcAdjustments

setlocale(LC_NUMERIC, 'de_DE.UTF-8')

# nur für KAP:
# https://www.wertpapier-forum.de/topic/58402-steuererkl%C3%A4rung-etoro/
# based on trade.report

accountStatementFilename = " ".join(sys.argv[1:])
closedPositionsTable = pd.read_excel(accountStatementFilename, 'Closed Positions', engine='openpyxl')
accountActivityTable = pd.read_excel(accountStatementFilename, 'Account Activity', engine='openpyxl')

detailedTable = calcDetailedTable(accountActivityTable, closedPositionsTable)
print_detailed_table(detailedTable)
detailedTable.to_csv('detailedTable.csv')

adjustments = calcAdjustments(accountActivityTable)

calcKapSummary(detailedTable, adjustments)