import time
from typing import Any,  Optional, Union
from datetime import date

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from options import OptionContainer

from src.scraper.fb_posting_date_helper import return_delta

class FileHandler:
    @classmethod
    def make_file(
        cls,
        articles: list[str],
        posting_date: str,
        kind: str,
        file_name,
        idx: Optional[int] = None,
    ) -> None:

        stored_file_loc = OptionContainer.save_path(file_name)
        delta = return_delta(posting_date)

        if idx is not None and delta is not None:
            with open(
                fr"{stored_file_loc}\{idx}_{file_name}_{str(date.today() - delta)}.{kind}",
                "w",
                encoding="utf-8",
            ) as f:
                for article in articles:
                    f.write(f"{article}\n")

    @classmethod
    def get_data_as_file(
        cls,
        i: int,
        web_elems_or_data_list: Union[WebElement, list[str]],
        post_date: Union[WebElement, str],
        file_name: str,
        kind: str,
    ):
        try:
            if type(web_elems_or_data_list) is WebElement:
                article_list = []
                date_data = ""
                divs: list[WebElement] = web_elems_or_data_list.find_elements(
                    By.CSS_SELECTOR, 'div[style="text-align: start;"]'
                )

                if type(post_date) is WebElement:
                    date_from_web_elem: Any = post_date.get_attribute(
                        "innerText"
                    ).strip()
                    date_data = date_from_web_elem

                if len(divs) != 0:
                    for div in divs:
                        time.sleep(0.5)
                        article_list.append(
                            div.get_attribute("innerHTML").strip())

                FileHandler.make_file(
                    articles=article_list,
                    posting_date=date_data or "",
                    file_name=file_name,
                    kind=kind,
                    idx=i + 1,
                )

            else:
                if type(web_elems_or_data_list) is list[str] and type(post_date) is str:
                    FileHandler.make_file(
                        articles=web_elems_or_data_list,
                        posting_date=post_date,
                        file_name=file_name,
                        kind=kind,
                        idx=i + 1,
                    )
        except Exception as e:
            print(e)
