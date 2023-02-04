import time
import keys
import tweepy

BOT_SCREEN_NAME = ''
USER_SCREEN_NAME = ''
TWEET_COUNT = 5 # number of tweets the bots sees at a time
BOT_TWEET_COUNT = 1 # number of recent tweets from the bot
KEYWORDS = [""]
seen = set()
FILENAME = ''
SLEEP_TIME = 0 # how ofter you want to check for new tweets



def api():
    """
        Authenticate the current user's Twitter account.
    """
    auth = tweepy.OAuthHandler(keys.CUSTOMER_KEY, keys.CUSTOMER_SECRET)
    try:
        auth.set_access_token(keys.ACCESS_KEY, keys.ACCESS_SECRET)
    except tweepy.errors.TweepyException:
        print('Error! Failed to get access token.')
    return tweepy.API(auth)


def retriveLastSeenTweet(filename):
    """
        Returns the last tweet that the bot has replied to.
    """
    file = open(filename, 'r')
    last_seen_id = int(file.read().strip())
    file.close()
    return last_seen_id


def storeLastSeenTweet(filename, tweet_id):
    """
        Updates the last tweet that the bot has replied to.
    """
    file = open(filename, 'w')
    file.write(str(tweet_id))
    file.close()
    return


def tweet(api: tweepy.API, message: str):
    """
        Updates the authenticating user's current status. Tweets message.
    """
    api.update_status(message)


def getTweet(api: tweepy.API, screen_name: str, count):
    """
        Returns the few tweets of user.
    """
    tweets = dict()
    user_tweets = api.user_timeline(screen_name=screen_name, count=count, include_rts=False)
    for user_tweet in user_tweets:
        if user_tweet.in_reply_to_status_id is None and user_tweet.author.id != bot_id:
            tweets[user_tweet.id] = user_tweet.text
    return tweets


def getBotTweet(api: tweepy.API, screen_name: str, count):
    """
        Returns a dictionary of the  last tweets from the bot account that is not a RT or reply.
    """
    tweets = dict()
    user_tweets = api.user_timeline(screen_name=screen_name, count=count, include_rts=False, exclude_replies=True)
    for user_tweet in user_tweets:
        tweets[user_tweet.id] = [user_tweet.text, user_tweets.url]
    return tweets


def searchKeyword(keywords, tweets):
    """
        Returns a dictionary of tweets with specific keywords identified.
    """
    key_tweets = dict()
    for value, tweet in tweets.items():
        id = value[0]
        for word in keywords:
            if word.lower() in tweet.lower():
                key_tweets[id] = tweet
                continue
    return key_tweets


def replyTweet(api: tweepy.API, screen_name: str, message: str, tweets):
    """
         Updates the authenticating user's current status with a reply to a Tweeted message.
    """
    last_seen_tweet_id = retriveLastSeenTweet(FILENAME)
    for value, tweet in tweets.items():
        id = value[0]
        if id == last_seen_tweet_id:
            print("skipping because ", id, " already seen")
            continue
        else:
            api.update_status('@' + screen_name + ' ' + message, in_reply_to_status_id=id,
                              auto_populate_reply_metadata=True)
            storeLastSeenTweet(FILENAME, id)


def quoteTweet(api: tweepy.API, screen_name: str, message: str, tweets):
    """
         Updates the authenticating user's current status with a reply to a Tweeted message.
    """
    last_seen_tweet_id = retriveLastSeenTweet(FILENAME)
    for value, tweet in tweets.items():
        id = value[0]
        url = value[1]
        if id == last_seen_tweet_id:
            print("skipping because ", id, " already seen")
            continue
        else:
            api.update_status('@' + screen_name + ' ' + message + '\n' + url, in_reply_to_status_id=id,
                              auto_populate_reply_metadata=True)
            storeLastSeenTweet(FILENAME, id)


if __name__ == '__main__':
    while True:
        api = api()
        bot_id = api.get_user(screen_name=BOT_SCREEN_NAME).id
        respond_to_tweets = searchKeyword(KEYWORDS, getTweet(api, USER_SCREEN_NAME, TWEET_COUNT))
        message_2 = getBotTweet(api, BOT_SCREEN_NAME, BOT_TWEET_COUNT)
        # for k, message in message_2.items():
           # quoteTweet(api, USER_SCREEN_NAME, message, respond_to_tweets)
        # for k, message in message_2.items():
           # replyTweet(api, USER_SCREEN_NAME, message, respond_to_tweets)
        time.sleep(SLEEP_TIME)
