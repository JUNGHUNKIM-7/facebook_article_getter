from typing import Optional, Union, Dict
from data_reader.investipy_container import InvestipyContainer
from data_reader.data_reader_container import DataReaderContainer

from src.utils.option_container import OptionContainer
from src.data_reader.instance_helper import TickerInstanceHelper
from scraper.fb_controller import FacebookController
from scraper.soup_controller import SoupController


class InstanceRunner:
    @classmethod
    def make_instance(
        cls,
        key: str,
        news_channel: Optional[str] = None,
        options: Dict[str, bool] = None,
        **kwargs,
    ) -> Union[FacebookController, SoupController, None]:
        obj = kwargs.get(key)
        if options is None:
            options = {
                "headless": OptionContainer.HEAD_LESS,
                "browser_status": OptionContainer.BROWSER_STATUS,
            }

        if obj != None:
            if key == "facebook":
                key_li = ["url", "person_name", "person_info"]
                url, person_name, person_info = [obj.get(key) for key in key_li]
                return FacebookController(
                    loc=url,
                    person_name=person_name,
                    person_info=person_info,
                    options=options,
                )

            elif key == "cnbc" or key == "yh" or key == "trade" or key == "investing":
                if news_channel:
                    url: str = obj[f"{news_channel}"]
                    return SoupController(url=url)
            else:
                raise Exception("No Data Found")

    @classmethod
    def run_facebook(
        cls,
        instance: FacebookController,
        drag_count_or_infinite: Union[int, bool],
        file_name: str,
        kind: str,
        year: Optional[int] = None,
        search_keyword: Optional[str] = None,
        scrape_count: int = 1,
    ) -> None:
        try:
            print(
                f"""
                PERSON: {instance.person_name}
                INFO: {instance.person_info}
                YEAR: {year}
                KEYWORD: {search_keyword}
                SCRAP_COUNT: {scrape_count}
                DRAG_STATUS: {drag_count_or_infinite}
                """
            )
            instance.login()
            instance.search_person()
            instance.search_posts(year=year, search_keyword=search_keyword)
            instance.bottom_end(drag_count_or_infinite=drag_count_or_infinite)
            instance.saved_file_by_moving(
                file_name=file_name,
                kind=kind,
                scrape_count=scrape_count,
                year=year,
                search_keyword=search_keyword,
            )
        except Exception as e:
            raise e
        finally:
            if OptionContainer.BROWSER_STATUS:
                instance.delete_all_cookies()
                instance.close_browser()
            else:
                print("Running Finished")

    @classmethod
    def run_news(cls, instance: SoupController):
        try:
            instance.get_html()
        except Exception as e:
            print(e)

    @classmethod
    def run_data_reader(cls, src="pds") -> None:
        tickers = TickerInstanceHelper.return_ticker_ins_li(source=src)
        if tickers != None:
            for ticker_ins in tickers:
                if type(ticker_ins) is DataReaderContainer:
                    ticker_ins.save_to_csv()

    @classmethod
    def run_investipy(cls, kind: str, src="investipy") -> None:
        tickers = TickerInstanceHelper.return_ticker_ins_li(source=src)
        if tickers != None:
            for ticker_py_ins in tickers:  # return, each instance
                if type(ticker_py_ins) is InvestipyContainer:

                    if kind == "stock":
                        ticker_py_ins.get_technical_indicator_to_scv(interval="monthly")

                    elif kind == "technical":
                        ticker_py_ins.get_technical_to_csv()

                    elif kind == "crypto":
                        ticker_py_ins.get_crypto_to_csv()

                    elif kind == "efts":
                        ticker_py_ins.get_etfs_to_csv()

                    elif kind == "commodities":
                        ticker_py_ins.get_comm_to_csv()

                    else:
                        raise Exception("Invalid Kind")
        else:
            raise Exception("Ticker is None")
