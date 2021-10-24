from inputs import *
from src.scraper.helper import Container
from file_controller import FileManager

from src.tickers.container import TickerContainer

# ------Debug-------
# 2. 2020 이하 버튼 클릭 문제
# no found any btn
# ------Debug-------

# -----instance-----
fb_ins = Container.make_instance(key='facebook', **fb)
news_ins = Container.make_instance(key='yh', news_channel='world', **news)

ti1 = TickerContainer(
    source='yahoo',
    ticker_li=tickers.get("group1"),
    time=time
)
# -----instance-----

# todo
# year = 2021 이하 작동안함

if __name__ == '__main__':
    # pandas data_Reader
    parse_ticker_only = TickerContainer.parse_ticker_switch(on=True)

    # Facebook options
    run_fb = Container.run_fb_switch(run=False)
    Container.set_headless(headless=False)
    Container.kill_browser(kill=False)

    try:
        if parse_ticker_only and not run_fb:
            ti1.save_to_csv()
        elif not parse_ticker_only and not run_fb:
            pass
            # FileManager.reading_files_from_dir()
            # Container.extracting_keyword()
            # Container.run_investing()
            # Container.news_run()
        else:
            Container.run_facebook(instance=fb_ins,
                                   year=2021,
                                   # search_keyword="금리",
                                   drag_count_or_infinite=1,
                                   file_name='oh',
                                   kind='txt',
                                   scrape_count=2)
            FileManager.reading_files_from_dir()
            Container.extracting_keyword()
            Container.run_investing()
            Container.news_run()
    except Exception as e:
        print(e)
