# -*- coding: cp1252 -*-
# Handles the Bitly data

import json
from urlparse import urlsplit
import bitlyextractor
import random
from operator import itemgetter
import datetime
import time
import bitly_api
import ast
from multiprocessing.dummy import Pool as ThreadPool

# Set up API auth
login = 'o_1ej62d4rq7'
api_key = 'R_a1f7decfc0f64426987e083fc9cedfcd'
generic_token = 'e82b679532f66075a939553af072fc3a1b3d0888'
# Open connection
c = bitly_api.Connection(login=login, api_key=api_key, access_token=generic_token)

# Object to hold our json data
tweetsData = []
expandedData = []
PATTERNLIST = [
    'www.bbc.co.uk',
    'www.bbc.com',
    'www.cnn.com',
    'www.abcnews.com',
    'www.foxnews.com',
    'www.washingtonpost.com',
    'www.theguardian.com',
    'www.breitbart.com',
    'endingthefed.com',
    'www.ft.com',
    'www.thetimes.co.uk',
    'time.com',
    'www.reuters.com',
    'uk.reuters.com',
    'www.cbsnews.com',
    'www.huffingtonpost.com',
    'www.huffingtonpost.co.uk',
    'www.thepoliticalinsider.com',
    'denverguardian.com',
    'conservativestate.com',
    'www.burrardstreetjournal.com',
    'abcnews.com.co',
    'libertynews.com',
    'www.yesimright.com',
    'twitchy.com',
    'worldnewsdailyreport.com',
    'donaldtrumpnews.co'
]

shortURLFilePath = './data/seenShortURLs.txt'

# Reads a number of random Tweets from a file
def handleTweets(tweetsPath, numToRead, outfile, newsOnly):
    start_time = time.time()
    file = open(outfile, 'a+')
    print "Starting handleTweets"
    longNewsURLs = open('./data/links/UnknownArticlesToBeExtracted.txt', 'a+')

    # Open the file
    tweetsFile = open(tweetsPath, 'r')

    # Read from the tweets file to tweetsData
    for line in tweetsFile:
        try:
            tweet = json.loads(line)
            tweetsData.append(tweet)
        except:
            continue
    tweetsFile.close()
    shortURLFile = open(shortURLFilePath, "r")
    shortURLDict = {}
    for line in shortURLFile:
        if line != '':
            shortURLDict = ast.literal_eval(line)
    
    bitlyDicts = []
    # Put URL info from the Tweets data in the tweets array
    for tw in tweetsData:
        # Save ID and bitly link in dict array
        if (tw['entities']['urls'][0]['expanded_url'] not in shortURLDict):
            dict = {'id': tw['id'], 'short_url': tw['entities']['urls'][0]['expanded_url'], 'long_url': '',
                    'bitly_global_hash': '', 'bitly_user_hash': '', 'refs': '', 'countries': '', 'global_clicks': '',
                    'user_clicks': ''}
            bitlyDicts.append(dict)
            #Glomm inte att lagga till url:en till dictionary:n over tidigare anvanda sedda url:er.
            shortURLDict[tw['entities']['urls'][0]['expanded_url']] = '1'
        else:
            #Inkrementera value till key:n for den hittade url:en
            shortURLDict[tw['entities']['urls'][0]['expanded_url']] = str(int(shortURLDict[tw['entities']['urls'][0]['expanded_url']])+1)
    print ("Number of tweets: ", len(tweetsData))
    shortURLFile.close()
    shortURLFile = open(shortURLFilePath, "w")
    shortURLFile.write(str(shortURLDict))
    shortURLFile.close()
    samples = pickSamples(bitlyDicts=bitlyDicts, numToRead=numToRead)

    print ("Number of samples: ", len(samples))
    uniqueBitlys = pickUnique(bitlySamples=samples)
    print ("Number of unique samples: ", len(uniqueBitlys))
    URLs = resolveBitlys(uniqueBitlys)
    print (time.time() - start_time)
    shortURLs = []
    longURLs = []
    globalHashes = []
    userHashes = []
    newsSamples = []

    # We split the tupe URLs into three arrays
    for url in URLs:
        shortURLs.append(url[0])
        longURLs.append(url[1])
        globalHashes.append(url[2])
        userHashes.append(url[3])
        r = urlsplit(url[1])
        if (newsOnly == 1 and isUniqueNews(r, url[1])):
            longNewsURLs.write(str(url[1]) + '\n')
            for s in samples:
                if (s['short_url'] == url[0]):
                    newsSamples.append(s)
                    print "match", url[1]
                    break
    longNewsURLs.close()

    if (newsOnly == 1):
        samples = newsSamples

    # For each of the Bitly links from our collected tweets

    for sample in samples:
        # If the bitlyURL is found (it should always be)
        # This I/O stuff could be on a thread. At the most five threads.
        if sample['short_url'] in shortURLs:
            i = shortURLs.index(sample['short_url'])
            sample['long_url'] = longURLs[i]
            sample['bitly_global_hash'] = globalHashes[i]
            sample['bitly_user_hash'] = userHashes[i]
        else:
            print(str(sample) + ' could not be resolved.')

    print "Starting multi-threaded clickblock processing"
    pool = ThreadPool(5)
    sample = pool.map(sampleClicks, samples)
    pool.close()
    pool.join()
    print "Finished multi-threaded clickblock processing"
    for sample in samples:
        if sample['short_url'] in shortURLs:
            file.write(str(sample) + '\n')
        else:
            print(str(sample) + ' could not be resolved.')
    file.close()
    print (time.time() - start_time)
    return sample

def updateClicks(path):
        print "Starting update"
        updatedClicks = []
        dataDict = []
        with open(path, 'r') as f:
                data=f.read().split('\n')
        print "Lines in data: " , len(data)-1
        for line in data:
		if line!='':
                        dataDict.append(ast.literal_eval(line)) # dataDict = ast.literal_eval(line)
                        #dataDict = sampleClicks(dataDict)
                        #updatedClicks.append(dataDict)
        pool = ThreadPool(5)
        updatedClicks = pool.map(sampleClicks, dataDict)
        pool.close()
        pool.join()
        return updatedClicks

def sampleClicks(sample):
    # print "Getting clickblock, countries and refs."
    clickBlock = bitlyextractor.getURLClicks(sample['bitly_global_hash'], c)
    sample['countries'] = bitlyextractor.getLinkCountries(sample['short_url'], c)
    sample['refs'] = bitlyextractor.getRefs(sample['short_url'], c)
    if clickBlock != None:
        for e in clickBlock:
            sample['user_clicks'] = e.get('user_clicks')
            sample['global_clicks'] = e.get('global_clicks')

    return sample


def pickSamples(bitlyDicts, numToRead):
    # Samples bitly links (with name and ID)
    bitlySamples = []

    # Select numToRead tweets randomly
    if (numToRead < len(bitlyDicts)):
        bitlySamples = random.sample(bitlyDicts, numToRead)
    elif len(bitlyDicts) == 0:
        print('No bitlys to read!')
        return None;
    else:
        # print('We only have ' + str(len(bitlyDicts)) + ' to read!')
        bitlySamples = random.sample(bitlyDicts, len(bitlyDicts))
    return bitlySamples


def isUniqueNews(urlPattern, longURL):
    for PATTERN in PATTERNLIST:
        if (PATTERN == urlPattern.netloc):
            if (patternIsUnique(longURL)):
                return True
            else:
                return False
    return False


def pickUnique(bitlySamples):
    bitlysArray = []
    for e in bitlySamples:
        # Only unique bitly links should be added
        if e['short_url'] not in bitlysArray:
            bitlysArray.append(e['short_url'])
    return bitlysArray


def resolveBitlys(bitlysArray):
    # The bitly bundle contains 15 Bitly URLs! (Cannot send more to Bitly)
    results = []
    start = 0
    end = 15
    max = len(bitlysArray)
    response = []  # The resolved info from Bitly
    URLsAndHash = []
    bundles = []
    pool = ThreadPool(5)
    run = True

    # Build bundles of bitlys to resolve, max 15 at a time
    while run:
        # print('We have more than or equal to 15 bitlys!')
        if (max < end) and (start < max):
            end = max
            run = False
        elif (max < end) and (start == max):
            end = max
            break
        bundles.append(itemgetter(slice(start, end))(bitlysArray))
        start += 15
        end += 15

    URLsAndHash = pool.map(resolveBitlyBundle, bundles)
    pool.close()
    pool.join()
    print "The number of workers run for resolving bitlys were:", len(URLsAndHash)
    for e in URLsAndHash:
        results.extend(e)
    print "Number of bitlys resolved:", len(results)
    return results


def resolveBitlyBundle(bitlyBundle):
    resolvedBundle = []
    try:
        # This I/O stuff could be on a thread. At the most five threads.
        if(len(bitlyBundle) < 15):
            print("We are curently extracting %d links, this should be the last set of links" % (len(bitlyBundle)))
        response = bitlyextractor.expandShortUrl(bitlyBundle, c)  # TODO Error handling on the response
        for e in response:
            shortURL = checkShortURL(e)
            longURL = checkLongURL(e)
            globalHash = checkGlobalHash(e)
            userHash = checkUserHash(e)
            resolvedBundle.append((shortURL, longURL, globalHash, userHash))
    except Exception as ex:
        print('Problems with the response from Bitly')
        print ex
        return resolvedBundle
    return resolvedBundle


def checkUserHash(e):
    hash = ''
    try:
        hash = (e.get('user_hash'))
        return hash
    except AttributeError:
        return hash


def checkGlobalHash(e):
    hash = ''
    try:
        hash = (e.get('global_hash'))
        return hash
    except AttributeError:
        return hash


def checkLongURL(e):
    longURL = ''
    try:
        longURL = (e.get('long_url')).encode('utf-8')
        return longURL
    except AttributeError:
        return longURL


def checkShortURL(e):
    shortURL = ''
    try:
        shortURL = e.get('short_url')
        return shortURL
    except AttributeError:
        return shortURL


def patternIsUnique(s):
    with open('./data/links/UnknownArticlesToBeExtracted.txt') as f:
        for line in f:
            if (s + '\n' == line):
                f.close()
                return False
    f.close()
    return True


# This function is not currently used, but if we want some official news channels from Twitter, this is an incomplete list
def getNewsNames():
    newsSources = []
    newsSources.append('CNN')  # CNN
    newsSources.append('CNNMoney')  # CNNMoney
    newsSources.append('cnnbrk')
    newsSources.append('BBC')
    newsSources.append('BBCBreaking')
    newsSources.append('Reuters')
    newsSources.append('nytimes')
    newsSources.append('TIME')
    newsSources.append('washingtonpost')
    newsSources.append('WSJ')
    newsSources.append('FoxNews')
    newsSources.append('ABC')
    newsSources.append('NPR')
    newsSources.append('guardian')
    newsSources.append('CBSNews')
    newsSources.append('AFP')
    newsSources.append('cnni')
    newsSources.append('NBCNews')
    newsSources.append('latimes')
    newsSources.append('NewYorker')
    newsSources.append('HuffingtonPost')
    return newsSources;
