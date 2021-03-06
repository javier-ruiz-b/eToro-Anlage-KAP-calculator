from datetime import datetime

def parseDate(date): #example: 18/10/2021 13:32:48
    ddmmyyDate = date.split(" ")[0].split("/")
    return ddmmyyDate[2] + "-" + ddmmyyDate[1] + "-" + ddmmyyDate[0]

def parseGermanDate(date): #example: 26.03.2020 08:00
    ddmmyyDate = date.split(" ")[0].split(".")
    return ddmmyyDate[2] + "-" + ddmmyyDate[1] + "-" + ddmmyyDate[0]

def parseDateToTimestamp(date): #example: 18/10/2021 13:32:48
    date_time_obj = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    return datetime.timestamp(date_time_obj)