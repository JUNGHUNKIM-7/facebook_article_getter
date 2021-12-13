from typing import List
from inputs import *
from src.data_reader.data_reader_container import DataReaderContainer
from src.data_reader.investipy_container import InvestipyContainer


class TickerInstanceHelper:
    @classmethod
    def return_ticker_ins_li(
        cls, source: str
    ) -> List[DataReaderContainer] | List[InvestipyContainer] | None:
        instance_li = []

        if source != "pds" and source != "investipy" and not source:
            raise Exception("Any Source Found to Search tickers")
        elif source == "pds":
            for i in range(len(tickers.keys())):
                ticker_instance = DataReaderContainer(
                    source=tickers[f"group{i + 1}"]["source"],
                    ticker_li=tickers[f"group{i + 1}"]["tickers_group"],
                    time_data=time_set[f"set{i + 1}"],
                )
                instance_li.append(ticker_instance)
            return instance_li
        elif source == "investipy":
            for i in range(len(tickers.keys())):
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
                    instance_li.append(ticker_instance)
            return instance_li
