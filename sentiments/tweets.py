###########################################################################################
# Functions to do with fetching, cleaning, and analyzing data from tweepy (Twitter API).  #
# Written by Lewis Kim.                                                                   #
###########################################################################################

import tweepy
from twython import Twython
import pandas as pd
import numpy as np
import re

from datetime import datetime
import os
import pickle

# Twitter API Credentials. Enter in your dev. account's API keys/secrets.

consumer_key = "3daaCRqE9kbiVSxxNjmmx1iGp"
consumer_secret = "nqaBQPe54hx7sJeFtVWTK8QyhBo5J75nVlqFERQ6SaMFerBb3d"
access_token = "967529922724966400-AtEXEfM4mxxkhfBtDshgh8eV8ZTimDI"
access_secret = "CT9biXzWYloFVpTsaYVvfwbGpHHGQo0arS4dnhK7Wo1wA"

# Read in the VADER Lexicon into a pandas dataframe called 'sent'.

filepath = os.path.dirname(os.path.realpath(__file__)) + '/vader_lexicon.txt'

sent = pd.read_table(filepath, header=None, usecols=[0, 1])
sent = sent.rename(columns = {0: 'token', 1: 'polarity'})
sent = sent.set_index('token', drop = True)

"""Return the list of tweepy's Status objects (from user_timeline()) for the given USERNAME."""
def get_twitter_data(username):
	
	# Get authorized by Twitter, and set up tweepy.
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	return api.user_timeline(screen_name = username, count = 200)

"""Return a pandas dataframe with its columns as tweet text, retweet count, tweet time,
   tweet location, pst_time (see line ), hour (see line ), no_punc (see line ), and
   polarity (see line ) indexed by tweet id. The data for the columns comes from TWEETS."""
def create_tweet_df(tweets,):
	#Initialize an empty dataframe.
	df = pd.DataFrame([])

	# Add columns of twitter data to df.
	df['id'] = [tweet.id for tweet in tweets]
	df['text'] = [tweet.text for tweet in tweets]  # Some entries may be missing (see line ).
	df['retweet_count'] = [tweet.retweet_count for tweet in tweets]
	df['time'] = [tweet.created_at for tweet in tweets]
	df['location'] = [tweet.user.location for tweet in tweets]

	# Set the index of df as the tweet ids, and convert the text in the 'text' column to all
	# lowercase.
	df = df.set_index('id')
	df['text'] = df['text'].str.lower()

	# Create a new column called 'pst_time' that converts the datetime values in 'time' to follow
	# the Pacific Standard Time (PST).
	df['pst_time'] = (
    df['time'].dt.tz_localize("UTC")   # Set initial timezone to UTC.
                 .dt.tz_convert("America/Los_Angeles") # Convert to Pacific Standard Time.
                 )

	# Create a new column called hours that contains the hour of the day as floating point number
	# computed by: hour + minute/60 + second/60^2.
	df['hour'] = [get_hour(val.time()) for val in df['pst_time']]

	# Remove all punctuations from 'text' and save it as a new column, 'no_punc'.
	punct_re = r''"[^\w\d\s]"
	df['no_punc'] = df['text'].str.replace(punct_re, ' ')

	# Convert the tweets in 'no_punc' into a tidy format to make sentiments easier to calculate.
	# The index of the table should be the IDs of the tweets, repeated once for every word in the tweet.
	# tidy_format has 2 columns:
	# 1) num: the location of the word in the tweet.
	# 2) word: the individual words of each tweet.
	tempDF = df['no_punc'].str.split(expand = True)

	tempDF2 = pd.DataFrame(tempDF.stack(), columns = ['word'])
	tempDF2.reset_index(inplace = True)

	tidy_format = tempDF2.rename(columns = {'id': 'id', 'level_1': 'num', 'word': 'word'})
	tidy_format.set_index('id', inplace = True)

	# Add a polarity column to df. The polarity column contains the sum of the sentiment polarity of
	# each word in the text of the tweet.
	tf2 = tidy_format.reset_index()
	words = sent.reset_index().rename(columns = {'token': 'word'})

	tempPol = pd.merge(tf2, words, how = 'left', on = 'word')

	pol = tempPol.groupby('id').sum()
	pol.drop('num', axis = 1, inplace = True)

	df['polarity'] = pol['polarity']

	df = df.dropna()

	# Filter out the retweets.
	# df = df[df['text'].str[0:2] != 'rt']

	return df

### Utility functions. ###

"""Return the hour of the given DAY as a floating point number computed by:
   hour + minute/60 + second/60^2."""
def get_hour(day):
	hour = day.hour + day.minute/60 + day.second/3600
	return hour


### Analysis functions. ###

"""Return an overall sentiment (string) for a given polarity SCORE. Sentiments
   range from very positive, generally positive, slightly positive, neutral,
   slightly negative, generally negative, and very negative.
   Scale may need readjustments."""
def get_sentiment(score):
	# Ranges for score-to-sentiment scale, from the VADER Lexicon documentation.
	# Negative ranges.
	if score < -4:
		return "extremely negative."

	elif score >= -4 and score <= -3:
		return "very negative."

	elif score > -3 and score <= -2:
		return "fairly negative."

	elif score > -2 and score <= -1:
		return "negative."

	elif score > -1 and score < -0.1:
		return "slightly negative."

	# Neutral range.
	elif score >= -0.1 and score <= 0.1:
		return "neutral."

	# Positive ranges.
	elif score > 0.1 and score <= 1:
		return "slightly positive."

	elif score > 1 and score <= 2:
		return "positive."

	elif score > 2 and score <= 3:
		return "fairly positive."

	elif score > 3 and score <= 4:
		return "very positive."

	elif score > 4:
		return "extremely positive."


"""Return a list of tuples of top 10 most positive tweets and their dates, from the
   selected user's Twitter DATA."""
def get_positive_tweets(data):
	
	# Sort 'polarity' values in descending order.
	df = data.sort_values('polarity', ascending = False)

	tweets = df['text'].tolist()[0:10]
	dates = df['pst_time'].tolist()[0:10]
	polarities = [round(x, 2) for x in df['polarity'].tolist()[0:10]]

	pos_tweets = [(x, y, z) for x, y, z in zip(tweets, dates, polarities)]

	return pos_tweets


"""Return a list of tuples of top 10 most negative tweets and their dates, from the
   selected user's Twitter DATA."""
def get_negative_tweets(data):

	# Sort 'polarity' values in ascending order.
	df = data.sort_values('polarity', ascending = True)

	tweets = df['text'].tolist()[0:10]
	dates = df['pst_time'].tolist()[0:10]
	polarities = [round(x, 2) for x in df['polarity'].tolist()[0:10]]

	neg_tweets = [(x, y, z) for x, y, z in zip(tweets, dates, polarities)]

	return neg_tweets


"""Use Twython to get the user with USERNAME's Twitter profile image link."""
def get_user_img(username):
	t = Twython(app_key=consumer_key,
		app_secret=consumer_secret,
		oauth_token=access_token,
		oauth_token_secret=access_secret)

	return t.show_user(screen_name=username)

