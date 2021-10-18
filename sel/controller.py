import os
import time
from datetime import date
from dotenv import load_dotenv
from typing import Optional, List, Union

from selenium import webdriver as driver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class FacebookController(driver.Firefox):
    load_dotenv()

    def __init__(self, loc: str, person_name: str, person_info: Optional[str] = None,
                 driver_path: str = r'data_getter\sel\geckodriver.exe',
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
        time.sleep(0.5)

        self.find_element_by_id('pass').send_keys(self.__password)
        time.sleep(0.5)

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
                time.sleep(1)
                switch.click()

                divs = self.find_elements_by_css_selector('div[aria-haspopup="listbox"]')[0]
                divs.click()
                time.sleep(1)

                options = self.find_elements_by_css_selector('div[role="option"]')
                for option in options:
                    if f'{year}년' == option.get_attribute('innerText').strip():
                        option.click()
                        time.sleep(1)
                        break
                    else:
                        raise Exception("Not Found AnyOption")

            see_by_year()
        elif year is None and search_keyword:
            def search_latest_with_sub_keyword() -> None:
                btn = self.find_element_by_css_selector(f'div[aria-label="{self.person_name}님의 게시물 검색"]')
                btn.click()
                time.sleep(0.5)

                input_field = self.find_element_by_css_selector(
                    f'input[aria-label="{self.person_name}님의 게시물, 사진 및 태그에서 검색"]')
                input_field.send_keys(search_keyword)
                input_field.send_keys(Keys.ENTER)

                time.sleep(0.5)
                wrapper = self.find_elements_by_class_name('dbvibxzo')[1]
                div = wrapper.find_elements_by_class_name('qzhwtbm6')[1]
                switch = div.find_element_by_tag_name('input')
                switch.click()

            search_latest_with_sub_keyword()
        else:
            def see_latest_all() -> None:
                a = self.find_element_by_css_selector('a[href^="/search/posts"]')
                a.click()
                time.sleep(0.5)

                switch = self.find_element_by_css_selector('input[aria-label="최근 게시물"]')
                switch.click()

            see_latest_all()

    # 스크롤 가능 elem 수 결정 남.
    def bottom_end(self, count_or_infinite: Union[int, bool] = 1):
        # default : 3~4 ea
        # key_END 1 time => btn(2~3?) * count_or_infinite
        if count_or_infinite is False:
            for _ in range(count_or_infinite):
                self.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(1)

            self.find_element_by_tag_name('body').send_keys(Keys.HOME)
            # todo 바닥찍기

    def get_txt(self, i: int, wrapper, post_date, file_name: str):
        def make_file(idx: int, articles: List[str]):
            with open(f'{idx}_{file_name}_{str(date.today())}.txt', 'w', encoding='utf-8') as f:
                for article in articles:
                    f.write(f'{article}\n')

        try:
            article_list = []
            divs = wrapper.find_elements_by_css_selector('div[style="text-align: start;"]')
            if len(divs) != 0:
                article_list.append(post_date.get_attribute('innerText').strip())
                for div in divs:
                    a = div.find_elements_by_css_selector('a[role="link"]')
                    if len(a) == 0:
                        article_list.append(div.get_attribute('innerHTML').strip())
                        time.sleep(0.5)
                    else:
                        if len(div.find_elements_by_tag_name('a')) != 0:
                            article_list.append(
                                div.find_element_by_tag_name('a').get_attribute('innerHTML').strip())
                            continue
                        article_list.append(post_date.get_attribute('innerHTML').strip())
                        time.sleep(0.5)
            make_file(i + 1, article_list)  # 5ea

        except Exception as e:
            print(e)

    def saved_file_by_moving(self, file_name: str) -> None:
        feed = self.find_element_by_css_selector('div[role="feed"]')
        wrappers = feed.find_elements_by_css_selector('div[data-ad-comet-preview="message"]')
        links = feed.find_elements_by_css_selector('a[href^="https://www.facebook.com/"]')
        missing_btn = 0

        # todo fix post_date!
        try:
            print(f'{len(wrappers)} is Waiting')  # 1 wrapper = 1 btn

            for (i, wrapper), post_date in zip(enumerate(wrappers), links):  # each Wrapper
                # moving
                desired_y = (wrapper.size['height'] / 2) + wrapper.location['y']
                current_y = (self.execute_script('return window.innerHeight') / 2) + self.execute_script(
                    'return window.pageYOffset')
                scroll_y_by = desired_y - current_y
                self.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
                time.sleep(2)

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
                self.get_txt(i=i, wrapper=wrapper, post_date=post_date, file_name=file_name)
                print(f'Completed: {i + 1}')

            print(f'{len(wrappers) - missing_btn}ea are totally saved.')


        except Exception as e:
            print(e)
