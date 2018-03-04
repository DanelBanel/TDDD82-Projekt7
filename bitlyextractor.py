# -*- coding: cp1252 -*-
# Communicates with bitly.com to expand short URL's
# Send request to bitly API and write response to file.
# shortUrls is an array of up to 15 short URL's (bitly.com API max limit)
def expandShortUrl(shortUrls, c):
    # File to write to
    path = './data/'

    response = None
    try:
        o = open(path + 'expanded.txt', 'a+')
        response = c.expand(shortUrl=shortUrls)
        # print("Länkar extraherad")
        o.write((str(response).encode('utf-8')) + '\n')
        o.close()
    except:
        pass
    return response;


def getRefs(link, c):
    refs = None
    try:
        refs = c.link_referrers_by_domain(link)
    # print("refs-länk hittad")
    except:
        print('Unable to retrieve refs')
    return refs;


def getLinkCountries(link, c):
    countries = None
    try:
        countries = c.link_countries(link)
    # print("land hittat")
    except:
        print('Unable to retrieve countries')
    return countries;


def getURLClicks(globalHash, c):
    URLclicks = None
    try:
        URLclicks = c.clicks(globalHash)
    # print("Vi har hittat hur många gånger länken klickats")
    except:
        print('Unable to retrieve clicks')
    return URLclicks;

# Dummy main function, just for testing a bitly URL	
# if __name__ == '__main__':
#	shortUrls = []
#	shortUrls.append('http://bit.ly/28Zo8vQ')
#	expandShortUrl(shortUrls)
#	getURLClicks('28ZYUgL')
#	getLinkCountries('http://bit.ly/28Zo8vQ')
#	getRefs('http://bit.ly/28Zo8vQ')
