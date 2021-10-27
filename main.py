from src.globals.options import *
from src.globals.inputs import *
from src.globals.instance_controller import InstanceController

if __name__ == '__main__':
    try:
        if PARSE_TICKER and not RUN_INVESTIPY:
            InstanceController.run_data_reader()
        elif not PARSE_TICKER and RUN_INVESTIPY:
            InstanceController.run_investipy()
        elif RUN_FB and RUN_INVESTIPY:
            InstanceController.run_data_reader()
            InstanceController.run_investipy()
        elif RUN_FB:
            fb_ins = InstanceController.make_instance(key='facebook', **fb)
            InstanceController.run_facebook(instance=fb_ins,
                                            year=2021,
                                            search_keyword="금리",
                                            drag_count_or_infinite=1,
                                            file_name='oh',
                                            kind='txt',
                                            scrape_count=2)
        else:
            news_ins = InstanceController.make_instance(key='investing', news_channel='market', **news)
            InstanceController.run_news(instance=news_ins)
    except Exception as e:
        print(e)
