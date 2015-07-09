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

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = keys.readline().rstrip()
CONSUMER_SECRET = keys.readline().rstrip()
ACCESS_KEY = keys.readline().rstrip()
ACCESS_SECRET = keys.readline().rstrip()

keys.close()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

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
        #print tweet.keys()
        if 'entities' in tweet:
            entities = tweet['entities']
            try:
                media = entities["media"]
                for medium in media:
                    if(medium["type"] == 'photo'):
                        print 'media_url='+str(medium["media_url"])
                        response=requests.get(medium["media_url"], stream=True)
                        with open('img' + str(i) + '.jpg', 'wb') as outFile:
                            shutil.copyfileobj(response.raw, outFile)
                        del response
                       
                        
                        self.done = True;
                        return False
            except Exception as e:
                print '.',
            #if 'media' in entities:
            #    media = entities['media']
            #    print 'media='+str(media)
            #    if 'type' in media and media['type'] == 'photo' and 'media_url' in media:
            #        print 'media_url='+str(media['media_url'])
                

    def on_error(self, status):
        print(status)

    
if __name__ == '__main__':
    subjects = ['Oil', 'Watercolor', 'Modernism', 'Impressionism', 'Abstract', 'Realism', 'Surreal', 'Art']
    
    while(1):
        random.shuffle(subjects);
        for i in range(0, 2):
            subject = subjects[i]
            l = StdOutListener(i)
            stream = Stream(auth, l)
            print 'Streaming ' + subject
            stream.filter(track=[subject])
            time.sleep(10)
        try:
            img1 = Image.open('img0.jpg')
            img2 = Image.open('img1.jpg')
            img1 = img1.resize((1024, 512))
            img2 = img2.resize((1024, 512))
            if (random.random() < 0.1):
                img2 = img2.rotate(180)
            #out = ImageChops.blend(img1, img2, 0.5)
            out = ImageChops.blend(img1, img2, 0.5)
            out.save('out.jpg')
            
            api.update_with_media('out.jpg', "Voila my new painting is complete! I call it " + subjects[0] + "-" + subjects[1] +"!" + " #" + subjects[0] + " #" + subjects[1]);
            time.sleep(60*5);
        except Exception as e:
            print e


