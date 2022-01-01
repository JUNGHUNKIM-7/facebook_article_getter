from functools import wraps
from src.inputs.tickers import *
from src.data_reader.data_reader_container import DataReaderContainer
from src.data_reader.investpy_container import InvestpyContainer

class TickerInstanceHelper:
    @classmethod
    def make_instance_list(
        cls, source: str
    ) -> list[DataReaderContainer] | list[InvestpyContainer] | None:
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
                f"{len(investpy_tickers)} groups will be Instanced to InvestpyContainer"
            )
            for i in range(len(investpy_tickers.keys())):
                if investpy_tickers[f"group{i + 1}"]["source"] == "investpy":
                    ticker_instance = InvestpyContainer(
                        ticker_li=investpy_tickers[f"group{i + 1}"]["tickers_group"],
                        time_data=investpy_time_set[f"set{i + 1}"],
                        sector=investpy_tickers[f"group{i + 1}"]["sector"],
                        # Optional section
                        interval=investpy_tickers[f"group{i + 1}"]["interval"]
                        if "interval" in investpy_tickers[f"group{i + 1}"].keys()
                        else None,
                        country=investpy_tickers[f"group{i + 1}"]["country"]
                        if "county" in investpy_tickers[f"group{i + 1}"].keys()
                        else None,
                        n_result=investpy_tickers[f"group{i + 1}"]["n_result"]
                        if "n_result" in investpy_tickers[f"group{i + 1}"].keys()
                        else None,
                        search_type=investpy_tickers[f"group{i + 1}"]["search_type"]
                        if "search_type" in investpy_tickers[f"group{i+ 1}"].keys()
                        else None,
                    )
                    instance_li.append(ticker_instance)
            return instance_li
