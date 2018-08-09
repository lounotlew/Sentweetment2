from django.shortcuts import render
from django.http import HttpResponse

import statistics
from . import tweets

# Create your views here.

def index(request):
	username = request.GET['username']
	context = {'username': username}

	twitter_data = tweets.get_twitter_data(username)
	sentiment_data = tweets.create_tweet_df(twitter_data)

	# sentiment_data columns: ['text' 'retweet_count' 'time' 'location' 'pst_time' 'hour' 'no_punc', 'polarity']

	avg_polarity = round(statistics.mean(sentiment_data['polarity'].tolist()), 4)

	top_10_pos = tweets.get_positive_tweets(sentiment_data)
	top_10_neg = tweets.get_negative_tweets(sentiment_data)

	# print(sentiment_data['polarity'].tolist())

	# print(len(sentiment_data))

	context = {"username": username, "avg_polarity": avg_polarity, "top_10_pos": top_10_pos, "top_10_neg": top_10_neg}

	return render(request, "sentiments/analysis.html", context = context)