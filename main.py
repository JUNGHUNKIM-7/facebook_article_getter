from src.globals.options_controller import OptionsController
from src.scraper.controller_fb_working import FacebookController
from src.globals.instance_controller import Runner
from src.globals.inputs import fb, news

# Facebook options
RUN_FB = OptionsController.set_running_fb(run=False)
OptionsController.set_headless(headless=False)
OptionsController.set_kill_browser(kill=True)
# Pdr options
PARSE_TICKER = OptionsController.parse_ticker_switch()
# INVESTIPY
RUN_INVESTIPY = OptionsController.set_investipy()

if __name__ == "__main__":
    try:
        if PARSE_TICKER and not RUN_INVESTIPY:
            Runner.run_data_reader()
        elif not PARSE_TICKER and RUN_INVESTIPY:
            Runner.run_investipy()
        elif PARSE_TICKER and RUN_INVESTIPY:
            Runner.run_data_reader()
            Runner.run_investipy()
        elif RUN_FB:
            fb_ins = Runner.make_instance(key="facebook", kwargs=fb)
            if fb_ins is not None and type(fb_ins) is FacebookController:
                Runner.run_facebook(
                    instance=fb_ins,
                    year=2021,
                    search_keyword="금리",
                    drag_count_or_infinite=1,
                    file_name="oh",
                    kind="txt",
                    scrape_count=2,
                )
        else:
            news_ins = Runner.make_instance(
                key="investing", news_channel="market", kwargs=news
            )

            if news_ins is not None and type(news_ins) is Runner:
                Runner.run_news(instance=news_ins)
    except Exception as e:
        print(e)
