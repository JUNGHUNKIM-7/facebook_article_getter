from src.globals.options_controller import OptionsController

# Facebook options
RUN_FB = OptionsController.set_running_fb(run=False)
OptionsController.set_headless(headless=False)
OptionsController.set_kill_browser(kill=True)

# Pdr options
PARSE_TICKER = OptionsController.parse_ticker_switch(run=True)
# INVESTIPY
RUN_INVESTIPY = OptionsController.set_investipy(run=False)
