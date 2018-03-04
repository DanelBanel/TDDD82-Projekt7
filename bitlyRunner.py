# Run the Bitly-extractor on the links in the tweets we collected
# We will start when we have one completed twitter file
import time
import bitlydatahandler
#from multiprocessing import Lock


def run(tweetsPath):
    #lock.acquire()
    path = './data/'

    runs = 0
##    lines = []
##    haveread = []


    #We will run the program until we have done a specified number of runs
    while (runs < 1):
        print('We are running! Lap ' + str(runs))
        # Open the file
##        runFile = open(path + 'runme.txt', 'r').read().split('\n')
##
##        # Read paths to files to get bitlys from later
##        for line in runFile:
##            try:
##                lines.append(line)
##            except:
##                continue

##        for line in lines:
##            if ((line not in haveread) and (line != '')):
        # Read me
        time_for_filename = time.strftime("%Y-%m-%d_%H%M%S")
        # Create a file for the news sites
        news_file_path = path + time_for_filename + '_news.txt'
        # Create a file for the randomly selected Bitly links
        random_file_path = path + time_for_filename + '_random.txt'
        # Random tweets
        #bitlydatahandler.handleTweets(tweetsPath=tweetsPath, numToRead=100, outfile=random_file_path, newsOnly=0)
        # News tweets (could do with 3000?)
        bitlydatahandler.handleTweets(tweetsPath=tweetsPath, numToRead=1000, outfile=news_file_path, newsOnly=1)
##        haveread.append(line)
        runs += 1
    #print("DONE")
    return news_file_path
    #lock.release()
