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

	num_tweets = len(sentiment_data)

	avg_polarity = round(statistics.mean(sentiment_data['polarity'].tolist()), 4)
	median_polarity = statistics.median(sentiment_data['polarity'].tolist())
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

	polarity_stats = {'totalAvgPolarity': avg_polarity, 'medianTweetPolarity': median_polarity}

	request.session['username'] = username
	request.session['df'] = df
	request.session['sentiment_data'] = sentiment_data
	request.session['polarity_stats'] = polarity_stats
	request.session['num_tweets'] = num_tweets

	context = {"username": username, "avg_polarity": avg_polarity, "sentiment": sentiment,
		"top_10_pos": top_10_pos, "top_10_neg": top_10_neg,"user_img": user_img}

	return render(request, "sentiments/analysis.html", context = context)


# 
def graphs(request):
	username = request.session['username']

	df = request.session['df']
	sentiment_data = request.session['sentiment_data']

	organized_dates = sentiment_data.sort_values('pst_time', ascending = True).reset_index(drop = True)['pst_time'].dt.date.tolist()

	diff = organized_dates[-1] - organized_dates[0]
	delta = diff.days

	# Labels: tweet times aggregated by their dates, with time dropped. (i.e. 3-14-2018 3:00 PM and 3-14-2018 1:00 AM grouped to 3-14-2018).
	labels = [x.isoformat() for x in df['tweet_date'].tolist()]
	# Values: Average polarity scores per tweet date (items of labels).
	values = [round(x, 2) for x in df['polarity'].tolist()]
	# Convert labels to an integer as the # of seconds after 1970-1-1 so it can be JSONified.
	series = [[((datetime.datetime.strptime(x, '%Y-%m-%d'))-datetime.datetime(1970,1,1)).total_seconds()*1000, y] for x, y in zip(labels, values)]

	# Round the values of SENTIMENT_DATA from views() to the nearest integer, and group by their counts.
	# Use this column to get a distribution of polarity scores.
	sentiment_data['rounded_pol'] = sentiment_data['polarity'].apply(lambda x: round(x))
	distribution = sentiment_data.groupby('rounded_pol').count().sort_index(ascending = True)

	# Distribution of polarity scores rounded to nearest integer.
	# Polarity bins converted to string for Highcharts.
	grouped_polarities = [str(x) for x in distribution.index.tolist()]
	counts = [int(x) for x in distribution['text'].tolist()]

	# Statistics.
	totalAvgPolarity = request.session['polarity_stats']['totalAvgPolarity']
	dailyAvgPolarity = round(statistics.mean(df['polarity'].tolist()), 4)
	medianTweetPolarity = request.session['polarity_stats']['medianTweetPolarity']
	medianDailyAvgPolarity = round(statistics.median(df['polarity'].tolist()), 4)

	num_tweets = request.session['num_tweets']

	context = {"data": json.dumps(series), "categories": json.dumps(grouped_polarities), "counts": json.dumps(counts), "username": username,
		"totalAvgPolarity": totalAvgPolarity, "dailyAvgPolarity": dailyAvgPolarity, "medianTweetPolarity": medianTweetPolarity,
		"medianDailyAvgPolarity": medianDailyAvgPolarity, "num_tweets": num_tweets, "delta": delta}

	return render(request, "sentiments/graphs.html", context)


#
def all_tweets(request):
	username = request.session['username']
	sentiment_data = request.session['sentiment_data']

	# Sort sentiment_data by polarity, in ascending order.
	sentiment_data = sentiment_data.sort_values('polarity', ascending = True)

	tweets = sentiment_data['text'].tolist()
	time = sentiment_data['pst_time'].tolist()
	polarity = [round(x, 2) for x in sentiment_data['polarity'].tolist()]

	data = zip(tweets, time, polarity)

	context = {"username": username, "data": data}

	return render(request, "sentiments/all-tweets.html", context = context)


#
def searched_tweets(request):
	



	return render(request, "searched-tweets.html")








