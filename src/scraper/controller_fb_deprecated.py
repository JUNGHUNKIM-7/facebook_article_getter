import os
import time
from typing import Optional, Union, List, Tuple, Dict

from dotenv import load_dotenv
from selenium import webdriver as driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.globals.file_controller import FileManager


class FacebookController(driver.Firefox):
    load_dotenv()
    OPS = driver.FirefoxOptions()

    def __init__(self, loc: str,
                 person_name: str,
                 person_info: Optional[str] = None,
                 driver_path: str = r'data_getter\geckodriver.exe',
                 options: Optional[Dict[str, bool]] = None):

        os.environ["PATH"] += driver_path
        self.__id = os.getenv('FB_ID')
        self.__password = os.getenv('FB_PASS')
        self.loc = loc
        self.person_name = person_name
        self.person_info = person_info
        self.__headless = options['headless']
        self.__browser_status = options['browser_status']

        if self.__headless:
            FacebookController.OPS.headless = self.__headless
            super(FacebookController, self).__init__(options=FacebookController.OPS)
        else:
            super(FacebookController, self).__init__()

        self.implicitly_wait(5)
        # self.maximize_window()

    @classmethod
    def make_wrapper_generator(cls, web_elements: List[WebElement], dates: Optional[List[WebElement]] = None) \
            -> Union[Tuple[int, WebElement, WebElement], Tuple[int, WebElement]]:
        if dates:
            for (i, wrapper_elem), date in zip(enumerate(web_elements), dates):
                yield i, wrapper_elem, date
        else:
            for i, wrapper_elem in enumerate(web_elements):
                yield i, wrapper_elem

    def close_browser(self) -> None:
        if self.__browser_status:
            time.sleep(3)
            self.quit()
        else:
            print('Running Program Done')

    def login(self) -> None:
        self.get(self.loc)
        self.find_element(By.ID, 'email').send_keys(self.__id)
        time.sleep(1)

        self.find_element(By.ID, 'pass').send_keys(self.__password)
        time.sleep(1)

        btn = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        btn.click()

    def search_person(self) -> None:
        search_bar = self.find_element(By.CSS_SELECTOR, 'input[spellcheck="false"]')
        search_bar.click()
        search_bar.send_keys(self.person_name)
        time.sleep(2)

        spans = self.find_elements(By.CLASS_NAME, 'ojkyduve')

        for span in spans:
            cond = span.get_attribute('innerHTML').strip()
            if self.person_info in cond:
                span.click()
                break
            else:
                raise NoSuchElementException

    def page_refresh(self) -> None:
        btn = self.find_element(By.CSS_SELECTOR, 'div[aria-label="페이지 새로 고침"]')
        btn.click()
        time.sleep(1)

    def year_selector(self, year: int, wrapper_css_selector: str):
        year_dict = {
            '2021': 0,
            '2020': 1,
            '2019': 2,
            '2018': 3,
            '2017': 4,
            '2016': 5,
            '2015': 6,
            '2014': 7,
            '2013': 8,
            '2012': 9,
        }
        options_wrapper = self.find_element(By.CSS_SELECTOR, wrapper_css_selector)

        # todo 2021 제외하고는 작동안됨
        for key in year_dict.keys():
            if str(year) == key:
                val = year_dict.get(key)
                btn = options_wrapper.find_elements(By.CSS_SELECTOR, 'div[aria-checked="false"]')[val]
                btn.click()
                time.sleep(2.5)
                break
            else:
                raise Exception("Not Found Year Options")

    def search_posts(self, year: Optional[int] = None, search_keyword: Optional[str] = None) -> None:
        if year and search_keyword is None:
            a = self.find_element(By.CSS_SELECTOR, 'a[href^="/search/posts"]')
            a.click()
            time.sleep(1)

            switch = self.find_element(By.CSS_SELECTOR, 'input[aria-label="최근 게시물"]')
            switch.click()
            time.sleep(1)

            year_selection = self.find_elements(By.CSS_SELECTOR, 'div[aria-haspopup="listbox"]')[0]
            year_selection.click()
            time.sleep(1)

            self.year_selector(year=year, wrapper_css_selector='div[role="listbox"]')
        elif year and search_keyword:
            time.sleep(1)
            btn = self.find_element(By.CSS_SELECTOR, f'div[aria-label="{self.person_name}님의 게시물 검색"]')
            btn.click()

            time.sleep(1)
            input_field = self.find_element(By.CSS_SELECTOR,
                                            f'input[aria-label="{self.person_name}님의 게시물, 사진 및 태그에서 검색"]')
            input_field.send_keys(search_keyword)
            time.sleep(0.5)
            input_field.send_keys(Keys.ENTER)
            time.sleep(0.5)

            wrapper = self.find_elements(By.CLASS_NAME, 'dbvibxzo')[1]
            div = wrapper.find_elements(By.CLASS_NAME, 'qzhwtbm6')[1]
            switch = div.find_element(By.TAG_NAME, 'input')
            switch.click()

            year_selection_wrapper = self.find_elements(By.CLASS_NAME, 'lwwyvkzy')[1]
            year_selection = year_selection_wrapper.find_elements(By.CSS_SELECTOR, 'div[role="combobox"]')[1]
            year_selection.click()
            time.sleep(1)

            self.year_selector(year=year, wrapper_css_selector='div[role="listbox"]')
        else:
            a = self.find_element(By.CSS_SELECTOR, 'a[href^="/search/posts"]')
            a.click()
            time.sleep(1)

            switch = self.find_element(By.CSS_SELECTOR, 'input[aria-label="최근 게시물"]')
            switch.click()

    def bottom_end(self, drag_count_or_infinite: Union[int, bool]):
        if drag_count_or_infinite is not bool:
            for _ in range(drag_count_or_infinite):
                time.sleep(1)
                self.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(1.5)
            self.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
        else:
            pass
            # curr_y = 0
            # while True:
            #     self.position_to_base(element=curr_y)
            #     time.sleep(1.5)

    def position_to_base(self, element: WebElement) -> None:
        desired_y = (element.size['height'] / 2) + element.location['y']
        current_y = (self.execute_script('return window.innerHeight') / 2) + self.execute_script(
            'return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(2)

    def saved_file_by_moving(self,
                             file_name: str,
                             kind: str,
                             scrape_count: int = 1,
                             year: Optional[int] = None,
                             search_keyword: Optional[str] = None,
                             ) -> None:
        feed = self.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

        try:
            time.sleep(2)
            if year and not search_keyword:
                wrappers = feed.find_elements(By.CSS_SELECTOR, 'div[data-ad-comet-preview="message"]')
                links = feed.find_elements(By.CSS_SELECTOR, 'a[aria-label*="일"]')
                missing_btn = 0

                # generator
                year_wrapper_gen = FacebookController.make_wrapper_generator(web_elements=wrappers, dates=links)
                if scrape_count >= 1:
                    for _ in range(scrape_count):
                        i, wrapper, post_date = next(year_wrapper_gen)
                        print(f"Wrapper {i + 1} is reading data")

                        self.position_to_base(element=wrapper)

                        button_check = len(wrapper.find_elements(By.CSS_SELECTOR, 'div[role="button"]'))

                        if button_check == 0:
                            missing_btn += 1
                            continue
                        else:
                            btn = wrapper.find_element(By.CSS_SELECTOR, 'div[role="button"]')
                            btn.click()
                            time.sleep(1.5)

                        print(f'Start Scraping {i + 1}')
                        FileManager.get_data_as_file(i=i,
                                                     web_elems_or_data_list=wrapper,
                                                     post_date=post_date,
                                                     file_name=file_name,
                                                     kind=kind)
                        print(f'Completed: {i + 1}')
                else:
                    raise Exception('Scrape Count should be same or more at least a elem')
                print(f'Wrapper: {scrape_count} are totally saved, MissingBtn:{missing_btn}')

            elif year and search_keyword:
                wrappers = self.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
                keyword_wrapper_gen = FacebookController.make_wrapper_generator(web_elements=wrappers)

                if scrape_count >= 1:
                    for _ in range(scrape_count):
                        i, wrapper = next(keyword_wrapper_gen)
                        print(f"Wrapper {i + 1} is reading data")

                        WebDriverWait(self, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))

                        # moving
                        self.position_to_base(element=wrapper)

                        if len(wrapper.find_elements(By.CSS_SELECTOR, 'a[href*="posts"]')) == 0:
                            continue
                        else:
                            link = wrapper.find_element(By.CSS_SELECTOR, 'a[href*="posts"]').get_attribute(
                                'href').strip()
                            self.get(link)

                            WebDriverWait(self, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="article"]')))

                            big_wrapper = self.find_element(By.CSS_SELECTOR, 'div[role="article"]')
                            date = big_wrapper.find_element(By.CSS_SELECTOR, 'a[href*="posts"]') \
                                .get_attribute('innerText').strip()

                            data = []
                            posts_wrapper = big_wrapper.find_element(By.CSS_SELECTOR,
                                                                     'div[data-ad-preview="message"]')
                            posts = posts_wrapper.find_elements(By.CSS_SELECTOR, 'div[style="text-align:start"]')

                            for post in posts:
                                data.append(post.get_attribute('innerText').strip())

                            # parsing and save files
                            print(f'Start Scraping {i + 1}')
                            FileManager.get_data_as_file(i=i,
                                                         web_elems_or_data_list=data,
                                                         post_date=date,
                                                         file_name=file_name,
                                                         kind=kind)
                            print(f'Completed: {i + 1}')

                            self.back()
                else:
                    raise Exception('Scrape Count should be same or more at least a elem')
                print(f'Wrapper: {scrape_count} are totally saved')

            else:
                raise Exception("Year or Search should be passed to filter posts")
        except Exception as e:
            print(e)
