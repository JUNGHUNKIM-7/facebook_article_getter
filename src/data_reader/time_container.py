from datetime import datetime, timedelta, date
from typing import Dict


class TimeContainer:
    def __init__(self, time_val: Dict[str, str]) -> None:
        if time_val.get('before') is not None:
            self.__delta_start = timedelta(days=float(time_val.get('before')))
        else:
            self.__delta_start = timedelta(days=0)

        if time_val.get('after') is not None:
            self.__delta_end = timedelta(days=float(time_val.get('after')))
        else:
            self.__delta_end = timedelta(days=0)

        self.__dateString = time_val.get('base')
        self.__today = datetime.now().date()

        y, m, d = [int(e) for e in self.__dateString.split("-")]
        self.__base = datetime(y, m, d).date()

        self.__date = {
            "before_from_base": self.__base - self.__delta_start,
            "after_from_base": self.__base + self.__delta_end
        }

        self.__starting_date = self.__date['before_from_base']
        self.__ending_date = self.__date['after_from_base']

    @property
    def base(self) -> date:
        return self.__base

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
