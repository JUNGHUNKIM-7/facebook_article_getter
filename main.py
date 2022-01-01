from options import OptionContainer, RunOptions

from src.web_runner import WebRunner
from src.finance_data_runner import FinanceRunner


def runOptions(options: RunOptions, **kwarg):
    match options:
        case RunOptions.RUN_FB:
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
        case RunOptions.RUN_TICKER:
            OptionContainer.set_data_reader(run=kwarg.get('run', None))
            if OptionContainer.PARSE_TICKER is True:
                FinanceRunner.run_data_reader()
        case RunOptions.RUN_INVESTPY:
            OptionContainer.set_investpy(run=kwarg.get('run', None))
            if OptionContainer.RUN_INVESTPY is True:
                FinanceRunner.run_investpy()
        case _:
            raise Exception("Not Implemented")


if __name__ == "__main__":
    try:
        runOptions(RunOptions.RUN_INVESTPY, run=True)
    except:
        raise Exception("Not Implemented")
