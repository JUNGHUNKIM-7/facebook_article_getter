from datetime import datetime, timedelta, date
from typing import Dict, Any


class TimeHandler:
    def __init__(self, time_val: Dict[str, Any]) -> None:
        self.__starting = time_val.get("before")
        self.__ending = time_val.get("after")

        if time_val.get("before") is not None and self.__starting:
            self.__delta_start = timedelta(days=float(self.__starting))
        else:
            self.__delta_start = timedelta(days=0)

        if time_val.get("after") is not None and self.__ending:
            self.__delta_end = timedelta(days=float(self.__ending))
        else:
            self.__delta_end = timedelta(days=0)

        self.__dateString = time_val.get("base")
        self.__specific_date = time_val.get("specific")
        self.__today = datetime.now().date()

        if self.__dateString is not None:
            y, m, d = [int(e) for e in self.__dateString.split("-")]
            self.__base = datetime(y, m, d).date()

        if self.__specific_date is not None:
            y, m, d = [int(e) for e in self.__specific_date.split("-")]
            self.__specific = datetime(y, m, d).date()

        self.__date = {
            "before_from_base": self.__base - self.__delta_start,
            "after_from_base": self.__base + self.__delta_end,
        }

        self.__starting_date = self.__date["before_from_base"]
        self.__ending_date = self.__date["after_from_base"]

    @property
    def base(self) -> date:
        return self.__base

    @property
    def specific(self) -> date:
        return self.__specific

    @property
    def start(self) -> date:
        return self.__starting_date

    @property
    def end(self) -> date:
        return self.__ending_date

    @property
    def today(self) -> date:
        return self.__today

    def __str__(self):
        return f"Starting: {self.start} & base : {self.start} & Ending: {self.end} "
