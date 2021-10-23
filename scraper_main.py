from scraper_inputs import *
from src.scraper.container import Container
from src.scraper.convert_files import FileManager

# ------Debug-------
# 2. 2020 이하 버튼 클릭 문제
# no found any btn
# ------Debug-------

# -----instance-----
fb_ins = Container.make_instance(key='facebook', **fb)
news_ins = Container.make_instance(key='yh', news_channel='world', **news)
# -----instance-----

# todo
# year = 2021 이하 작동안함

if __name__ == '__main__':
    run_fb = Container.switch_fb_run(run=True)
    if not run_fb:
        try:
            FileManager.reading_files_from_dir()
            Container.extracting_keyword()
            Container.run_investing()
            Container.news_run()
        except Exception as e:
            print(e)
    else:
        try:
            Container.run_facebook(instance=fb_ins,
                                   year=2021,
                                   # search_keyword="금리",
                                   drag_count_or_infinite=1,
                                   file_name='oh',
                                   kind='txt',
                                   scrape_count=2)
            FileManager.reading_files_from_dir()
            Container.extracting_keyword()
            Container.run_investing()
            Container.news_run()
        except Exception as e:
            print(e)
