from src.data_reader.investpy_container import InvestpyContainer, SearchTypes
from src.data_reader.data_reader_container import DataReaderContainer
from src.data_reader.instance_helper import TickerInstanceHelper


class FinanceRunner:
    @classmethod
    def run_data_reader(cls, src="pds") -> None:
        tickers = TickerInstanceHelper.make_instance_list(source=src)

        if tickers is not None:
            for ticker_ins in tickers:
                if isinstance(ticker_ins, DataReaderContainer):
                    ticker_ins.save_to_csv()

    @classmethod
    def run_investpy(cls, src="investpy") -> None:
        tickers = TickerInstanceHelper.make_instance_list(source=src)

        if tickers is not None:
            for ticker_py_ins in tickers:
                if isinstance(ticker_py_ins, InvestpyContainer):
                    match ticker_py_ins.sector:
                        case "stocks":
                            ticker_py_ins.technical_indicator_to_csv()

                        case "stock":
                            ticker_py_ins.get_technical_idx()

                        case "cryptos":
                            if ticker_py_ins.__search_type == (SearchTypes.GET_CRYPTO_LIST or SearchTypes.GET_CRYPTO_OVERVIEW):
                                ticker_py_ins.get_crypto_list_or_overview()
                            elif ticker_py_ins.__search_type == (SearchTypes.GET_CRYPTO_INFO or SearchTypes.GET_CRYPTO_HISTORICAL):
                                ticker_py_ins.get_each_info_or_historical()
                            else:
                                raise Exception("Crypto Search Type Error")

                        case "etfs":
                            if ticker_py_ins.__search_type == (SearchTypes.GET_ETF_LIST or SearchTypes.GET_ETF_COUNTRIES):
                                ticker_py_ins.get_efts_info_or_countries()
                            elif ticker_py_ins.__search_type == (SearchTypes.GET_ETF_INFO or SearchTypes.GET_ETF_HISTORICAL):
                                ticker_py_ins.get_etfs_info_or_historical()
                            else:
                                raise Exception("ETF Search Type Error")

                        case "commodities":
                            if ticker_py_ins.__search_type == (SearchTypes.GET_COMMO_BY_GROUP or SearchTypes.GET_COMMO_OVERVIEW_BY_GROUP):
                                ticker_py_ins.get_commodities_by_group()
                            elif ticker_py_ins.__search_type == (SearchTypes.GET_COMMO_INFO or SearchTypes.GET_COMMO_HISTORICAL):
                                ticker_py_ins.get_commodities_info_or_historical()
                            else:
                                raise Exception(
                                    "Commodities Search Type Error")

                        case _:
                            raise Exception("Invalid Sector")
        else:
            raise Exception("Intance Func Not Implemented")
