from typing import Optional, Union, Dict

from src.data_reader.ticker_manager import TickerManager
from src.scraper.controller_fb_working import FacebookController
from src.scraper.controller_soup import SoupController


class InstanceController:
    # tickers
    PARSE_TICKER = True

    # FB
    RUN_FB = True
    HEAD_LESS = True
    BROWSER_STATUS = True

    # Investipy
    RUN_INVESTIPY = True

    # Options
    @classmethod
    def parse_ticker_switch(cls, run: bool = PARSE_TICKER) -> bool:
        if run is False:
            InstanceController.PARSE_TICKER = run
            return InstanceController.PARSE_TICKER
        else:
            return InstanceController.PARSE_TICKER

    @classmethod
    def set_running_fb(cls, run: bool = RUN_FB):
        if run is False:
            InstanceController.RUN_FB = run
            print('Status : Not Facebook')
            return InstanceController.RUN_FB
        else:
            print('Status : Running Facebook')
            return InstanceController.RUN_FB

    @classmethod
    def set_headless(cls, headless: bool = HEAD_LESS):
        if headless is False:
            print('Option : Not Headless')
            InstanceController.HEAD_LESS = headless
            return InstanceController.HEAD_LESS
        else:
            print('Option : On Headless')
            return InstanceController.HEAD_LESS

    @classmethod
    def set_kill_browser(cls, kill: bool = BROWSER_STATUS):
        if kill is False:
            print('Option : Not Kill browser')
            InstanceController.BROWSER_STATUS = kill
            return InstanceController.BROWSER_STATUS
        else:
            print('Option : Kill browser')
            return InstanceController.BROWSER_STATUS

    @classmethod
    def set_investipy(cls, run: bool = PARSE_TICKER) -> bool:
        if run is False:
            InstanceController.PARSE_TICKER = run
            return InstanceController.RUN_INVESTIPY
        else:
            return InstanceController.RUN_INVESTIPY

    # return instance for running
    @classmethod
    def make_instance(cls,
                      key: str,
                      news_channel: Optional[str] = None,
                      options: Dict[str, bool] = None,
                      **kwargs) -> Union[FacebookController, SoupController]:
        if options is None:
            options = {
                'headless': InstanceController.HEAD_LESS,
                'browser_status': InstanceController.BROWSER_STATUS
            }

        if key == 'facebook':
            obj = kwargs.get(key)
            key_li = ['url', 'person_name', 'person_info']
            url, person_name, person_info = [obj.get(key) for key in key_li]
            return FacebookController(loc=url, person_name=person_name, person_info=person_info, options=options)

        elif key == 'cnbc' or key == 'yh' or key == 'trade' or key == 'investing':
            obj = kwargs.get(key)
            if news_channel:
                url = obj.get(news_channel)
                return SoupController(url=url)
        else:
            raise Exception('No Data Found')

    # after that, link instance as arg, then run instance methods
    # run_facebook is instance behaviors wrapper
    @classmethod
    def run_facebook(cls,
                     instance: FacebookController,
                     drag_count_or_infinite: Union[int, bool],
                     file_name: str,
                     kind: str,
                     year: Optional[int] = None,
                     search_keyword: Optional[str] = None,
                     scrape_count: int = 1,
                     ) -> None:
        try:
            print(f"""
                PERSON: {instance.person_name}
                INFO: {instance.person_info}
                YEAR: {year}
                KEYWORD: {search_keyword}
                SCRAP_COUNT: {scrape_count}
                DRAG_STATUS: {drag_count_or_infinite}
                """)
            instance.login()
            instance.search_person()
            instance.search_posts(year=year, search_keyword=search_keyword)
            instance.bottom_end(drag_count_or_infinite=drag_count_or_infinite)
            instance.saved_file_by_moving(
                file_name=file_name,
                kind=kind,
                scrape_count=scrape_count,
                year=year,
                search_keyword=search_keyword)
        except Exception as e:
            raise e
        finally:
            if InstanceController.BROWSER_STATUS:
                instance.delete_all_cookies()
                instance.close_browser()
            else:
                print('Running Finished')

    @classmethod
    def run_news(cls, instance: SoupController):
        try:
            instance.get_html()
        except Exception as e:
            print(e)

    @classmethod
    def run_data_reader(cls):
        for ticker_ins in TickerManager.return_ticker_ins_li(source='pds'):
            ticker_ins.save_to_csv()

    @classmethod
    def run_investipy(cls):
        for ticker_py_ins in TickerManager.return_ticker_ins_li(source='investipy'):  # return, each instance
            ticker_py_ins.get_technical_combined_to_csv(interval_for_technical_data='monthly')
