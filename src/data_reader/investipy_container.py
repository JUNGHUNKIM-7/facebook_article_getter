from datetime import date
from typing import Dict, Any, List, Union

import pandas as pd
from pandas import DataFrame

import investpy
from investpy.utils.search_obj import SearchObj

from src.utils.time_handler import TimeHandler
from src.utils.option_container import OptionContainer

class InvestipyContainer:
    def __init__(
        self,
        ticker_li: List[str],
        time_data: Dict[str, Union[str, int]],
        kind: str,
        interval: str,
        country: List[str] = ["united states"],
        n_result: int = 1,
    ):
        self.__ticker_li = ticker_li
        self.__kind = kind
        self.__interval = interval
        self.__country = country
        self.__n_result = n_result

        if time_data.get("before") is not None:
            self.__start = TimeHandler(time_data).start
        else:
            self.__start = TimeHandler(time_data).base

        if time_data.get("after") is not None and time_data.get("specific") is None:
            self.__end = TimeHandler(time_data).end
        elif time_data.get("after") is None and time_data.get("specific") is not None:
            self.__end = TimeHandler(time_data).specific
        elif (
            time_data.get("before")
            and time_data.get("base")
            and not time_data.get("after")
            and not time_data.get("specific")
        ):
            self.__end = TimeHandler(time_data).base
        else:
            self.__end = TimeHandler(time_data).today

        sy, sm, sd = [elem for elem in str(self.__start).split("-")]
        ey, em, ed = [elem for elem in str(self.__end).split("-")]

        self.__start = f"{sd}/{sm}/{sy}"
        self.__end = f"{ed}/{em}/{ey}"

        self.__loc = OptionContainer.save_path()

    @property
    def starting_date(self) -> date | str:
        return self.__start

    @property
    def ending_date(self) -> date | str:
        return self.__end

    @property
    def kind(self) -> str:
        return self.__kind

    def __str__(self):
        return f"{self.__ticker_li}\n{self.__kind}\n{self.__interval}\n{self.__start}\n{self.__end}"

    # df helper
    def save_to_csv(self, df: DataFrame, file_name: str, desc: str):
        df.to_csv(f"{self.__loc}\\{file_name}_{desc}.csv")
        print(f"Ticker {self.__start}-{self.__end}: {file_name} downloaded")

    # technical indicator
    @staticmethod
    def get_info(elem: SearchObj) -> DataFrame:
        info_dict: Dict[str, Any] = elem.retrieve_information()  # return dict
        key_temp = []
        value_temp = []

        for key, value in info_dict.items():
            key_temp.append(key)
            value_temp.append(value)
        df: DataFrame = pd.DataFrame(data={"indicator": key_temp, "value": value_temp})
        return df

    @staticmethod
    def technical_info(elem: SearchObj, interval: str) -> DataFrame:
        df: DataFrame = elem.retrieve_technical_indicators(interval=interval)
        return df

    def get_list_from_investpy_quotes(self) -> List[Any]:
        quotes: List[Any] = []
        for ticker in self.__ticker_li:
            quotes.append(
                investpy.search_quotes(
                    text=ticker,
                    products=[self.__kind],
                    countries=self.__country,
                    n_results=self.__n_result,
                )
            )
        return quotes

    def get_technical_indicator_to_scv(self) -> None:
        for e in self.get_list_from_investpy_quotes():
            info_df = self.get_info(elem=e)
            technical_df = self.technical_info(elem=e, interval=self.__interval)
            combined_df: DataFrame = pd.concat(
                [info_df, technical_df], ignore_index=True
            )
            self.save_to_csv(
                df=combined_df, file_name=e.name, desc="technical_indicator"
            )

    # technical idx
    def technical_container(self):
        pass

    def get_technical_to_csv(self):
        pass

    # crypto
    def crypto_container(self):
        pass

    def get_crypto_to_csv(self):
        pass

    # etfs
    def etfs_container(self):
        pass

    def get_etfs_to_csv(self):
        pass

    # commodities
    def commodities_container(self):
        pass

    def get_comm_to_csv(self):
        pass
