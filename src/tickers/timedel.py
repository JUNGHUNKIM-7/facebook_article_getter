from datetime import datetime, timedelta, date
from typing import Dict


class TimeContainer:
    def __init__(self, time_val: Dict[str, str]) -> None:
        self.__delta_start = timedelta(days=float(time_val.get('before')))
        self.__dateString = time_val.get('base')
        self.__delta_end = timedelta(days=float(time_val.get('after')))

        y, m, d = [int(e) for e in self.__dateString.split("-")]
        self.__base = datetime(y, m, d).date()

        self.__date = {
            "before_from_base": self.__base - self.__delta_start,
            "after_from_base": self.__base + self.__delta_end
        }

        self.__starting_date_obj = self.__date['before_from_base']
        self.__ending_date_obj = self.__date['after_from_base']

    @property
    def date_string(self) -> str:
        return self.__dateString

    @property
    def start(self) -> date:
        return self.__starting_date_obj

    @property
    def end(self) -> date:
        return self.__ending_date_obj

    def __str__(self):
        return f"Starting: {self.start} & base : {self.start} & Ending: {self.end} "
