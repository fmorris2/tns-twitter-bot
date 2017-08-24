class NewsStory:
    """
    Represents a news story parsed
    from TNS.

    Attributes:
        trending_topic: the tag for the trending topic on twitter
        tweet_volume: how many people were tweeting about this topic
        news_story_link: the URL to the news story
    """
    def __init__(self, topic, tweet_vol, link):
        self.trending_topic = topic.encode('utf-8')
        self.tweet_volume = tweet_vol
        self.news_story_link = link.encode('utf-8')