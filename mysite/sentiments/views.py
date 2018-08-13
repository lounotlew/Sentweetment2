from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

import json
import datetime

import statistics
from . import tweets
# Create your views here.

# 
def index(request):
	try:
		# Check if the username is valid, i.e. if tweepy actually returns any data.
		twitter_data = tweets.get_twitter_data(request.GET['username'])

		if len(twitter_data) == 0:
			messages.error(request, "That Twitter account does not exist, or has no tweets.")
			return redirect("/")		

	except:
		messages.error(request, "That Twitter account does not exist, or has no tweets.")
		return redirect("/")

	username = request.GET['username']

	# sentiment_data columns: ['text' 'retweet_count' 'time' 'location' 'pst_time' 'hour' 'no_punc', 'polarity']
	sentiment_data = tweets.create_tweet_df(twitter_data)

	avg_polarity = round(statistics.mean(sentiment_data['polarity'].tolist()), 4)
	sentiment = tweets.get_sentiment(avg_polarity)

	# Top 10 positive/negative tweets.
	top_10_pos = tweets.get_positive_tweets(sentiment_data)
	top_10_neg = tweets.get_negative_tweets(sentiment_data)

	img = tweets.get_user_img(username)['profile_image_url']
	# Remove the "_normal.jpg" tag at the end to get the full-size image.
	user_img = tweets.get_user_img(username)['profile_image_url'][0:len(img)-11] + ".jpg"

	# Add a new column called "tweet_date" to sentiment_data that consists of all tweet dates, without specific times.
	# (i.e. 3-14-2018 8:00 PM becomes 3-14-2018). Then group the sentiment_data by "tweet_date", and save to a new df.
	sentiment_data['tweet_date'] = sentiment_data['pst_time'].dt.date
	df = sentiment_data.groupby('tweet_date').mean().reset_index(drop = False)

	request.session['df'] = df

	context = {"username": username, "avg_polarity": avg_polarity, "sentiment": sentiment,
		"top_10_pos": top_10_pos, "top_10_neg": top_10_neg,"user_img": user_img}

	return render(request, "sentiments/analysis.html", context = context)


# 
def graphs(request):
	df = request.session['df']

	avg_polarity = round(statistics.mean(df['polarity'].tolist()), 4)

	values = [round(x, 2) for x in df['polarity'].tolist()]
	labels = [x.isoformat() for x in df['tweet_date'].tolist()]

	series = [[((datetime.datetime.strptime(x, '%Y-%m-%d'))-datetime.datetime(1970,1,1)).total_seconds()*1000, y] for x, y in zip(labels, values)]

	context = {"data": json.dumps(series), "username": request.GET['username']}

	return render(request, "sentiments/graphs.html", context)







