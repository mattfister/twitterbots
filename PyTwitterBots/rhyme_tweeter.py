#!/usr/bin/python
# what do you call a blank blank, a blah, blah, where the blahs rhyme
# based on code from http://computationalhumor.tumblr.com
import time
import random
import string

import tweepy
import nltk
from nltk.corpus import wordnet as wn

import rhyme_humor

from wordtools.aOrAn import aOrAn


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


def main():
    while True:
        try:
            rhyme = rhyme_humor.random_rhyme()
            print rhyme
            api.update_status(status=rhyme)
        except Exception:
            continue
        time.sleep(60*60)

if __name__ == "__main__":
    main()
