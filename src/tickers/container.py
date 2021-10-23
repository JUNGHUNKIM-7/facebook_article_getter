from datetime import date, datetime
from typing import List, Union


class Container:
    def __init__(
        self,
        tickers: Union[List[str], None],
        sdate: Union[date, datetime],
        edate: Union[date, datetime] = datetime.now().date(),
    ) -> None:

        if (
            not isinstance(tickers, list)
            or not isinstance(sdate, date)
            or isinstance(edate, date)
        ):
            raise TypeError("Check Your data")

        self.__tickers = tickers

        if (len(str(sdate)) + len(str(edate))) < 20:
            raise NotImplementedError("Enter Correct Date")
        else:
            self.__sdate = sdate
            self.__edate = edate

    @property
    def tickers(self) -> Union[List[str], str, None]:
        return self.__tickers

    @property
    def sdate(self) -> Union[date, datetime, str]:
        return self.__sdate

    @property
    def edate(self) -> Union[date, datetime, str]:
        return self.__edate

    @tickers.setter
    def tickers(self, tickerList: str) -> None:
        self.__tickers = tickerList

    @sdate.setter
    def sdate(self, otherSdate: str) -> None:
        self.__sdate = otherSdate

    @edate.setter
    def edate(self, otherEdate: str) -> None:
        self.__edate = otherEdate

    def __str__(self) -> str:
        return f"{self.__tickers} : START: {self.__sdate} - END: {self.__edate}"
