# Germany Anlage KAP calculations for eToro

Calculates the values that should go in your german tax declaration (Steuererklärung).

Use at your own risk! Use services like trade.report if you want more guarantees.


## Usage:

* Export the Account Statement of the whole year in Excel format (01-01 - 31-12).
* Install python requirements: pip3 install -r requirements.txt 
* Update USD-EUR database file if necessary (> Steuererklärung 2020). Download this file as csv: https://www.bundesbank.de/dynamic/action/de/statistiken/zeitreihen-datenbanken/zeitreihen-datenbank/723454/723454?listId=www_s331_b01012_3&tsTab=1&statisticType=BBK_ITS&tsId=BBEX3.D.USD.EUR.BB.AC.000
* Run: python3 main.py eToroAccountStatement - xxxxxxxxx - 01-01-2020 - 31-12-2020.xlsx
* Optional: Use trade.report if you want to check that half of the calculations are correct.