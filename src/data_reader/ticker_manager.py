from src.globals.inputs import *
from src.data_reader.ticker_controller import TickerController


class TickerManager:
    @classmethod
    def return_ticker_ins_li(cls):
        instance_li = []
        for i in range(len(time_set.keys())):
            ticker_instance = TickerController(
                source=tickers[f'group{i + 1}']['source'],
                ticker_li=tickers[f'group{i + 1}']['tickers_group'],
                time_data=time_set[f'set{i + 1}']
            )
            instance_li.append(ticker_instance)
        return instance_li
