import time
from typing import List, Optional, Union
from datetime import date

from selenium.webdriver.remote.webelement import WebElement


class FileManager:
    @classmethod
    def make_file(cls, articles: List[str], root: str, file_name: str, kind: str, idx: Optional[int] = None):
        if idx is not None:
            with open(f'{root}{idx}_{file_name}_{str(date.today())}.{kind}', 'w', encoding='utf-8') as f:
                for article in articles:
                    f.write(f'{article}\n')
        else:
            pass  # todo default behavior

    @classmethod
    def get_data_as_file(cls, i: int,
                         web_elems_or_data_list: Union[WebElement, List[str]],
                         post_date: WebElement,
                         root: str,
                         file_name: str,
                         kind: str):
        try:
            if web_elems_or_data_list is not List[str]:
                article_list = []
                divs = web_elems_or_data_list.find_elements_by_css_selector('div[style="text-align: start;"]')
                if len(divs) != 0:
                    article_list.append(post_date.get_attribute('innerText').strip())
                    for div in divs:
                        time.sleep(1)
                        a = div.find_elements_by_css_selector('a[role="link"]')
                        if len(a) == 0:
                            article_list.append(div.get_attribute('innerHTML').strip())
                        else:
                            if len(div.find_elements_by_tag_name('a')) != 0:
                                article_list.append(
                                    div.find_element_by_tag_name('a').get_attribute('innerHTML').strip())
                                continue
                            article_list.append(post_date.get_attribute('innerHTML').strip())

                FileManager.make_file(articles=article_list,
                                      root=root,
                                      file_name=file_name,
                                      kind=kind,
                                      idx=i + 1)
            else:
                FileManager.make_file(articles=web_elems_or_data_list,
                                      root=root,
                                      file_name=file_name,
                                      kind=kind,
                                      idx=i + 1)
        except Exception as e:
            print(e)

    @classmethod
    def read_file(cls, path: str):
        pass
    # todo - read files
