import os


class OptionContainer:
    # tickers
    PARSE_TICKER = True

    # FB
    RUN_FB = True
    HEAD_LESS = True
    BROWSER_STATUS = True

    # investpy
    RUN_investpy = True

    SAVE_DIR = r"finance_data_getter\files"

    # Options
    @classmethod
    def save_path(cls, folder_name: str = SAVE_DIR) -> str:
        curr = os.getcwd()
        root = os.path.dirname(curr)
        stored_file_loc = os.path.join(root, folder_name)
        return stored_file_loc

    @classmethod
    def set_data_reader(cls, run: bool = PARSE_TICKER) -> bool:
        if run is False:
            OptionContainer.PARSE_TICKER = run
            return OptionContainer.PARSE_TICKER
        else:
            return OptionContainer.PARSE_TICKER

    @classmethod
    def set_running_fb(cls, run: bool = RUN_FB):
        if run is False:
            OptionContainer.RUN_FB = run
            print("Status : Not implemented")
            return OptionContainer.RUN_FB
        else:
            print("Status : Running Facebook")
            return OptionContainer.RUN_FB

    @classmethod
    def set_headless(cls, headless: bool = HEAD_LESS):
        if headless is False:
            print("Headless : No")
            OptionContainer.HEAD_LESS = headless
            return OptionContainer.HEAD_LESS
        else:
            print("Headless : Yes")
            return OptionContainer.HEAD_LESS

    @classmethod
    def set_kill_browser(cls, kill: bool = BROWSER_STATUS):
        if kill is False:
            print("KillBrower : No")
            OptionContainer.BROWSER_STATUS = kill
            return OptionContainer.BROWSER_STATUS
        else:
            print("KillBrower : Yes")
            return OptionContainer.BROWSER_STATUS

    @classmethod
    def set_investpy(cls, run: bool = RUN_investpy) -> bool:
        if run is False:
            OptionContainer.RUN_investpy = run
            return OptionContainer.RUN_investpy
        else:
            return OptionContainer.RUN_investpy
