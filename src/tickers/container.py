import time
from typing import List, Dict, Tuple, Optional
from datetime import date
import pandas as pd
from pandas import DataFrame
import pandas_datareader as pdr

from file_controller import FileManager
from src.tickers.timedel import TimeContainer


class TickerContainer:
    PARSE_TICKER = False

    @classmethod
    def parse_ticker_switch(cls, on: Optional[bool] = None):
        TickerContainer.PARSE_TICKER = on

    def __init__(self, source: str, ticker_li: List[str], time: Dict[str, str]):
        self.source = source
        self.__ticker_li = ticker_li
        self.__start = TimeContainer(time).start
        self.__end = TimeContainer(time).end
        self.__date_string = TimeContainer.date_string

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
            df = pdr.DataReader(ticker, self.source, self.__start, self.__end)
            time.sleep(1)
            df: DataFrame = pd.DataFrame(df)
            df.to_csv(fr'{file_loc}\{ticker}_{str(self.__start)}_{str(self.__end)}')
            print(f'download {ticker} -{self.__start} | {self.__date_string} | +{self.__end} done')
