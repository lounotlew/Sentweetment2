# Sentweetment 2 - A Django Web Application for Twitter Sentiment Analysis
> Written by Lewis Kim

### Description

Sentweetment 2 is a Django web application with a relatively minimal and simple user interface for performing sentiment analysis on Twitter accounts (users). Using the [VADER Lexicon](https://github.com/cjhutto/vaderSentiment), Sentweetment 2 tokenizes each tweet made by a user (for a max. of 200 tweets, limited by the Twitter API) to individual words, and applies a polarity score to each word. Then, these individual scores are aggregated per-tweet to give an overall tweet polarity score. These scores are also used to calculate an overall user polarity score (by their average), and ultimately the general sentiment of a Twitter account/user. All of these operations are performed through [``pandas``](https://pandas.pydata.org/).

This methodology is based on [UC Berkeley's Data Science 100 Project 1: "Trump, Twitter, and Text"](https://github.com/cjhutto/vaderSentiment).

Although context isn't taken into account (yet), the general idea is that the more positive/negative words a tweet contains, the more likely it is that that tweet is positive/negative.

The user interface displays a simple average tweet polarity score and a sentiment (e.g. positive, slightly negative, extremely positive) at a glance, and optionally offers a more detailed analysis, such as polarity score distributions, trend graphs, and useful statistics.

This web application is mostly based on an earlier project I did, [Sentweetment](https://github.com/lounotlew/Sentweetment), and is essentially a port from a ``tkinter`` interface to a Django web interface.

### Installation

Sentweetment 2 was written in Python 3.6, and may not work with Python 2.

Required packages/frameworks:
- ``django``: (``pip3 install django``)
- ``pandas``: (``pip3 install pandas``)
- ``tweepy``:(``pip3 install tweepy``)
- ``twython``: (``pip3 install twython``)
- ``Highcharts``: (use a CDN or download the .js file)

To view this website, please visit [placeholder link]().

### References

References to the libraries and packages used in Sentweetment 2:

1) ``django``: https://www.djangoproject.com/
2) ``pandas``: https://pandas.pydata.org/
3) ``tweepy``: http://www.tweepy.org/
4) ``twython``: https://twython.readthedocs.io/en/latest/
4) ``Highcharts``: https://www.highcharts.com/
