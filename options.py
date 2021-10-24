from inputs import *
from src.scraper.helper import Container
from src.tickers.container import TickerContainer

# Facebook options
RUN_FB = Container.run_fb_switch(run=False)
Container.set_headless(headless=False)
Container.kill_browser(kill=True)

# Pdr options
PARSE_TICKER_ONLY = TickerContainer.parse_ticker_switch(run=True)


def return_ticker_ins_li():
    ticker_group_count = len(tickers.keys())
    instance_li = []
    for i in range(ticker_group_count):
        ticker_instance = TickerContainer(
            source=tickers[f'group{i + 1}']['source'],
            ticker_li=tickers[f'group{i + 1}']['tickers'],
            time=time_set[f'set{i + 1}']
        )
        instance_li.append(ticker_instance)
    return instance_li
