from typing import Dict, List, Union
from bs4 import BeautifulSoup
import requests as r


# import markdown as m
# from prettytable import PrettyTable


class DataHandler:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
    }

    def __init__(self, url: str) -> None:
        self.res = r.get(url, headers=DataHandler.headers)
        try:
            self.res.raise_for_status()
            self.soup = BeautifulSoup(self.res.text, 'lxml')
        except ConnectionError as c:
            print(c)

    def for_test(self, tag: str, attrs: Dict[str, str]):
        print(self.soup.prettify())
        print(self.soup.find_all(tag, attrs))

    def get_elem(self, tag: Union[str, List[str]], find_all: bool = False, **kwargs: [str, str]):
        def get_key_val():
            for k, v in kwargs.items():
                print(k, v)
                return k, v

        key, val = get_key_val()

        if not find_all:
            return self.soup.find(tag, attrs={key: val})
        else:
            return self.soup.find_all(tag, attrs={key: val})

    # def parse_data(self, find_all: bool = False) -> None:
    #     # react dom 에서 작동 불가 = 데이터 없음(None)
    #     soup_ins = DataHandler(url=self.current_url)
    #     obj = {"style": "text-align: start;"}
    #
    #     if not find_all:
    #         article = soup_ins.get_elem(tag='div', find_all=find_all, **obj)
    #         print(article.text)
    #     else:
    #         articles = soup_ins.get_elem(tag='div', find_all=find_all, **obj)
    #         print(articles.text)
