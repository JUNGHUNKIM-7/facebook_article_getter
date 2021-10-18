from inputs import *
from typing import Optional, Union
from sel.controller import FacebookController
from bs.handler import DataHandler


def make_ins(key: str, news_channel: Optional[str] = None, **kwargs) \
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


fb_ins1 = make_ins(key='facebook', **fb)
news_ins1 = make_ins(key='yh', news_channel='world', **news)


def fb_run() -> None:
    try:
        fb_ins1.login()
        fb_ins1.search_person()
        fb_ins1.search_posts(year=2021)
        fb_ins1.bottom_end(count_or_infinite=2)
        fb_ins1.saved_file_by_moving(file_name='oh')
    except Exception as e:
        raise e
    finally:
        fb_ins1.close_browser(close=False)


def news_run():
    pass


if __name__ == '__main__':
    fb_run()
    news_run()
