from datetime import date
from src.data_reader.investpy_container import SearchTypes

# indices, stocks, etfs, funds, commodities, currencies, cryptos, bonds, certificates, fxfutures
investpy_tickers = {
    # "group1": {
    #     "source": "investpy",
    #     "tickers_group": ["AMZN", "AAPL"],
    #     "sector": "stocks",
    #     "interval": "monthly",
    # },
    # "group2": {
    #     "source": "investpy",
    #     "tickers_group": ["AMZN", "AAPL"],
    #     "sector": "stock",
    #     "interval": "monthly",
    # },
    # "group1": {
    #     "source": "investpy",
    #     "tickers_group": ["bitcoin", "ethereum"],
    #     "sector": "cryptos",
    #     "interval": "monthly",
    #     "search_type" : SearchTypes.GET_TICKER_INFO
    # },
    "group4": {
        "source": "investpy",
        "tickers_group": ["bitcoin", "ethereum"],
        "sector": "etfs",
        "interval": "daily",
    },
    # "group5": {
    #     "source": "investpy",
    #     "tickers_group": ["bitcoin", "ethereum"],
    #     "sector": "commodities",
    #     "interval": "daily",
    # },
}

datareader_tickers = {
    "group1": {"source": "yahoo", "tickers_group": ["AMZN", "AAPL"]},
    "group2": {"source": "naver", "tickers_group": ["005930", "035720"]},
    "group3": {"source": "naver", "tickers_group": ["000660", "066570"]},
}

investpy_time_set = {
    "set1": {"before": 10, "base": str(date.today()), "after": 10},
    # "set2": {"before": 10, "base": str(date.today()), "after": 10},
    # "set3": {"before": 10, "base": str(date.today()), "after": 10},
    # "set4": {"before": 10, "base": str(date.today()), "after": 10},
    # "set5": {"before": 10, "base": str(date.today()), "after": 10},
    # "set5": {"before": 10, "base": str(date.today()), "after": 10},
}

datareader_time_set = {
    "set1": {"before": 10, "base": str(date.today()), "after": 10},
    "set2": {"before": 10, "base": "2020-05-05"},
    "set3": {"base": "2020-05-05", "after": 3},
}
