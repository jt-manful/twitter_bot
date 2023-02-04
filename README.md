# Twitter Bot
  A twitter bot that can reply and quote reply tweets

  built using Tweepy for python

# Description:
  This bot replies and/or quote replies the tweets of a target account containing specfic key words.

# Feature List:
1. replyTweet():
  This function replies a tweet with a given keyword in it with the last (not reply or RT) tweet from the user account 
  
2. qouteTweet():
    This function replies a tweet with a given keyword in it with the last (not reply or RT) tweet from the user account and quote the replied tweet using its url.
   
   
# Installation:
    pip install tweepy

# Usage:
 In keys.py input the secret access keys and consumer keys from your twittwer developer account
 
    CUSTOMER_KEY = ''
    CUSTOMER_SECRET = ''
    bearer_token = ''
    ACCESS_KEY = ''
    ACCESS_SECRET = ''
  
In twtiiter_not.py include the bot user name, user name of the target account to want to reply messages, the keywords the bot should look out for, and sleep time
    
    BOT_SCREEN_NAME = ''
    USER_SCREEN_NAME = ''
    KEYWORDS = [""]
    SLEEP_TIME = 0 # how often should the bot checking for tweets
