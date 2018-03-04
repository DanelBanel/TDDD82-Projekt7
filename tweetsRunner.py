# ******** TWEETS-RUNNER *********'
# Main file of the project!
# Collects tweets in [runs] number of runs, as default set to 1 (meaning one run)
# Each run lasts for [timeout] seconds, as default set to 10 seconds
# Each run is saved in a file named with date and time.
# The file name is written to a file.

import bitlyFinder
import time
from time import strftime

def collectTweets(timeout):
    path = './data/'

   # timeout = 20
    print('We are starting to collect tweets')
##    runmeFile = open(path + 'runme.txt', 'w')

    # Tweets file named year-month-day_hour.txt
    time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
    path_and_filename = path + 'tweets/' + time_for_filename + '.txt'

    # Get Tweets from Twitter! (Last argument is seconds to collect data)
    bitlyFinder.collectTweets(path_and_filename, timeout)
##    runmeFile.write(path_and_filename + '\n')
##    runmeFile.close()
    return path_and_filename

