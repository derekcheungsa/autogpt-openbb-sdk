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
    "get_financial_metrics",  # command name
    "Financial metrics for a ticker",  # command description
    '"ticker": "<ticker>", "statements": "<statements>"',  # command arguments in JSON format
)
def get_financial_metrics(ticker: str, statements: str) -> str:
    """
    This function retrieves the financial metrics for a given stock ticker.
    
    Parameters:
    ticker (str): The ticker symbol for the stock. It can be prefixed with a '$' symbol.
    statements (str): Not used in the current function. It could be used to specify financial statements to retrieve.
    
    Returns:
    str: A JSON string representing the financial metrics for the stock.
    """
    # If the ticker starts with '$', remove it
    if ticker.startswith('$'):
        ticker = ticker[1:]

    # Retrieve financial metrics from openbb.stocks.ca.screener
    df = openbb.stocks.ca.screener([ticker], data_type="financial")    

    # Drop unnecessary columns
    df = df.drop(columns=['Change', 'Volume', 'Earnings', 'Price','Market Cap'])

    # Fill NA/NaN values with 0
    df = df.fillna(0)

    # Format the output better by converting the metrics to percentages
    df['Dividend'] = df['Dividend'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['ROA'] = df['ROA'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['ROE'] = df['ROE'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['ROI'] = df['ROI'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Gross M'] = df['Gross M'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Oper M'] = df['Oper M'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Profit M'] = df['Profit M'].apply(lambda x: "{0:.1f}%".format(x*100))                          
    
    # Convert the data frame to a JSON string
    json_string = df.to_json(orient='records')
    
    # Convert the JSON string to a Python string
    data = json.dumps(json_string)
    
    # Return the data
    return data

@command(
    "get_valuation_metrics",  # command name
    "Valuation metrics for a ticker",  # command description
    '"ticker": "<ticker>", "statements": "<statements>"',  # command arguments in JSON format
)
def get_valuation_metrics(ticker: str, statements: str) -> str:
    """
    This function retrieves the valuation metrics for a given stock ticker.
    
    Parameters:
    ticker (str): The ticker symbol for the stock. It can be prefixed with a '$' symbol.
    statements (str): Not used in the current function. It could be used to specify financial statements to retrieve.
    
    Returns:
    str: A JSON string representing the valuation metrics for the stock.
    """
    # If the ticker starts with '$', remove it
    if ticker.startswith('$'):
        ticker = ticker[1:]

    # Retrieve valuation metrics from openbb.stocks.ca.screener
    df = openbb.stocks.ca.screener([ticker], data_type="valuation")    

    # Drop unnecessary columns
    df = df.drop(columns=['Change', 'Volume', 'Price', 'EPS next 5Y', 'PEG', 'Sales past 5Y'])

    # Fill NA/NaN values with 0
    df = df.fillna(0)

    # Format the Market Cap by converting it to millions and appending 'M'
    df['Market Cap'] = df['Market Cap'].apply(lambda x: "${0:.0f} M".format(x/1000000))

    # Convert the data frame to a JSON string
    json_string = df.to_json(orient='records')
    
    # Convert the JSON string to a Python string
    data = json.dumps(json_string)
    
    # Return the data
    return data


@command(
    "get_performance_metrics",  # command name
    "Performance metrics for a ticker",  # command description
    '"ticker": "<ticker>", "statements": "<statements>"',  # command arguments in JSON format
)
def get_performance_metrics(ticker: str, statements: str) -> str:
    """
    This function retrieves the performance metrics for a given stock ticker.
    
    Parameters:
    ticker (str): The ticker symbol for the stock. It can be prefixed with a '$' symbol.
    statements (str): Not used in the current function. It could be used to specify financial statements to retrieve.
    
    Returns:
    str: A JSON string representing the performance metrics for the stock.
    """
    # If the ticker starts with '$', remove it
    if ticker.startswith('$'):
        ticker = ticker[1:]

    # Retrieve performance metrics from openbb.stocks.ca.screener
    df = openbb.stocks.ca.screener([ticker], data_type="performance")    
    
    # Convert performance metrics to percentages
    df['Perf Week'] = df['Perf Week'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Perf Month'] = df['Perf Month'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Perf Quart'] = df['Perf Quart'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Perf Half'] = df['Perf Half'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Perf Year'] = df['Perf Year'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Perf YTD'] = df['Perf YTD'].apply(lambda x: "{0:.1f}%".format(x*100))
    
    # Fill NA/NaN values with an empty string
    df = df.fillna("")
                         
    # Convert the data frame to a JSON string
    json_string = df.to_json(orient='records')
    
    # Convert the JSON string to a Python string
    data = json.dumps(json_string)
    
    # Return the data
    return data

@command(
    "get_ownership_metrics",  # command name
    "Ownership metrics for a ticker",  # command description
    '"ticker": "<ticker>", "statements": "<statements>"',  # command arguments in JSON format
)
def get_ownership_metrics(ticker: str, statements: str) -> str:
    """
    This function retrieves the ownership metrics for a given stock ticker.
    
    Parameters:
    ticker (str): The ticker symbol for the stock. It can be prefixed with a '$' symbol.
    statements (str): Not used in the current function. It could be used to specify financial statements to retrieve.
    
    Returns:
    str: A JSON string representing the ownership metrics for the stock.
    """
    # If the ticker starts with '$', remove it
    if ticker.startswith('$'):
        ticker = ticker[1:]

    # Retrieve ownership metrics from openbb.stocks.ca.screener
    df = openbb.stocks.ca.screener([ticker], data_type="ownership")
    
    # Drop unnecessary columns
    df = df.drop(columns=['Market Cap', 'Change', 'Volume', 'Avg Volume', 'Price'])
    
    # Fill NA/NaN values with an empty string
    df = df.fillna("")
    
    # Convert the data frame to a JSON string
    json_string = df.to_json(orient='records')
    data = json.dumps(json_string)
    return data   

@command(
    "get_technical_analysis_summary",  # command name
    "Summary of technical analysis",  # command description
    '"ticker": "<ticker>"',  # command arguments in JSON format
)
def get_technical_analysis_summary(ticker: str) -> str:
    """
    This function retrieves the summary of technical analysis for a given stock ticker.
    
    Parameters:
    ticker (str): The ticker symbol for the stock. It can be prefixed with a '$' symbol.
    
    Returns:
    str: A string representing the summary of technical analysis for the stock.
    """
    # If the ticker starts with '$', remove it
    if ticker.startswith('$'):
        ticker = ticker[1:]

    # Retrieve technical analysis summary from openbb.stocks.ta.summary
    return openbb.stocks.ta.summary(ticker)
 
       
@command(
    "get_analyst_ratings",  # command name
    "Get analyst ratings",  # command description
    '"ticker": "<ticker>"',  # command argument in JSON format
)
def get_analyst_ratings(ticker: str) -> str:
    """
    This function retrieves the analyst ratings for a given stock ticker.
    
    Parameters:
    ticker (str): The ticker symbol for the stock. It can be prefixed with a '$' symbol.
    
    Returns:
    str: A JSON string representing the analyst ratings for the stock.
    """
    # If the ticker starts with '$', remove it
    if ticker.startswith('$'):
        ticker = ticker[1:]
        
    # Retrieve analyst ratings from openbb.stocks.fa.rating
    df_rating = openbb.stocks.fa.rating(ticker)
    
    # Select the first row from the data frame
    df_rating = df_rating.head(1)
    
    # Convert the data frame to a JSON string
    json_string = df_rating.to_json(orient='records')
    
    # Convert the JSON string to a Python string
    data = json.dumps(json_string)
    
    # Return the data
    return data

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
    active = openbb.crypto.dd.active(symbol=symbol, interval=interval, start_date=start_date, end_date=end_date)
    json_string = active.to_json(orient='records')
    data = json.dumps(json_string)
    return data 

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
    active = openbb.crypto.dd.active(symbol=symbol, interval=interval, start_date=start_date, end_date=end_date)
    json_string = active.to_json(orient='records')
    data = json.dumps(json_string)
    return data 