from typing import Optional, Union
from src.sel.controller import FacebookController
from src.bs.handler import DataHandler


# todo news_run func with soup

class Container:
    run_fb = False

    def __enter__(self):
        return Container.run_fb

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
    def run_facebook(cls,
                     instance: FacebookController,
                     drag_count_or_infinite: Union[int, bool],
                     file_name: str,
                     kind: str,
                     year: Optional[int] = None,
                     search_keyword: Optional[str] = None,
                     scrape_count: int = 1) -> None:
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
            # when debugging, close=False
            # instance.delete_all_cookies()
            instance.close_browser(close=False)

    @classmethod
    def switch_fb_run(cls, run: bool = False):
        if run:
            print('Facebook is running')
            Container.run_fb = run
            return Container.run_fb
        else:
            print('Passing Facebook Parsing')
            return Container.run_fb

    @classmethod
    def extracting_keyword(cls):
        pass

    @classmethod
    def run_investing(cls):
        pass

    @classmethod
    def news_run(cls):
        pass
