from typing import List, Union
from src.globals.inputs import *
from src.data_reader.ticker_controller import TickerController
from src.data_reader.investipy_controller import InvestipyController


class TickerManager:
    @classmethod
    def return_ticker_ins_li(
        cls, source: str
    ) -> Union[List[TickerController], List[InvestipyController], None]:
        instance_li = []

        if source != "pds" and source != "investipy" and not source:
            raise Exception("Any Source Found to Search tickers")
        elif source == "pds":
            for i in range(len(tickers.keys())):
                ticker_instance = TickerController(
                    source=tickers[f"group{i + 1}"]["source"],
                    ticker_li=tickers[f"group{i + 1}"]["tickers_group"],
                    time_data=time_set[f"set{i + 1}"],
                )
                instance_li.append(ticker_instance)
            return instance_li
        elif source == "investipy":
            for i in range(len(tickers.keys())):
                ticker_instance = InvestipyController(
                    ticker_li=tickers[f"group{i + 1}"]["tickers_group"],
                    time_data=time_set[f"set{i + 1}"],
                )
                instance_li.append(ticker_instance)
            return instance_li
