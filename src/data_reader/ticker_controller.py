import time
from typing import List, Dict, Tuple, Any
from datetime import date

import pandas as pd
from pandas import DataFrame
import pandas_datareader as pdr

from src.globals.file_controller import FileManager
from src.globals.time_container import TimeContainer


class TickerController:
    def __init__(self, source: str, ticker_li: List[str], time_data: Dict[str, Any]):
        self.__source = source
        self.__ticker_li = ticker_li
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

    @staticmethod
    def handle_csv(df, new_cols, file_loc, ticker, start, end):
        column_set = zip(df.columns, new_cols)
        [df.rename(columns={old: new}, inplace=True) for old, new in column_set]
        df = df.round(decimals=3)

        df.set_index('일자', inplace=True)
        df.to_csv(fr'{file_loc}\{ticker}_{str(start)}_{str(end)}.csv')
        print(f'{ticker} {start} to {end} downloaded')

    def save_to_csv(self) -> None:
        file_loc = FileManager.get_save_path('data_getter\\files')
        for ticker in self.__ticker_li:
            if self.__source == 'yahoo':
                df = pdr.DataReader(ticker, self.__source, self.__start, self.__end)
                time.sleep(1)
                df: DataFrame = pd.DataFrame(df)

                df.reset_index(inplace=True)
                df.index.name = 'index'
                df = pd.concat([df, df[['Close', 'Adj Close']].diff().rename(
                    {'Close': 'Close Diff', 'Adj Close': 'Adj Close Diff'}, axis=1)], axis=1)
                new_cols = ['일자', '일별최고가', '일별최저가', '시작가', '종가', '거래량', '조정종가', '전일대비종가(%)', '전일대비조정종가(%)']

                TickerController.handle_csv(df, new_cols, file_loc, ticker, self.__start, self.__end)

            if self.__source == 'naver':
                df = pdr.DataReader(ticker, self.__source, self.__start, self.__end)
                time.sleep(1)
                df: DataFrame = pd.DataFrame(df)

                df.reset_index(inplace=True)
                df.index.name = 'index'

                df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(
                    int)

                df['shifted'] = df['Close'].shift(periods=1)
                df['전일대비종가(%)'] = ((df['Close'] - df['shifted']) / df['shifted']) * 100
                df.drop(columns='shifted', inplace=True)
                new_cols = ['일자', '시작가', '일별최고가', '일별최저가', '종가', '거래량']

                TickerController.handle_csv(df, new_cols, file_loc, ticker, self.__start, self.__end)
