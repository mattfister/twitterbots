#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys
import json
import requests
import shutil
import random
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from PIL import Image
from PIL import ImageChops

keys = open('keys.txt', 'r')

# enter the corresponding information from your Twitter application:
CONSUMER_KEY = keys.readline().rstrip()
CONSUMER_SECRET = keys.readline().rstrip()
ACCESS_KEY = keys.readline().rstrip()
ACCESS_SECRET = keys.readline().rstrip()

keys.close()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

corpus = {}
file
adventureFile = open('adventureData/adventureData.txt')
for line in adventureFile:

adventureFile.close()


def postTweet(tweet):
    api.update_status(status=tweet)


class StdOutListener(StreamListener):
    def __init__(self, i):
        self.done = False;
        self.imgNum = i;

    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        tweet = json.loads(data)
        # print tweet.keys()
        if 'entities' in tweet:
            entities = tweet['entities']
            try:
                media = entities["media"]
                for medium in media:
                    if (medium["type"] == 'photo'):
                        print 'media_url=' + str(medium["media_url"])
                        response = requests.get(medium["media_url"], stream=True)
                        with open('img' + str(self.imgNum) + '.jpg', 'wb') as outFile:
                            shutil.copyfileobj(response.raw, outFile)
                        del response

                        self.done = True;
                        return False
            except Exception as e:
                print e,
                # if 'media' in entities:
                #    media = entities['media']
                #    print 'media='+str(media)
                #    if 'type' in media and media['type'] == 'photo' and 'media_url' in media:
                #        print 'media_url='+str(media['media_url'])

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    story = [['Today I went to the beach!', 'beach'],
             ['The water was warm and inviting.', 'ocean'],
             ['I got a bad sunburn though!', 'sun'],
             ['Then I saw a turtle... It was huge', 'turtle'],
             ['I went back home happy', 'beach']]

    for segment in story:
        status = segment[0]
        subject = segment[1]
        listener = StdOutListener(0)
        stream = Stream(auth, listener)
        print 'Streaming ' + subject
        stream.filter(track=[subject])
        time.sleep(10)
        try:
            api.update_with_media('img0.jpg', status)
            time.sleep(60 * 10)
        except Exception as e:
            print e
