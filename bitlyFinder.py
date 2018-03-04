# Uses Tweepy to communicate with Twitter API and search the stream for
# the keywords [bit ly], then filters the 'urls' field for bit.ly links
# before printing matching results

import tweepy
import json
import time

# API Access key variables
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


def buildURLList():
    urlList = []
    urlList.append('http://bit.ly/')
    urlList.append('http://cnn.it/')
    urlList.append('http://huff.to/')
    urlList.append('http://bbc.it/')
    urlList.append('http://bbc.in/')
    urlList.append('http://nyti.ms/')
    urlList.append('http://fxn.ws/')
    return urlList


# Listens to responses from tweepy stream
class StdOutListener(tweepy.StreamListener):
    # Init function
    def __init__(self, time_limit, path_and_filename):
        self.start_time = time.time()
        self.limit = time_limit
        self.filename = path_and_filename

    # Prints data that contains bit.ly links
    def on_data(self, data):
        obj = json.loads(data)
        if 'entities' in obj and 'urls' in obj['entities'] and len(obj['entities']['urls']) > 0:
            expUrl = obj['entities']['urls'][0]['expanded_url']
            # if expUrl is None:
            #        print('We have a None')
            urlList = buildURLList()  # List of URLs that are OK, e.g. cnn.it, bit.ly etc.
            goodURL = False
            for url in urlList:
                if (expUrl is not None) and (url in expUrl): goodURL = True
            if goodURL:
                tweetsFile = open(self.filename, 'a+')
                if (time.time() - self.start_time) < self.limit:
                    tweetsFile.write(data)
                    return True
                else:
                    tweetsFile.close()
                    return False
        return True

    def on_error(self, status):
        print(status)


def readTokensFromConf():
    # We want to modify the global variables
    global access_token, access_token_secret, consumer_secret, consumer_key
    access_token = '741298123088252928-lvwlT3tnKkJp7IPHHBfagm7RIQtfvOw'
    access_token_secret = 'rXYyhuBRLHdi9scnURd7wRBFZS59RyWfhIpco1RgIczdK'
    consumer_key = 'nZ0GXjkq7fGAM2WJVObMSRdkl'
    consumer_secret = 'DDTRELK5IpXDcXmeMmOkmWXEXOm7C8bLUCAZuIrS1dL06YEFW8'


def collectTweets(path_and_filename, seconds_to_collect):
    # Read tokens and keys from conf
    readTokensFromConf()
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Streaming API
    listener = StdOutListener(time_limit=seconds_to_collect, path_and_filename=path_and_filename)
    stream = tweepy.Stream(auth, listener)
    # KEYWORDS
    # Note: Important to not use dots in the URLs in the filter (see below)
    print('Starting keyword filtering!')
    stream.filter(track=['bit ly', 'cnn it', 'huff to', 'bbc it', 'bbc in', 'nyti ms', 'fxn ws'])
    print("Done streaming!")
