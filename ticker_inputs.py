from dataclasses import dataclass
from typing import List, Tuple, Union


@dataclass
class TickerInfo:
    __tickers: Union[List[str], None]
    __time: Tuple[int, str, int]

    @property
    def tickers(self) -> Union[List[str], None]:
        return self.__tickers

    @property
    def time(self) -> Tuple[int, str, int]:
        return self.__time


# settings
tickers = {
    "tech": ["AMZN", "AAPL"],
}

time = {"delta_before": 1, "middle": "2020-01-01", "delta_ending": 1}
