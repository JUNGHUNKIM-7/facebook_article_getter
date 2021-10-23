from ticker_inputs import *
from src.tickers.timedel import TimeContainer
from src.tickers.convert_ticker_to_csv import Reader

# ticker instance
ti1 = TickerInfo(
    tickers.get("tech"), (time["delta_before"], time["middle"], time["delta_ending"])
)
# passing instance to make date obj from instance
time1 = TimeContainer(ti1)

# instance for make csv
ticker_li_1 = Reader(tickers=ti1.tickers, time_info=time1)

# todo checking funcworks
if __name__ == "__main__":
    try:
        print(ticker_li_1)
        # ticker_li_1.save_to_csv(f"{ti1.time[0]}_{ti1.time[1]}")
    except NotImplemented as n:
        print(n)
    else:
        print(f"{ticker_li_1.tickers} downloaded")
