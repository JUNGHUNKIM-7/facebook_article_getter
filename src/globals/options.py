from src.scraper.instance_controller import InstanceController

# Facebook options
RUN_FB = InstanceController.set_running_fb(run=False)
InstanceController.set_headless(headless=False)
InstanceController.set_kill_browser(kill=True)

# Pdr options
PARSE_TICKER_ONLY = InstanceController.parse_ticker_switch(run=True)
