from options import *
from inputs import *
from src.scraper.helper import Container
from file_controller import FileManager

fb_ins = Container.make_instance(key='facebook', **fb)
news_ins = Container.make_instance(key='yh', news_channel='world', **news)

if __name__ == '__main__':
    try:
        if PARSE_TICKER_ONLY and not RUN_FB:
            for elem in return_ticker_ins_li():
                elem.save_to_csv()
        elif not PARSE_TICKER_ONLY and not RUN_FB:
            FileManager.reading_files_from_dir()
            Container.extracting_keyword()
            Container.run_investing()
            Container.news_run()
        elif not PARSE_TICKER_ONLY and RUN_FB:
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
        else:
            raise NotImplemented('Any Action has\'nt started')
    except Exception as e:
        print(e)
