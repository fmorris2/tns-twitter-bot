# tns-twitter-bot
Consumes the Twitter news scraper (TNS) web service, and periodically posts trending news stories to a twitter account.

### Architecture
- Language: [Python](https://www.python.org/)
- Libraries:
    - [tweepy](http://tweepy.readthedocs.io/en/v3.5.0/getting_started.html)
    
### Overview
Meant to make use of the TNS web service that I made, tns-twitter-bot (ttb) will consume the web service and periodically tweet relevant trending news stories. TTB will function as a dynamic news source, always up to date with the subjects that people are talking about.

### Basic Logic Flow
- Bot runs on a cycle at a set interval (currently 2 hours, may be adjusted)
    1. Consumes TNS web service, grabs news stories for a set location and stores them until the end of the cycle
    2. Loops through news entries
        - If entry has already been tweeted about before, skip it
        - If entry is new news, tweet about it
            - Tweets a message with the url to the news story
            - Waits a specific amount of time (5 mins currently) before continuing in loop. This is to avoid spamming tweets all at once.
     
### Usage
Simply visit the Twitter page [here](https://twitter.com/thetnsbot).
