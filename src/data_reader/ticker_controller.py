import time
from typing import List, Dict, Tuple, Any
from datetime import date
import pandas as pd
from pandas import DataFrame
import pandas_datareader as pdr

from src.globals.file_controller import FileManager
from src.data_reader.time_container import TimeContainer


class TickerController:
    def __init__(self, source: str, ticker_li: List[str], time_data: Dict[str, Any]):
        self.__source = source
        self.__ticker_li = ticker_li
        if time_data.get('before') is None:
            self.__start = TimeContainer(time_data).base
        else:
            self.__start = TimeContainer(time_data).start

        if time_data.get('after') is None:
            self.__end = TimeContainer(time_data).today
        else:
            self.__end = TimeContainer(time_data).end

    @property
    def tickers(self) -> List[str]:
        return self.__ticker_li

    @tickers.setter
    def tickers(self, other_li: List[str]) -> None:
        self.__ticker_li = other_li

    @property
    def time_data(self) -> Tuple[date, date]:
        return self.__start, self.__end

    @time_data.setter
    def time_data(self, other_dict: Dict[str, str]) -> None:
        TimeContainer(other_dict)

    def save_to_csv(self) -> None:
        file_loc = FileManager.get_save_path('data_getter\\files')
        for ticker in self.__ticker_li:
            df = pdr.DataReader(ticker, self.__source, self.__start, self.__end)
            time.sleep(1)
            df: DataFrame = pd.DataFrame(df)
            df.to_csv(fr'{file_loc}\{ticker}_{str(self.__start)}_{str(self.__end)}')
            print(f'{ticker} {self.__start} to {self.__end} downloaded')
