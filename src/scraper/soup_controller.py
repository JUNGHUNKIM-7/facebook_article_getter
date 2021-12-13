from typing import Dict, List, Union, Any
from bs4 import BeautifulSoup
import requests as r

from src.utils.option_container import OptionContainer


class SoupController:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
    }

    def __init__(self, url: str) -> None:
        self.res = r.get(url, headers=SoupController.headers)
        try:
            self.res.raise_for_status()
            self.soup = BeautifulSoup(self.res.text, 'lxml')
        except Exception as e:
            print(e)

    def get_html(self):
        stored_loc = OptionContainer.save_path()
        with open(fr'{stored_loc}\page.html', 'w', encoding='utf-8') as f:
            f.write(self.soup.prettify())

    def get_elem(self, tag: Union[str, List[str]], attribute_dict: Dict[str, Any], find_all: bool = False):
        def return_attrs():
            for key, val in attribute_dict.items():
                return {key: val}

        # 수프 객체 리턴
        if not find_all:
            return self.soup.find(tag, attrs=return_attrs())
        else:
            return self.soup.find_all(tag, attrs=return_attrs())
