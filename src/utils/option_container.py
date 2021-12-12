class OptionContainer:
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
            OptionContainer.PARSE_TICKER = run
            return OptionContainer.PARSE_TICKER
        else:
            return OptionContainer.PARSE_TICKER

    @classmethod
    def set_running_fb(cls, run: bool = RUN_FB):
        if run is False:
            OptionContainer.RUN_FB = run
            print("Status : Not Facebook")
            return OptionContainer.RUN_FB
        else:
            print("Status : Running Facebook")
            return OptionContainer.RUN_FB

    @classmethod
    def set_headless(cls, headless: bool = HEAD_LESS):
        if headless is False:
            print("Option : Not Headless")
            OptionContainer.HEAD_LESS = headless
            return OptionContainer.HEAD_LESS
        else:
            print("Option : On Headless")
            return OptionContainer.HEAD_LESS

    @classmethod
    def set_kill_browser(cls, kill: bool = BROWSER_STATUS):
        if kill is False:
            print("Option : Not Kill browser")
            OptionContainer.BROWSER_STATUS = kill
            return OptionContainer.BROWSER_STATUS
        else:
            print("Option : Kill browser")
            return OptionContainer.BROWSER_STATUS

    @classmethod
    def set_investipy(cls, run: bool = RUN_INVESTIPY) -> bool:
        if run is False:
            OptionContainer.RUN_INVESTIPY = run
            return OptionContainer.RUN_INVESTIPY
        else:
            return OptionContainer.RUN_INVESTIPY
