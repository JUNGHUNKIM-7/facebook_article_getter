from typing import List
from inputs import *
from src.data_reader.data_reader_container import DataReaderContainer
from src.data_reader.investpy_container import InvestpyContainer


class TickerInstanceHelper:
    @classmethod
    def make_instance_list(
        cls, source: str
    ) -> List[DataReaderContainer] | List[InvestpyContainer] | None:
        instance_li = []

        if source != "pds" and source != "investpy" and not source:
            raise Exception("Source is not valid")
        elif source == "pds":
            print(
                f"{len(datareader_tickers)} tickers will be Instanced to DataReaderContainer"
            )
            for i in range(len(datareader_tickers.keys())):
                ticker_instance = DataReaderContainer(
                    source=datareader_tickers[f"group{i + 1}"]["source"],
                    ticker_li=datareader_tickers[f"group{i + 1}"]["tickers_group"],
                    time_data=datareader_time_set[f"set{i + 1}"],
                )
                instance_li.append(ticker_instance)
            return instance_li
        elif source == "investpy":
            print(
                f"{len(investpy_tickers)} tickers will be Instanced to InvestpyContainer"
            )
            # todo data filtering
            for i in range(len(investpy_tickers.keys())):
                if investpy_tickers[f"group{i + 1}"]["source"] == "investpy":
                    interval: str = investpy_tickers[f"group{i + 1}"]["interval"]
                    country: List[str] = investpy_tickers[f"group{i + 1}"]["country"]
                    n_result: int = investpy_tickers[f"group{i + 1}"]["n_result"]

                    ticker_instance = InvestpyContainer(
                        ticker_li=investpy_tickers[f"group{i + 1}"]["tickers_group"],
                        time_data=investpy_time_set[f"set{i + 1}"],
                        sector=investpy_tickers[f"group{i + 1}"]["kind"],
                        # Optional section
                        interval=interval if interval else "daily",
                        country=country if country else ["united states"],
                        n_result=n_result if n_result else 1,
                    )
                    instance_li.append(ticker_instance)
            return instance_li
