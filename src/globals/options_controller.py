class OptionsController:
    # tickers
    PARSE_TICKER = True

    # FB
    RUN_FB = True
    HEAD_LESS = True
    BROWSER_STATUS = True

    # Investipy
    RUN_INVESTIPY = True

    # Options
    @classmethod
    def parse_ticker_switch(cls, run: bool = PARSE_TICKER) -> bool:
        if run is False:
            OptionsController.PARSE_TICKER = run
            return OptionsController.PARSE_TICKER
        else:
            return OptionsController.PARSE_TICKER

    @classmethod
    def set_running_fb(cls, run: bool = RUN_FB):
        if run is False:
            OptionsController.RUN_FB = run
            print('Status : Not Facebook')
            return OptionsController.RUN_FB
        else:
            print('Status : Running Facebook')
            return OptionsController.RUN_FB

    @classmethod
    def set_headless(cls, headless: bool = HEAD_LESS):
        if headless is False:
            print('Option : Not Headless')
            OptionsController.HEAD_LESS = headless
            return OptionsController.HEAD_LESS
        else:
            print('Option : On Headless')
            return OptionsController.HEAD_LESS

    @classmethod
    def set_kill_browser(cls, kill: bool = BROWSER_STATUS):
        if kill is False:
            print('Option : Not Kill browser')
            OptionsController.BROWSER_STATUS = kill
            return OptionsController.BROWSER_STATUS
        else:
            print('Option : Kill browser')
            return OptionsController.BROWSER_STATUS

    @classmethod
    def set_investipy(cls, run: bool = RUN_INVESTIPY) -> bool:
        if run is False:
            OptionsController.RUN_INVESTIPY = run
            return OptionsController.RUN_INVESTIPY
        else:
            return OptionsController.RUN_INVESTIPY
