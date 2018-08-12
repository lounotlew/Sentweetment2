from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

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

	# Remove the "_normal.jpg" tag at the end to get the full-size image.
	img = tweets.get_user_img(username)['profile_image_url']
	user_img = tweets.get_user_img(username)['profile_image_url'][0:len(img)-11] + ".jpg"

	#
	sentiment_data['tweet_date'] = sentiment_data['pst_time'].dt.date
	df = sentiment_data.groupby('tweet_date').sum().reset_index(drop = False)

	labels = df['tweet_date'].tolist()
	values = df['polarity'].tolist()

	request.session['sentiment_data'] = sentiment_data

	context = {"username": username, "avg_polarity": avg_polarity, "sentiment": sentiment,
		"top_10_pos": top_10_pos, "top_10_neg": top_10_neg,"user_img": user_img, "labels": labels, "values": values}

	return render(request, "sentiments/analysis.html", context = context)


# 
def graphs(request):
	print(request.session['sentiment_data'])

	return render(request, "sentiments/graphs.html")







