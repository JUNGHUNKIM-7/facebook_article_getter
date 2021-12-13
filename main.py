from enum import Enum,auto

from src.instance_runner import InstanceRunner
from src.utils.option_container import OptionContainer

class Options(Enum):
    RUN_FB=auto()
    PARSE_TICKER=auto()
    RUN_INVESTIPY=auto()

def runOptions(options: Options, **kwarg):
    match options:
        case Options.RUN_FB:
            pass
            # OptionContainer.set_headless(headless=kwarg.get('headless',None))
            # OptionContainer.set_kill_browser(kill=kwarg.get('kill',None))
            # OptionContainer.set_running_fb(run=kwarg.get('run',None))
            # if OptionContainer.RUN_FB is True:
            #     fb_ins = InstanceRunner.make_instance(key="facebook", **fb)
            #     print(fb_ins)
            #     if fb_ins is None:
            #         raise Exception("Failed to create instance")
            #     if fb_ins is not None and type(fb_ins) is FacebookController:
            #             InstanceRunner.run_facebook(
            #                 instance=fb_ins,
            #                 year=2021,
            #                 search_keyword="금리",
            #                 drag_count_or_infinite=1,
            #                 file_name="oh",
            #                 kind="txt",
            #                 scrape_count=2,
            #             )
            #     else:
            #         news_ins = InstanceRunner.make_instance(
            #             key="investing", news_channel="market", **news
            #         )
            #         if news_ins is not None and type(news_ins) is InstanceRunner:
            #             InstanceRunner.run_news(instance=news_ins)
        case Options.PARSE_TICKER:
            OptionContainer.set_data_reader(run=kwarg.get('run',None))
            if OptionContainer.PARSE_TICKER is True:
                InstanceRunner.run_data_reader()
        case Options.RUN_INVESTIPY:
            OptionContainer.set_investipy(run=kwarg.get('run',None))
            if OptionContainer.RUN_INVESTIPY is True:
                InstanceRunner.run_investipy()
        case _:
            Exception("Not Implemented")


if __name__ == "__main__":
    try:
        runOptions(Options.RUN_INVESTIPY, run=True)
    except:
        raise Exception("Not Implemented")