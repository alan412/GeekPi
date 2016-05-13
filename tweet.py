import tweepy
from time import sleep
from credentials import *

class Twitter(object):
   def __init__(self):
      self.test = True     
      if(not self.test):
         auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
         auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
         self.api = tweepy.API(auth)
   
   def tweet(self, status_string, lat_in, long_in, file_jpg): 
      if(self.test):
         with open("tweets.txt", "a") as testFile:
            testFile.write("Would have been %s file with %s status and %.02f %.02f \n" % (file_jpg, status_string, lat_in, long_in))
      else:  
         self.api.update_with_media(file_jpg, status_string, lat=lat_in, long=long_in)

if __name__ == '__main__':
   twitter = Twitter()
   twitter.tweet("test", 36.068880, -94.175885, "/home/pi/Projects/capture.jpg")
