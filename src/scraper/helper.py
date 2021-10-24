from typing import Optional, Union
from src.scraper.controller.controller_fb import FacebookController
from src.scraper.controller.controller_soup import DataHandler


# todo news_run func with soup

class Container:
    RUN_FB = False
    HEAD_LESS = False
    BROWSER_STATUS = False

    def __enter__(self):
        return Container.RUN_FB

    @classmethod
    def make_instance(cls, key: str, news_channel: Optional[str] = None, **kwargs) \
            -> Union[FacebookController, DataHandler]:
        if key == 'facebook':
            obj = kwargs.get(key)
            key_li = ['url', 'person_name', 'person_info']
            url, person_name, person_info = [obj.get(key) for key in key_li]
            return FacebookController(loc=url, person_name=person_name, person_info=person_info)

        elif key == 'cnbc' or key == 'yh' or key == 'trade':
            obj = kwargs.get(key)
            if news_channel:
                url = obj.get(news_channel)
                return DataHandler(url=url)
        else:
            raise Exception('No Data Found')

    @classmethod
    def run_fb_switch(cls, run: bool = False):
        if run:
            print('Status : run Facebook')
            Container.RUN_FB = run
            return Container.RUN_FB
        else:
            print('Status : off Facebook')
            return Container.RUN_FB

    @classmethod
    def set_headless(cls, headless: bool = False):
        if headless:
            print('Option : headless')
            Container.HEAD_LESS = headless
            return Container.HEAD_LESS
        else:
            print('Option : set Headless')
            return Container.HEAD_LESS

    @classmethod
    def kill_browser(cls, kill: bool = False):
        if kill:
            print('Option : kill browser')
            Container.HEAD_LESS = kill
            return Container.BROWSER_STATUS
        else:
            print('Option : keep running browser')
            return Container.BROWSER_STATUS

    @classmethod
    def run_facebook(cls,
                     instance: FacebookController,
                     drag_count_or_infinite: Union[int, bool],
                     file_name: str,
                     kind: str,
                     year: Optional[int] = None,
                     search_keyword: Optional[str] = None,
                     scrape_count: int = 1,
                     head_less=HEAD_LESS,
                     browser_status=BROWSER_STATUS,
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
            if not head_less:
                instance.login()
                instance.search_person()
                instance.search_posts(search_keyword=search_keyword)
                instance.bottom_end(drag_count_or_infinite=drag_count_or_infinite)
                instance.saved_file_by_moving(
                    file_name=file_name,
                    kind=kind,
                    scrape_count=scrape_count,
                    year=year,
                    search_keyword=search_keyword)
            else:
                FacebookController.HEADLESS = True
                instance.login()
                instance.search_person()
                instance.search_posts(search_keyword=search_keyword)
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
            # instance.delete_all_cookies()
            if browser_status:
                instance.close_browser(close=browser_status)

    @classmethod
    def extracting_keyword(cls):
        pass

    @classmethod
    def run_investing(cls):
        pass

    @classmethod
    def news_run(cls):
        pass
