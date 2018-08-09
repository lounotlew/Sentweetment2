from django.shortcuts import render
from django.http import HttpResponse
from . import tweets
# Create your views here.

def index(request):
	username = request.GET['username']
	context = {'username': username}

	twitter_data = tweets.get_twitter_data(username)
	sentiment_data = tweets.create_tweet_df(twitter_data)

	# print(sentiment_data['polarity'].tolist())

	# print(len(sentiment_data))

	return render(request, "sentiments/analysis.html", context = context)