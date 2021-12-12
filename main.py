from scraper.fb_controller import FacebookController
from instance_runner import InstanceRunner
from inputs import fb, news
from src.utils.option_container import OptionContainer

# Facebook options
RUN_FB = OptionContainer.set_running_fb(run=False)
OptionContainer.set_headless(headless=False)
OptionContainer.set_kill_browser(kill=True)
# Pdr options
PARSE_TICKER = OptionContainer.parse_ticker_switch()
# INVESTIPY
RUN_INVESTIPY = OptionContainer.set_investipy()

if __name__ == "__main__":
    try:
        if PARSE_TICKER and not RUN_INVESTIPY:
            InstanceRunner.run_data_reader()
        elif not PARSE_TICKER and RUN_INVESTIPY:
            InstanceRunner.run_investipy(kind='stock')
        elif PARSE_TICKER and RUN_INVESTIPY:
            InstanceRunner.run_data_reader()
            InstanceRunner.run_investipy(kind='stock')
        elif RUN_FB:
            fb_ins = InstanceRunner.make_instance(key="facebook", kwargs=fb)
            if fb_ins is not None and type(fb_ins) is FacebookController:
                InstanceRunner.run_facebook(
                    instance=fb_ins,
                    year=2021,
                    search_keyword="금리",
                    drag_count_or_infinite=1,
                    file_name="oh",
                    kind="txt",
                    scrape_count=2,
                )
        else:
            news_ins = InstanceRunner.make_instance(
                key="investing", news_channel="market", kwargs=news
            )

            if news_ins is not None and type(news_ins) is InstanceRunner:
                InstanceRunner.run_news(instance=news_ins)
    except Exception as e:
        print(e)
