"""A module that contains a commands that call into OpenBB SDK."""
import os

from openbb_terminal.reports import widget_helpers as widgets
from openbb_terminal.sdk import openbb
from openbb_terminal import config_terminal as cfg
from openbb_terminal.helper_classes import TerminalStyle
from dotenv import load_dotenv
import json
import logging
import sys
from autogpt.commands.command import command
from urllib.request import urlopen
import certifi
import json

logging.basicConfig(level=logging.CRITICAL + 1)
load_dotenv()

@command(
    "get_active_addresses",  # command name
    "Retrieves the active addresses for a given cryptocurrency",  # command description
    '"symbol": "<symbol>", "interval": "<interval>", "start_date": "<start_date>", "end_date": "<end_date>"' # command argument in JSON format
)
def get_active_addresses(symbol: str, interval: str, start_date: str, end_date: str) -> str:
    """
    This function retrieves the active addresses for a given cryptocurrency.

    Parameters:
    symbol (str): The symbol for the cryptocurrency.
    interval (str): The interval for the active addresses data. Can be "24h", "7d", "30d", "3m", "6m", "1y", or "5y".
    start_date (str): The starting date is a string in the format 'YYYY-MM-DD'.
    end_date(str): The end date is a string in the format 'YYYY-MM-DD'.

    Returns:
    str: A JSON string representing the active addresses for the cryptocurrency.
    """
    if (interval == "1d"):
        interval = interval.replace("1d", "24h")
    
    active = openbb.crypto.dd.active(symbol=symbol, interval=interval, start_date=start_date, end_date=end_date)
    json_string = active.to_json(orient='records')
    data = json.dumps(json_string)
    return data 

@command(
    "get_crypto_ath",  # command name
    "Retrieves the all time high for a given cryptocurrency.",  # command description
    '"symbol": "<symbol>", "currency": "<currency>"' # command argument in JSON format
)
def get_crypto_ath(symbol: str, currency: str) -> str:
    """
    This function retrieves the all time high for a given cryptocurrency.

    Parameters:
    symbol (str): The symbol for the cryptocurrency.
    currency (str): The currency to get all time high in.

    Returns:
    str: A JSON string representing the all time high for the cryptocurrency.
    """
    ath = openbb.crypto.dd.ath(symbol=symbol, currency=currency)
    json_string = ath.to_json(orient='records')
    data = json.dumps(json_string)
    return data

@command(
    "get_crypto_atl",  # command name
    "Retrieves the all time low for a given cryptocurrency.",  # command description
    '"symbol": "<symbol>", "currency": "<currency>"' # command argument in JSON format
)
def get_crypto_atl(symbol: str, currency: str) -> str:
    """
    This function retrieves the all time low for a given cryptocurrency.

    Parameters:
    symbol (str): The symbol for the cryptocurrency.
    currency (str): The currency to get all time low in.

    Returns:
    str: A JSON string representing the all time low for the cryptocurrency.
    """
    atl = openbb.crypto.dd.atl(symbol=symbol, currency=currency)
    json_string = atl.to_json(orient='records')
    data = json.dumps(json_string)
    return data

@command(
    "get_basic_coin_info",  # command name
    "Get basic coin info",  # command description
    '"symbol": "<symbol>"' # command argument in JSON format
)
def get_basic_coin_info(symbol: str) -> str:
    """
    Basic coin information [Source: CoinPaprika]
        
    Parameters:
    symbol (str): The symbol for the cryptocurrency.

    Returns:
    str: A JSON string representing the basic coin information.
    """
    basic = openbb.crypto.dd.basic(symbol=symbol)
    json_string = basic.to_json(orient='records')
    data = json.dumps(json_string)
    return data

@command(
    "get_coin_data",  # command name
    "Get coin data",  # command description
    '"symbol": "<symbol>"' # command argument in JSON format
)
def get_coin_data(symbol: str) -> str:
    """
    Get coin by id [Source: CoinPaprika]

    symbol(str): id of coin from coinpaprika e.g. Ethereum - > 'eth-ethereum'
    """
    coin_id_data = openbb.crypto.dd.coin(symbol=symbol)
    data = json.dumps(coin_id_data)
    return data

@command(
    "get_potential_returns",  # command name
    "Get potential crypto returns",  # command description
    '"main_coin": "<main_coin>", "to_symbol": "<to_symbol>", "limit": "<limit>", "price": "<price>"' # command argument in JSON format
)
def get_potential_returns(main_coin: str, to_symbol: str, limit: int, price: float) -> str:
    """

    This function fetches data to calculate potential returns of a certain coin.
    
    Parameters:
    main_coin (str): The symbol for the cryptocurrency.
    to_symbol (str): The symbol for the cryptocurrency to compare with.
    limit (int): The number of coins with highest market cap to compare main_coin with.
    price (float): The target price of main_coin to check potential returns.
    
    Returns:
    str: A JSON string representing the potential returns of the cryptocurrency.
    """
    potential_returns = openbb.crypto.dd.pr(main_coin=main_coin, to_symbol=to_symbol, limit=limit, price=price)
    json_string = potential_returns.to_json(orient='records')
    data = json.dumps(json_string)
    return data

@command(
    "get_marketcap_dominance",  # command name
    "Get crypto marketcap dominance",  # command description
    '"symbol": "<symbol>", "interval": "<interval>", "start_date": "<start_date>", "end_date": "<end_date>"' # command argument in JSON format
)
def get_marketcap_dominance(symbol: str, interval: str, start_date: str, end_date: str) -> str:
    """
    Returns market dominance of a coin over time
    [Source: https://messari.io/]

    Parameters
    ----------
    symbol : str
        Crypto symbol to check market cap
    interval : str
        Interval frequency (possible values are: 5m, 15m, 30m, 1h, 1d, 1w)
    start_date : Optional[str]
        Initial date like string (e.g., 2021-10-01)
    end_date : Optional[str]
        End date like string (e.g., 2021-10-01)
    """
    mcapdom = openbb.crypto.dd.mcapdom(symbol=symbol, interval=interval, start_date=start_date, end_date=end_date)
    json_string = mcapdom.to_json(orient='records')
    data = json.dumps(json_string)
    return data