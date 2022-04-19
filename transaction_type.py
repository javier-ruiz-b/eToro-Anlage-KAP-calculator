from strenum import StrEnum

class TransactionType(StrEnum):
    CFD = 'CFD',
    Crypto = 'Crypto',
    ETF = 'ETF',
    Stocks = 'Stocks'