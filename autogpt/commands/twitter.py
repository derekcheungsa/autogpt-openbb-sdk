"""A module that contains a command to send a tweet."""
import os

import tweepy
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, TwitterTweetReader
from IPython.display import Markdown, display
import os
from autogpt.commands.command import command
import logging
import sys

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
load_dotenv()
logging.basicConfig(level=logging.CRITICAL + 1)

#Prototype of getting stock tickers from twitter
@command(
    "stocks_from_tweet",
    "Get stocks from twitter",
    '',
)
def stocks_from_tweet() -> str:
    reader = TwitterTweetReader(BEARER_TOKEN)
    documents = reader.load_data(["mintzmyer"])

    index = GPTSimpleVectorIndex.from_documents(documents)
    response = index.query("Show stock tickers mentioned most positively")
    return response


@command(
    "send_tweet",
    "Send Tweet",
    '"tweet_text": "<tweet_text>"',
)
def send_tweet(tweet_text: str) -> str:
    """
      A function that takes in a string and returns a response from create chat
        completion api call.

    Args:
      tweet_text (str): Text to be tweeted.

      Returns:
          A result from sending the tweet.
    """
    consumer_key = os.environ.get("TW_CONSUMER_KEY")
    consumer_secret = os.environ.get("TW_CONSUMER_SECRET")
    access_token = os.environ.get("TW_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TW_ACCESS_TOKEN_SECRET")
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Send tweet
    try:
        api.update_status(tweet_text)
        return "Tweet sent successfully!"
    except tweepy.TweepyException as e:
        return f"Error sending tweet: {e.reason}"
