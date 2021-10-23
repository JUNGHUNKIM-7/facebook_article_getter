from typing import List, Union
import pandas_datareader as pdr
import pandas as pd
import time

from container import Container
from timedel import TimeContainer


class Reader(Container):
    def __init__(
            self, tickers: Union[List[str], None], time_info: TimeContainer
    ) -> None:
        super().__init__(
            tickers=tickers, sdate=time_info.start, edate=time_info.end,
        )

    def save_to_csv(self, file_name: str) -> None:
        for ticker in self.tickers:
            df = pdr.DataReader(ticker, "yahoo", self.sdate, self.edate)
            time.sleep(1.5)
            df = pd.DataFrame(df)
            df.to_csv(f"files\\csv\\{ticker}_{file_name}.csv")
