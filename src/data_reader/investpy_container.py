from datetime import date
from typing import Any, Optional
import pandas as pd
from pandas import DataFrame
import investpy
from investpy.utils.search_obj import SearchObj
from src.utils.time_handler import TimeHandler
from options import OptionContainer, SearchTypes
from dataclasses import dataclass, field


class InvestpyContainer():
    def __init__(
        self,
        ticker_li: list[str],
        time_data: dict[str, str | int],
        sector: str,
        interval: Optional[str] = None,
        country: Optional[list[str]] = None,
        n_result: Optional[int] = None,
        search_type: SearchTypes = None
    ):
        self.__ticker_li = ticker_li
        self.__sector = sector
        self.__interval = interval if interval is not None else 'daily'
        self.__country = country if country is not None else ['united states']
        self.__n_result = n_result if n_result is not None else 1

        if search_type is not None:
            self.__search_type = search_type

        self.__start = TimeHandler(time_data).start \
            if time_data.get("before") is not None \
            else TimeHandler(time_data).base

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

    def save_to_csv(self, df: DataFrame, file_name: str, desc: str) -> None:
        df.to_csv(f"{self.__loc}\\{file_name}_{desc}.csv")
        print(f"Ticker {self.__start}-{self.__end}: {file_name} downloaded")

    @staticmethod
    def get_info(elem: SearchObj) -> DataFrame:
        info_dict: dict[str, Any] = elem.retrieve_information()
        key_temp = []
        value_temp = []

        for key, value in info_dict.items():
            key_temp.append(key)
            value_temp.append(value)
        df: DataFrame = pd.DataFrame(
            data={"indicator": key_temp, "value": value_temp})
        return df

    @staticmethod
    def get_technical_indicator(elem: SearchObj, interval: str) -> DataFrame:
        if interval is not None:
            df: DataFrame = elem.retrieve_technical_indicators(
                interval=interval)
            return df

    def get_quotes(self) -> list[Any]:
        quotes: list[Any] = []
        for t in self.__ticker_li:
            quotes.append(
                investpy.search_quotes(
                    text=t,
                    products=[self.__sector],
                    countries=self.__country,
                    n_results=self.__n_result
                )
            )
        return quotes

    def technical_indicator_to_csv(self) -> None:
        for e in self.get_quotes():
            info_df = self.get_info(elem=e)
            technical_df = self.get_technical_indicator(
                elem=e, interval=self.__interval)
            combined_df: DataFrame = pd.concat(
                [info_df, technical_df], ignore_index=True
            )
            self.save_to_csv(
                df=combined_df, file_name=e.name, desc="technical_indicator"
            )

    def get_technical_idx(self) -> DataFrame | None:
        for t in self.__ticker_li:
            ma_df = investpy.moving_averages(
                name=t,
                country=self.__country[0],
                product_type=self.__sector,
                interval=self.__interval,
            )
            pv_point_df = investpy.pivot_points(
                name=t,
                country=self.__country[0],
                product_type=self.__sector,
                interval=self.__interval,
            )
            combined_df = pd.concat([ma_df, pv_point_df], axis=1)
            self.save_to_csv(df=combined_df, file_name=t, desc='technical_idx')

    def get_crypto_list_or_overview(self) -> None:
        match self.__search_type:
            case SearchTypes.GET_CRYPTO_LIST:
                crypto_list: list[str] = investpy.get_cryptos_list()
                data = {'crypto': crypto_list}
                self.save_to_csv(df=pd.DataFrame(data=data),
                                 file_name=f"cryto_list.csv", desc="crypto_list")

            case SearchTypes.GET_CRYPTO_OVERVIEW:
                overview: DataFrame = investpy.get_cryptos_overview(
                    n_results=self.__n_result)
                self.save_to_csv(df=overview, desc="crypto_overview",
                                 file_name=f"crypto_overview.csv")

    def get_each_info_or_historical(self) -> None:
        for t in self.__ticker_li:
            match self.__search_type:
                case SearchTypes.GET_CRYPTO_INFO:
                    info = investpy.get_crypto_information(crypto=t)
                    self.save_to_csv(df=pd.DataFrame(
                        info), file_name=f"{t}_info.csv", desc="crypto_info")

                case SearchTypes.GET_CRYPTO_HISTORICAL:
                    historical = investpy.get_crypto_historical_data(
                        crypto=t, from_date=self.__start, to_date=self.__end)

                    if isinstance(historical, DataFrame):
                        self.save_to_csv(
                            df=historical, desc="crypto_historical", file_name=f"{t}_historical.csv")

    def get_efts_info_or_countries(self) -> None:
        match self.__search_type:
            case SearchTypes.GET_ETF_LIST:
                all_efts: list[str] = investpy.get_etfs_list(
                    country=self.__country)
                d = {'etf': all_efts}
                self.save_to_csv(df=pd.DataFrame(data=d),
                                 file_name=f"etf_list.csv", desc="etf_list")

            case SearchTypes.GET_ETF_COUNTRIES:
                etf_countries: list[str] = investpy.get_etf_countries()
                d = {'etf_countries': etf_countries}
                self.save_to_csv(df=pd.DataFrame(
                    data=d), file_name=f"etf_countries.csv", desc="etf_countries")

    def get_etfs_info_or_historical(self) -> None:
        for t in self.__ticker_li:
            match self.__search_type:
                case SearchTypes.GET_ETF_INFO:
                    etf_info = investpy.get_etf_information(
                        etf=t, country=self.__country[0])

                    if isinstance(etf_info, DataFrame):
                        self.save_to_csv(
                            df=etf_info, desc='etf_info', file_name=f"{t}_info.csv")

                case SearchTypes.GET_ETF_HISTORICAL:
                    etf_historical = investpy.get_etf_historical_data(
                        country=self.__country[0],
                        etf=t,
                        from_date=self.__start,
                        to_date=self.__end,
                        interval=self.__interval
                    )

                    if isinstance(etf_historical, DataFrame):
                        self.save_to_csv(
                            df=etf_historical, desc='etf_historical', file_name=f"{t}_historical.csv")

    def get_commodities_info_or_historical(self) -> None:
        for t in self.__ticker_li:
            match self.__search_type:
                case SearchTypes.GET_COMMO_INFO:
                    get_commo_info = investpy.get_commodity_information(
                        commodity=t, country=self.__country[0])

                    if isinstance(get_commo_info, DataFrame):
                        self.save_to_csv(
                            df=get_commo_info, desc="commodity_info", file_name=f"{t}_info.csv")

                case SearchTypes.GET_COMMO_HISTORICAL:
                    commo_historical = investpy.get_commodity_historical_data(
                        commodity=t, country=self.__country, interval=self.__interval, from_date=self.__start, to_date=self.__end
                    )

                    if isinstance(commo_historical, DataFrame):
                        self.save_to_csv(
                            df=commo_historical, file_name='commodity_historical', desc="commodity_historical",)

    def get_commodities_by_group(self) -> None:
        for t in self.__ticker_li:
            match self.__search_type:
                case SearchTypes.GET_COMMO_LIST:
                    commo_list = investpy.get_commodities_list(group=t)
                    get_commo_group = investpy.get_commodity_groups()
                    d = {'commodity': commo_list,
                         'commodity_group': get_commo_group}
                    self.save_to_csv(df=pd.DataFrame(
                        data=d), file_name=f"commodity_list_and_group.csv", desc="commodity_list_and_group")

                case SearchTypes.GET_COMMO_BY_GROUP:
                    get_commo = investpy.get_commodities(group=t)
                    self.save_to_csv(df=pd.DataFrame(
                        data=get_commo), file_name=f"{t}_list.csv", desc="commodity_list")

                case SearchTypes.GET_COMMO_OVERVIEW_BY_GROUP:
                    commo_overview = investpy.get_commodities_overview(group=t)
                    self.save_to_csv(
                        df=commo_overview, desc="commodity_overview", file_name=f"{t}_overview.csv")
