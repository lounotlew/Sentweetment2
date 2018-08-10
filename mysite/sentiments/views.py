from django.shortcuts import render
from django.http import HttpResponse

import statistics
from . import tweets

# Create your views here.

def index(request):
	username = request.GET['username']
	context = {'username': username}

	twitter_data = tweets.get_twitter_data(username)
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

	context = {"username": username, "avg_polarity": avg_polarity, "sentiment": sentiment,
		"top_10_pos": top_10_pos, "top_10_neg": top_10_neg,"user_img": user_img}

	return render(request, "sentiments/analysis.html", context = context)