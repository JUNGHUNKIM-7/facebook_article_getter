import os
import time
from dotenv import load_dotenv
from typing import Optional, Union, List, Tuple

from selenium import webdriver as driver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from src.files import FileManager


class FacebookController(driver.Firefox):
    load_dotenv()

    def __init__(self, loc: str, person_name: str, person_info: Optional[str] = None,
                 driver_path: str = r'data_getter\src\geckodriver.exe',
                 close: bool = False):
        # settings
        os.environ["PATH"] += driver_path
        # options = driver.FirefoxOptions()
        # options.headless()

        # vars
        self.__id = os.getenv('FB_BACK')
        self.__password = os.getenv('FB_PASS')
        self.loc = loc
        self.person_name = person_name
        self.person_info = person_info
        self.close = close
        super(FacebookController, self).__init__()

        self.implicitly_wait(5)  # default 8
        self.maximize_window()

    def close_browser(self, close: bool = False) -> None:
        self.close = close
        if self.close is True:
            time.sleep(3)
            self.quit()

    def login(self) -> None:
        self.get(self.loc)
        self.find_element_by_id('email').send_keys(self.__id)
        time.sleep(1)

        self.find_element_by_id('pass').send_keys(self.__password)
        time.sleep(1)

        btn = self.find_element_by_css_selector('button[type="submit"]')
        btn.click()

    def search_person(self) -> None:
        search_bar = self.find_element_by_css_selector('input[spellcheck="false"]')
        search_bar.click()
        search_bar.send_keys(self.person_name)
        time.sleep(2)

        spans = self.find_elements_by_class_name('ojkyduve')

        for span in spans:
            cond = span.get_attribute('innerHTML').strip()
            if self.person_info in cond:
                span.click()
                break
            else:
                raise NoSuchElementException

    # if blocked
    def page_refresh(self) -> None:
        btn = self.find_element_by_css_selector('div[aria-label="페이지 새로 고침"]')
        btn.click()
        time.sleep(1)

    def search_posts(self, year: Optional[int] = None, search_keyword: Optional[str] = None) -> None:
        if year and search_keyword is None:
            def see_by_year() -> None:
                a = self.find_element_by_css_selector('a[href^="/search/posts"]')
                a.click()
                time.sleep(1)

                switch = self.find_element_by_css_selector('input[aria-label="최근 게시물"]')
                switch.click()
                time.sleep(1)

                divs = self.find_elements_by_css_selector('div[aria-haspopup="listbox"]')[0]
                divs.click()
                time.sleep(2)

                options = self.find_elements_by_css_selector('div[role="option"]')
                for option in options:
                    if f'{year}년' == option.get_attribute('innerText').strip():
                        option.click()
                        time.sleep(2)
                        break
                    else:
                        raise Exception("Not Found AnyOption")

            see_by_year()
        elif year is None and search_keyword:
            def search_latest_with_sub_keyword() -> None:
                btn = self.find_element_by_css_selector(f'div[aria-label="{self.person_name}님의 게시물 검색"]')
                btn.click()
                time.sleep(1)

                input_field = self.find_element_by_css_selector(
                    f'input[aria-label="{self.person_name}님의 게시물, 사진 및 태그에서 검색"]')
                input_field.send_keys(search_keyword)
                input_field.send_keys(Keys.ENTER)

                time.sleep(1)
                wrapper = self.find_elements_by_class_name('dbvibxzo')[1]
                div = wrapper.find_elements_by_class_name('qzhwtbm6')[1]
                switch = div.find_element_by_tag_name('input')
                switch.click()

            search_latest_with_sub_keyword()
        else:
            def see_latest_all() -> None:
                a = self.find_element_by_css_selector('a[href^="/search/posts"]')
                a.click()
                time.sleep(1)

                switch = self.find_element_by_css_selector('input[aria-label="최근 게시물"]')
                switch.click()

            see_latest_all()

    # 스크롤 가능 elem 수 결정 남.
    def bottom_end(self, drag_count_or_infinite: Union[int, bool] = 1):
        # default : 3~4 ea
        # key_END 1 time => btn(2~3?) * count_or_infinite
        if drag_count_or_infinite is not bool:
            for _ in range(drag_count_or_infinite):
                time.sleep(2)
                self.find_element_by_tag_name('body').send_keys(Keys.END)
            # todo, drag_count is bool, while loop
            # todo 바닥찍기

            self.find_element_by_tag_name('body').send_keys(Keys.HOME)
        else:

            pass

    def position_to_middle(self, element: WebElement) -> None:
        desired_y = (element.size['height'] / 2) + element.location['y']
        current_y = (self.execute_script('return window.innerHeight') / 2) + self.execute_script(
            'return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(2)

    def wrapper_gen(self, web_elements: List[WebElement], dates: Optional[List[WebElement]] = None) \
            -> Union[Tuple[int, WebElement, WebElement], Tuple[int, WebElement]]:
        if dates:
            for (i, wrapper_elem), date in zip(enumerate(web_elements), dates):
                yield i, wrapper_elem, date
        else:
            for i, wrapper_elem in enumerate(web_elements):
                yield i, wrapper_elem

    def saved_file_by_moving(self,
                             root: str,
                             file_name: str,
                             kind: str,
                             year: Optional[int] = None,
                             search_keyword: Optional[str] = None,
                             scrape_count: int = 1) -> None:
        feed = self.find_element_by_css_selector('div[role="feed"]')

        try:
            time.sleep(2)
            if year and not search_keyword:
                wrappers = feed.find_elements_by_css_selector('div[data-ad-comet-preview="message"]')
                links = feed.find_elements_by_css_selector('a[href^="https://www.facebook.com/"]')
                missing_btn = 0

                # generator
                year_wrapper_gen = self.wrapper_gen(web_elements=wrappers, dates=links)

                for _ in range(scrape_count):
                    i, wrapper, post_date = next(year_wrapper_gen)
                    print(f"Wrapper {i + 1} is reading data")

                    # moving
                    self.position_to_middle(element=wrapper)

                    # see more btn click
                    button_check = len(wrapper.find_elements_by_css_selector('div[role="button"]'))
                    if button_check == 0:
                        missing_btn += 1
                        continue
                    else:  # button_check > 0
                        btn = wrapper.find_element_by_css_selector('div[role="button"]')
                        btn.click()
                        time.sleep(1.5)

                    # parsing and save files
                    print(f'Start Scraping {i + 1}')
                    # todo fix post_date!
                    FileManager.get_data_as_file(i=i,
                                                 web_elems_or_data_list=wrapper,
                                                 post_date=post_date,
                                                 root=root,
                                                 file_name=file_name,
                                                 kind=kind)
                    print(f'Completed: {i + 1}')

                print(f'Wrapper: {scrape_count} are totally saved, MissingBtn:{missing_btn}')
            elif not year and search_keyword:
                wrappers = feed.find_elements_by_css_selector('div[role="article"]')
                keyword_wrapper_gen = self.wrapper_gen(web_elements=wrappers)

                for _ in range(scrape_count):  # each wrapper
                    i, wrapper = next(keyword_wrapper_gen)
                    link = wrapper.find_element_by_css_selector('a[role="link"]')
                    print(f"Wrapper {i + 1} is reading data")

                    # moving
                    self.position_to_middle(element=wrapper)

                    link.click()
                    time.sleep(1)

                    # handling pop up
                    big_wrapper = self.find_element_by_css_selector(
                        'div[style="border-radius: max(0px, min(8px, -999900% - 39996px + 999900vw)) / 8px;"]')
                    # area-label 중 : 을 포함하는 태그.
                    # document.querySelectorAll('a[aria-label*=":"]')
                    post_date = big_wrapper.find_element_by_css_selector('a[aria-label*=":"]')
                    posts = big_wrapper.find_elements_by_css_selector('div[style="text-align: start;"]')

                    data = [post_date + "\n"]
                    for post in posts:
                        data.append(post.get_attribute('innerHTML').strip())

                    # parsing and save files
                    print(f'Start Scraping {i + 1}')
                    FileManager.get_data_as_file(i=i,
                                                 web_elems_or_data_list=data,
                                                 post_date=post_date,
                                                 root=root,
                                                 file_name=file_name,
                                                 kind=kind)
                    print(f'Completed: {i + 1}')

                    # out
                    self.back()
                    time.sleep(2)
                print(f'{len(wrappers)} files are totally saved.')
            else:
                raise Exception("Year or Search should be passed to filter posts")
        except Exception as e:
            print(e)
