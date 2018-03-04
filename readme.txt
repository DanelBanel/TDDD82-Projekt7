The current version of our program works as follows

******* Main ********
It is from this file the program runs from, from here you can chose for how long you want to collect tweets
and what you would like to do with them after collecting them.

******* tweets-runner ********
This file collects the tweets, with the help of some help files.

******* bitly-runner *********
//Reads file names from a file (which tweets-runner stores them in). 
The file names are the twitter files to process. For each such file,
this program runs a set of X (in this case 100 (not currently true)) randomly selected tweets
and as many news tweets (no random tweets at the moment, only news). The program asks bitly for long URL, clicks per
country and clicks per referrer. We also save identifiers (bitly user, bitly
link, and tweet ID) global clicks and clicks made by user.

******* helper files *********
bitlyextractor, bitlyfinder and bitlydatahandler are helper filers. 
A directory "data" is used for the data and a sub-directory "tweets" in "data" for the tweets.

Files that also exist in the project is:

htmlToText, extract the news article from an url

naiveBayesTrainer, trains a text classifier to classify text as fake or real

naiveBayesPipeline, classifies the text as fake or real.

*****How to run the program *****

To run the program you will need Python 2.7.9 or later of the 2.7.x branch and several extra packages, to get these packages you can 
use pip install individually for most of them or use pip with one of the requirements files plus additional work on Windows. 
The packages that you need to install are:

xlwt (which is used to save to excel, use pip to install)
beautifulsoup4 (use pip to install)

tweepy (twitter API. There is an error in the version available through pip as of 2017-04-20, use a manuall install of the 
latest version from Github untill a newer version comes to pip)

bitly_api (bitlys api, use pip to install)
For the naive bayes classifier you need several packages:
numpy (use pip to install, get version 1.11 or later. Speciall case for Windows, see below)
pandas (use pip to install. Requires numpy)
Scipy (Use pip to install if not on Windows, get version 0.19.0. Requires numpy)
scikit-learn (Use pip to install if not on Windows, get version 0.18.1. Requires numpy and Scipy)
****************************************
These two are a little bit tricky to install on Windows due to you need a special Windows version, you can find the packeges
on this page: http://www.lfd.uci.edu/~gohlke/pythonlibs/
You may also need to install numpy-1.11+mkl from the same page.
Make sure you have Microsoft Visual C++ 2008 redistributable package.
Make sure that you get a version that is compatible with: Your operating system, your version of Python and version of package as specified above.
Scipy (for example: scikit_learn‑0.18.1‑cp27‑cp27m‑win_amd64.whl for a computer running a 64-bit version of Windows on x86-64 and Python 2.7)
scikit-learn (for example: scipy‑0.19.0‑cp27‑cp27m‑win_amd64.whl)
*********************************************
