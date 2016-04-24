import tweepy
from picamera import PiCamera
from time import sleep
from credentials import *

class Twitter(object):
   def __init__(self, test = True):
      if test:        
         auth = tweepy.OAuthHandler(TEST_TWITTER_CONSUMER_KEY, TEST_TWITTER_CONSUMER_SECRET)
         auth.set_access_token(TEST_TWITTER_ACCESS_TOKEN, TEST_TWITTER_ACCESS_SECRET)
         self.api = tweepy.API(auth)
      else:
         auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
         auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
         self.api = tweepy.API(auth)
   
   def tweet(self, status_string, lat_in, long_in, file_jpg):
      self.api.update_with_media(file_jpg, status_string, lat=lat_in, long=long_in)


if __name__ == '__main__':
   camera = PiCamera()

   camera.start_preview()
   camera.annotate_text = "testing"
   sleep(5)
   camera.capture('/home/pi/Projects/capture.jpg',use_video_port = True)
   camera.stop_preview()
#   twitter = Twitter(False)
   twitter = Twitter()
   twitter.tweet("test", 36.068880, -94.175885, "/home/pi/Projects/capture.jpg")
