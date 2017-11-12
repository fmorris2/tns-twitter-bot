import urllib, json, tweepy
import backend.types.NewsStory as NewsStory
from time import sleep


class Bot:
    CYCLE_TIME = 60 * 30 #30 minutes between TNS consumptions
    INTERVAL_BETWEEN_STORY_TWEETS = 60 * 10 #10 minutes between news story tweets
    TNS_URL = 'http://tns.vikingsoftware.org:5000/news/Syracuse'
    KEY_FILE_PATH = '/data/keys'

    """
    An object that represents the TNS Twitter
    bot and all of its functionality

    Attributes:
        root_path: absolute path to this running program
        tweepy_api: the tweepy API object we'll use to access the TNS Twitter account
        keys: 4-tuple containing API keys for the TNS Twitter account
        already_tweeted_topics: cache representing topics that have already been tweeted
    """

    def __init__(self):
        from tns_twitter_bot import ROOT_PATH
        self.root_path = ROOT_PATH
        self.keys = self.load_api_keys(ROOT_PATH)
        self.tweepy_api = self.create_tweepy_api()
        self.already_tweeted_topics = []

    """
    The main cycle method for the bot.
    Tweets about the news stories, and
    then sleeps for the designated cycle
    time
    """
    def cycle(self):
        self.tweet_news_stories()
        sleep(Bot.CYCLE_TIME)

    """
    Consumes TNS web service, tweets about
    each news entry with a specified amount of
    time between each tweet.
    """
    def tweet_news_stories(self):
        news_stories = self.gather_news_stories()
        for story in news_stories:
            self.handle_tweet_process_for_story(story)

    """
    Takes in a NewsStory object as a parameter,
    and checks the already_tweeted_topics list
    to see if we've already tweeted about this story.
    If we haven't, then we're free to tweet about it.
    """
    def handle_tweet_process_for_story(self, story):
        if(story.trending_topic not in self.already_tweeted_topics):
            if self.tweet_story(story):
                sleep(Bot.INTERVAL_BETWEEN_STORY_TWEETS)

    """
    Consumes the TNS web service
    and returns a list of NewsStory
    objects
    """
    def gather_news_stories(self):
        json_entries = self.gather_json_from_tns()
        return self.parse_json_into_list(json_entries)

    """
    Given a json object as a parameter,
    we will then parse it into a list
    of NewsStory objects, and then return
    the list
    """
    def parse_json_into_list(self, json):
        news_story_list = []
        if 'newsEntries' in json:
            entries = json['newsEntries']
            for entry in entries:
                news_story_list.append(NewsStory.NewsStory(entry[0], entry[1], entry[3]))
        return news_story_list

    """
    Requests the TNS web service,
    and parses the web page into
    a JSON object
    """
    def gather_json_from_tns(self):
        data = []
        try:
            response = urllib.urlopen(Bot.TNS_URL)
            data = json.load(response)
        except IOError:
            print 'IO Error in gather_json'

        return data

    """
    Takes in a NewsStory object,
    and sends out a tweet for it
    """
    def tweet_story(self, story):
        try:
            print 'Tweeting story for topic: ' + story.trending_topic
            self.already_tweeted_topics.append(story.trending_topic)
            self.tweepy_api.update_status(
                'Trending Topic: ' + story.trending_topic + '\n' \
                + 'Tweet Volume: ' + ('N/A' if story.tweet_volume is None else str(story.tweet_volume)) + '\n' \
                + story.news_story_link
            )
        except tweepy.TweepError or UnicodeEncodeError:
            return False
        return True


    """
    Loads the API keys from disk (data/keys),
    and returns them as a 4-tuple
    """
    def load_api_keys(self, path):
        lines = open(path + Bot.KEY_FILE_PATH).read().splitlines()
        return lines[0], lines[1], lines[2], lines[3]

    """
    Creates the required tweepy API
    object to be used throughout the lifetime
    of this bot
    """
    def create_tweepy_api(self):
        auth = tweepy.OAuthHandler(self.keys[0], self.keys[1])
        auth.set_access_token(self.keys[2], self.keys[3])
        return tweepy.API(auth)
