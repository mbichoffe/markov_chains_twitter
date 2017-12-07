#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import os
import re
import time
import codecs
import tweepy
import urllib3
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN_KEY = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

###ENDPOINTS###
REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
RETURN_URL = 'http://localhost:5000/oauth'

# authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# In case service is unavailable temporarily, bad gateway, timeout, overcapacity
# or internal error, we can try to call the API again
errorCodesList = ['130', '131', '500', '502', '503', '504']

# If folder doesn't exist, create one
fldName = os.getcwd() + "/data"
if not os.path.exists(os.path.dirname(fldName)):
    try:
        os.makedirs(os.path.dirname(fldName))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise


def wait(minutes):
    """Return time in sec to wait before making a new request to API."""
    seconds = minutes * 60
    time.sleep(seconds)


def checkError(response, screen_name):
    """
    Evaluate error response returned from API call, try again or print error
    message to terminal.

    """
    if response is None:
        print('Retrying')
        wait(3)
        get_all_tweets(screen_name)
    else:
        msg = response.text
        regex = re.match("^.*?\"code\":([\d]+),\"message\":\"(.*?)\.\".+", msg)
        if regex:
            code = regex.group(1)
            message = regex.group(2)
            if code in errorCodesList:
                print('Retrying')
                wait(3)
                get_all_tweets(screen_name)
            else:
                print("\n*Error*\nUser: " + screen_name + " Message: " +
                      message + ". Code: " + code + ".\n")
                pass
        else:
            if "Not authorized" in msg:
                print("\n*Error*\nUser: " + screen_name +
                      " Message: This account's tweets are protected.\n")
                pass
            else:
                print(msg)
                pass


def get_all_tweets(screen_name):
    """
    Request timelime from user specified in argument.
    If successful, store tweets in .txt form .
    """
    try:
        # Twitter only allows access to a users most recent 3240 tweets 
        # with this method

        # initialize list to hold tweets:
        all_tweets = []

        # make initial request for the most recent tweets
        # (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)
        # save the most recent tweets
        all_tweets.extend(new_tweets)
        # save the id of the oldest tweet minus one
        oldest = all_tweets[-1].id - 1

        # keep retrieving tweets until there are no more tweets left
        while len(new_tweets) > 0:

            print "User: " + screen_name
            print "Getting tweets before {}".format(oldest)

            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200,
                                           max_id=oldest)

            # save the most recent tweets
            all_tweets.extend(new_tweets)

            # update the id of the oldest tweet minus one
            oldest = all_tweets[-1].id - 1

            print("...{} tweets downloaded so far\n").format(len(all_tweets))

        # transform tweepy tweets into utf-8 encoded text:
        for tweet in all_tweets:
            text = tweet.text
            # write to txt file
            try:
                with codecs.open(os.getcwd() +
                                 "/data/" + screen_name + ".txt",
                                 "a", "utf-8", "ignore") as outFile:
                    outFile.write(text + "\n")  # use space as sentence finisher
            # Emojis can't be encoded into .txt file, so only
            # accept tweets without them
            except UnicodeError:
                print('Tweet contained non UTF-8 chars; discarded.')
            except urllib3.exceptions:
                print('Tweet raised some other exception; discarded.')


    except (Timeout, ConnectionError, ReadTimeoutError, ProtocolError) as exc:
        print("\n*Timeout Error*\nRetrying ...\n")
        wait(3)
        get_all_tweets(screen_name)

    except tweepy.TweepError as e:
        checkError(e.response, screen_name)

    except IndexError:
        print("\nUser \"" + screen_name +
              "\" didn't have enough tweets to retrieve ...\n")
        pass
