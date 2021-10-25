from src.globals.options import *
from src.globals.inputs import *

from src.data_reader.ticker_manager import TickerManager
from src.scraper.instance_controller import InstanceController
from src.globals.file_controller import FileManager
from src.globals.file_handler import FileHandler

fb_ins = InstanceController.make_instance(key='facebook',
                                          options={
                                              'headless': InstanceController.HEAD_LESS,
                                              'browser_status': InstanceController.BROWSER_STATUS
                                          },
                                          **fb)

news_ins = InstanceController.make_instance(key='yh',
                                            news_channel='world',
                                            **news)

if __name__ == '__main__':
    try:
        if PARSE_TICKER_ONLY and not RUN_FB:
            for elem in TickerManager.return_ticker_ins_li():
                elem.save_to_csv()
        elif not PARSE_TICKER_ONLY and not RUN_FB:
            FileManager.reading_files_from_dir()
            FileHandler.extracting_keyword()
            InstanceController.run_news()
        elif not PARSE_TICKER_ONLY and RUN_FB:
            InstanceController.run_facebook(instance=fb_ins,
                                            year=2021,
                                            # search_keyword="금리",
                                            drag_count_or_infinite=1,
                                            file_name='oh',
                                            kind='txt',
                                            scrape_count=2)
            FileManager.reading_files_from_dir()
            FileHandler.extracting_keyword()
            InstanceController.run_news()
        else:
            raise NotImplementedError('Check Your Options')
    except Exception as e:
        print(e)
