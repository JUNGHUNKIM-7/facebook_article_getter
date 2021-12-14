from datetime import date
from enum import Enum, auto
from typing import Dict, Any, List

import pandas as pd
from pandas import DataFrame
import investpy
from investpy.utils.search_obj import SearchObj

from src.utils.time_handler import TimeHandler
from src.utils.option_container import OptionContainer

class SearchTypes(Enum):
    GET_INFO = auto()
    GET_LIST = auto()
    GET_OVERVIEW = auto()
    GET_ETF_COUNTRIES = auto()


class InvestpyContainer:
    def __init__(
        self,
        ticker_li: List[str],
        time_data: Dict[str, str|int],
        sector: str,
        interval: str,
        country: List[str],
        n_result: int,
    ):
        self.__ticker_li = ticker_li
        self.__sector = sector
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
    def sector(self) -> str:
        return self.__sector

    def __str__(self):
        return f"{self.__ticker_li}\n{self.__sector}\n{self.__interval}\n{self.__start}\n{self.__end}"

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
    def get_technical_indicator(elem: SearchObj, interval: str) -> DataFrame:
        df: DataFrame = elem.retrieve_technical_indicators(interval=interval)
        return df

    def get_quotes(self) -> List[Any]:
        quotes: List[Any] = []
        for t in self.__ticker_li:
            quotes.append(
                investpy.search_quotes(
                    text=t,
                    products=[self.__sector],
                    countries=self.__country,
                    n_results=self.__n_result,
                )
            )
        return quotes

    # technical idx
    def get_technical_idx(self)  -> None:
        df_li: List[DataFrame] = []
        for t in self.__ticker_li:
            ma_df = investpy.moving_averages(  # moving Average
                name=t,
                country=self.__country[0],
                product_type=self.__sector,
                interval=self.__interval,
            )
            pv_point_df = investpy.pivot_points(  # pivot point
                name=t,
                country=self.__country[0],
                product_type=self.__sector,
                interval=self.__interval,
            )
            combined_df = pd.concat([ma_df, pv_point_df], ignore_index=True)
            df_li.append(combined_df)

    def get_crypto_info(self, type: SearchTypes):
        match type:
            case SearchTypes.GET_INFO:
                info = investpy.get_crypto_information(crypto="bitcoin")
                return info
            case SearchTypes.GET_LIST:
                crypto_list: List[str] = investpy.get_cryptos_list()
                return crypto_list
            case SearchTypes.GET_OVERVIEW:
                overview: DataFrame = investpy.get_cryptos_overview()
                return overview

    def get_crypto_quotes(self):
        historical = investpy.get_crypto_historical_data(
            crypto="bitcoin", from_date=self.__start, to_date=self.__end
        )
        print(historical)

    def get_efts_info(self, type: SearchTypes):
        match type:
            case SearchTypes.GET_LIST:
                all_efts: List[str] = investpy.get_etfs_list()
                return all_efts
            case SearchTypes.GET_ETF_COUNTRIES:
                etf_countries: List[str] = investpy.get_etf_countries()
                return etf_countries
            case SearchTypes.GET_INFO:
                etf_info = investpy.get_etf_information(etf="VFMVN30", country=self.__country[0])
                return etf_info

    def get_efts_quotes(self):
        etf_historical = investpy.get_etf_historical_data(
            country=self.__country[0],
            etf="COMT",
            from_date=self.__start,
            to_date=self.__end,
        )
        print(etf_historical)

    # commodities
    def get_commodities_info(self, type:SearchTypes):
        match type:
            case SearchTypes.GET_LIST:
                commo_list = investpy.get_commodities_list()
                get_commo_group = investpy.get_commodity_groups()
                return [commo_list, get_commo_group]
            case SearchTypes.GET_INFO:
                get_commo_info = investpy.get_commodity_information(commodity="crude")
                return get_commo_info
            case SearchTypes.GET_OVERVIEW:
                commo_overview = investpy.get_commodities_overview(group="crude")
                return commo_overview

    def get_commodities_quote(self):
        get_commo = investpy.get_commodities(group="crude")
        return get_commo

    def get_commodities_historical_data(self):
        commo_historical = investpy.get_commodity_historical_data(
            commodity="crude", from_date=self.__start, to_date=self.__end
        )
        return commo_historical

    # to csv
    def save_to_csv(self, df: DataFrame, file_name: str, desc: str):
        df.to_csv(f"{self.__loc}\\{file_name}_{desc}.csv")
        print(f"Ticker {self.__start}-{self.__end}: {file_name} downloaded")

    def technical_indicator_to_csv(self) -> None:
        print(f'{len(self.get_quotes())} are going to converting to csv')
        for e in self.get_quotes():
            info_df = self.get_info(elem=e)
            technical_df = self.get_technical_indicator(elem=e, interval=self.__interval)
            combined_df: DataFrame = pd.concat(
                [info_df, technical_df], ignore_index=True
            )
            self.save_to_csv(
                df=combined_df, file_name=e.name, desc="technical_indicator"
            )

    def technical_index_to_csv(self):
        pass

    def crypto_to_csv(self):
        pass

    def etfs_to_csv(self):
        pass

    def get_comm_to_csv(self):
        pass
