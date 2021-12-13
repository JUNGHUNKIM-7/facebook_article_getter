from src.data_reader.investipy_container import InvestipyContainer
from inputs import *

for i in range(2):
    if (
        tickers[f"group{i + 1}"]["source"] == "yahoo"
        or tickers[f"group{i + 1}"]["source"] == "investpy"
    ):
        ticker_instance = InvestipyContainer(
            ticker_li=tickers[f"group{i + 1}"]["tickers_group"],
            time_data=time_set[f"set{i + 1}"],
            kind=tickers[f"group{i + 1}"]["kind"],
            interval=tickers[f"group{i + 1}"]["interval"],
        )
        print(ticker_instance)
