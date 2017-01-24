# sentiment.py
# Demonstrates connecting to the twitter API and accessing the twitter stream
# Author: Jordan Ott
# Version 1.1
# Date: February 16, 2016

import twitter

# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information
# on Twitter's OAuth implementation.

CONSUMER_KEY = '******************************'
CONSUMER_SECRET = '******************************'
OAUTH_TOKEN = '******************************'
OAUTH_TOKEN_SECRET = '******************************'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)



# XXX: Set this variable to a trending topic,
# or anything else for that matter. The example query below
# was a trending topic when this content was being developed
# and is used throughout the remainder of this chapter.

def sentiment_analysis(q):

    count = 10000
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets

    search_results = twitter_api.search.tweets(q=q, count=count)
    
    statuses = search_results['statuses']
    # Iterate through 5 more batches of results by following the cursor
    for _ in range(5):
        try:
            next_results = search_results['search_metadata']['next_results']
        except: # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
    
    # Show one sample search result by slicing the list...
    status_texts = [ status['text'] for status in statuses ]
    # Compute a collection of all words from all tweets
    words = [ w for t in status_texts for w in t.split() ]
    
    # Get the original tweet id for a tweet from its retweeted_status node
    # and insert it here in place of the sample value that is provided
    # from the text of the book
    # Sentiment analysis
    sent_file = open('sentiment.txt')

    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    score = 0
    for word in words:
        #uword = word.encode('utf-8')
        if scores.get(word,0):
            score += scores[word]
    return float(score)
search_term_one = "google"

term_one_score = sentiment_analysis(search_term_one)

print("google sachs sentiment: ", term_one_score)

#chcp 65001 to fix codec issue