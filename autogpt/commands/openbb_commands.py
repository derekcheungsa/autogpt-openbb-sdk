"""A module that contains a command to send a tweet."""
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
    "get_financial_metrics",
    "Financial metrics for a ticker",
    '"ticker": "<ticker>", "statements": "<statements>"',
)
def get_financial_metrics(ticker, statements):    
    if ticker.startswith('$'):
        ticker= ticker[1:]

    df=openbb.stocks.ca.screener([ticker], data_type="financial")    
    df = df.drop(columns=['Change', 'Volume', 'Earnings', 'Price','Market Cap'])

    # Format the output better
    df['Dividend']=df['Dividend'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['ROA']=df['ROA'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['ROE']=df['ROE'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['ROI']=df['ROI'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Gross M']=df['Gross M'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Oper M']=df['Oper M'].apply(lambda x: "{0:.1f}%".format(x*100))
    df['Profit M']=df['Profit M'].apply(lambda x: "{0:.1f}%".format(x*100))                          
    json_string = df.to_json(orient='records')
    data = json.dumps(json_string)
    return data   

@command(
    "get_technical_analysis_summary",
    "Summary of technical analysis",
    '"ticker": "<ticker>"',
)
def get_technical_analysis_summary(ticker):  
    if ticker.startswith('$'):
        ticker= ticker[1:]
    return openbb.stocks.ta.summary(ticker)   
        

@command(
    "get_sector_valuations",
    "Get best sector valuations",
    '"sector": "<sector>"',
)
def get_sector_valuations(sector: str) -> str:
    # Assumes there is a preset that is available by sector 
    df=openbb.stocks.screener.screener_data(preset_loaded=f"{sector}_value_stocks.ini",data_type = 'valuation')
    df.sort_values(by='P/E', ascending=True, inplace=True)
    ticker_df = df[['Ticker']]
    ticker_df=ticker_df.head(3)
    json_string = ticker_df.to_json(orient='records')
    data = json.dumps(json_string)
    return data

@command(
    "get_analyst_ratings",
    "Get analyst ratings",
    '"ticker": "<ticker>"',
)
def get_analyst_ratings(ticker: str) -> str:
   if ticker.startswith('$'):
        ticker=ticker[1:]
   df_rating=openbb.stocks.fa.rating(ticker)
   df_rating=df_rating.head(1)
   json_string = df_rating.to_json(orient='records')
   data = json.dumps(json_string)
   return data
