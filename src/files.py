import os
import time
from typing import List, Optional, Union, Callable, Tuple
from datetime import date

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from date import return_delta


# todo
# read files 함수


class FileManager:
    @classmethod
    def make_file(cls,
                  articles: List[str],
                  posting_date: str,
                  file_name: str,
                  kind: str,
                  idx: Optional[int] = None) -> None:

        curr = os.getcwd()
        curr = os.path.dirname(curr)
        proj_folder = 'files'
        stored_file_loc = os.path.join(curr, proj_folder)
        delta = return_delta(posting_date)

        if idx is not None:
            with open(
                    fr'{stored_file_loc}\{idx}_{file_name}_{str(date.today() - delta)}.{kind}',
                    'w',
                    encoding='utf-8') as f:
                for article in articles:
                    f.write(f'{article}\n')

    @classmethod
    def get_data_as_file(cls, i: int,
                         web_elems_or_data_list: Union[WebElement, List[str]],
                         post_date: Union[WebElement, str],
                         file_name: str,
                         kind: str):
        try:
            if web_elems_or_data_list is not List[str]:
                article_list = []
                divs = web_elems_or_data_list.find_elements(By.CSS_SELECTOR, 'div[style="text-align: start;"]')
                date_from_web_elem = post_date.get_attribute('innerText').strip()

                if len(divs) != 0:
                    for div in divs:
                        time.sleep(0.5)
                        article_list.append(div.get_attribute('innerHTML').strip())
                FileManager.make_file(articles=article_list,
                                      posting_date=date_from_web_elem,
                                      file_name=file_name,
                                      kind=kind,
                                      idx=i + 1)
            else:
                FileManager.make_file(articles=web_elems_or_data_list,
                                      posting_date=post_date,
                                      file_name=file_name,
                                      kind=kind,
                                      idx=i + 1)
        except Exception as e:
            print(e)

    @classmethod
    def reading_files_from_dir(cls):
        pass
