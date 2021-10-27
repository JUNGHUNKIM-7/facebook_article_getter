import investpy
import pandas as pd
from pandas import DataFrame
from investpy.utils.search_obj import SearchObj

from src.globals.time_container import TimeContainer
from typing import Dict, Any, List, Optional

from src.globals.file_controller import FileManager


class InvestipyController:
    def __init__(self,
                 ticker_li: List[str],
                 time_data: Dict[str, Any],
                 products: Optional[List[str]] = None,
                 country: Optional[List[str]] = None,
                 n_result: Optional[int] = None):
        self.ticker_li = ticker_li

        if country is None:
            self.country = ['united states']

        if products is None:
            self.products = ['stocks']

        if n_result is None:
            self.n_result = 1

        if time_data.get('before') is not None:
            self.__start = TimeContainer(time_data).start
        else:
            self.__start = TimeContainer(time_data).base

        if time_data.get('after') is not None and time_data.get('specific') is None:
            self.__end = TimeContainer(time_data).end
        elif time_data.get('after') is None and time_data.get('specific') is not None:
            self.__end = TimeContainer(time_data).specific
        elif time_data.get('before') and time_data.get('base') and not time_data.get('after') and not time_data.get(
                'specific'):
            self.__end = TimeContainer(time_data).base
        else:
            self.__end = TimeContainer(time_data).today

        sy, sm, sd = [elem for elem in str(self.__start).split('-')]
        ey, em, ed = [elem for elem in str(self.__end).split('-')]
        self.__start = f'{sd}/{sm}/{sy}'
        self.__end = f'{ed}/{em}/{ey}'

    def container(self) -> List[SearchObj]:
        quotes: List[SearchObj] = []
        for ticker in self.ticker_li:
            quotes.append(investpy.search_quotes(text=ticker, products=self.products,
                                                 countries=self.country, n_results=self.n_result)
                          )
        return quotes

    def get_historical_data(self) -> None:
        for tickers in self.ticker_li:
            country = self.country[0]
            df = investpy.get_stock_historical_data(stock=tickers,
                                                    country=country,
                                                    from_date=self.__start,
                                                    to_date=self.__end)
            print(df)  # todo

    def get_info(self, elem) -> DataFrame:
        dict: Dict[str, Any] = elem.retrieve_information()  # return dict
        key_temp = []
        value_temp = []

        for key, value in dict.items():
            key_temp.append(key)
            value_temp.append(value)
        df: DataFrame = pd.DataFrame(data={'indicator': key_temp, 'value': value_temp})
        return df

    def get_technical_info(self, elem, interval: str) -> DataFrame:
        df: DataFrame = elem.retrieve_technical_indicators(interval=interval)  # return dataframes
        return df

    def get_technical_combined_to_csv(self, interval_for_technical_data: str) -> None:
        loc = FileManager.get_save_path(r'data_getter\files')
        for elem in self.container():
            info_df = self.get_info(elem=elem)
            technical_df = self.get_technical_info(elem=elem, interval=interval_for_technical_data)
            combined_df: DataFrame = pd.concat([info_df, technical_df], ignore_index=True)
            combined_df.to_csv(f"{loc}\{elem.name}'s_info_with_Technical_info.csv")
            print(f"Technical_info: {elem.name} downloaded")
