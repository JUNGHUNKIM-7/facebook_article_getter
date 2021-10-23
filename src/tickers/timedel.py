from datetime import datetime, timedelta, date
from ticker_inputs import TickerInfo


class TimeContainer:
    def __init__(self, ticker_info: TickerInfo) -> None:
        self.__delta_start = ticker_info.time[0]
        self.__dateString = ticker_info.time[1]
        self.__delta_end = ticker_info.time[-1]

        y, m, d = [int(e) for e in self.__dateString.split("-")]
        self.__middle = datetime(y, m, d).date()

        self.__date = {
            "start_to_date": str(
                self.__middle - timedelta(days=self.__delta_start)
            ).split(" ")[0],
            "date_to_now": str(self.__middle + timedelta(days=self.__delta_end)).split(
                " "
            )[0],
        }

        self.__staring_year, self.__starting_month, self.__starting_day = [
            int(p) for p in self.__date["start_to_date"].split("-")
        ]

        self.__ending_year, self.__ending_month, self.__ending_day = [
            int(p) for p in self.__date["date_to_now"].split("-")
        ]

        self.__starting_date_obj = date(
            self.__staring_year, self.__starting_month, self.__starting_day
        )

        self.__ending_date_obj = date(
            self.__ending_year, self.__ending_month, self.__ending_day
        )

    @property
    def delta_start(self) -> int:
        return self.__delta_start

    @property
    def delta_end(self) -> int:
        return self.__delta_end

    @delta_start.setter
    def delta_start(self, deltaVal_start: int) -> None:
        self.__delta_start = deltaVal_start

    @delta_end.setter
    def delta_end(self, deltaVal_end: int) -> None:
        self.__delta_end = deltaVal_end

    @property
    def start(self) -> date:
        return self.__starting_date_obj

    @property
    def end(self) -> date:
        return self.__ending_date_obj

    def __str__(self):
        return f"Starting: {self.__starting_date_obj} & Middle : {self.__dateString} & Ending: {self.__ending_date_obj} "
