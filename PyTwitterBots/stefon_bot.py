#! /usr/bin/env python
# stefon_bot.py

""" This is a twitter bot that replies to @mentions with a series of tweets describing the hottest club in New York.

REQUIREMENTS:
keys.txt
An adjacent file named keys.txt that requires the following twitter API keys each on there own line in this
format:

consumer_key
consumer_secret
access_key
access_secret

"""

import stefon
import tweepy
from tweepy import TweepError
import time


class StefonBot:
    def __init__(self):
        keys = open('keys.txt', 'r')

        # enter the corresponding information from your Twitter application:
        consumer_key = keys.readline().rstrip()
        consumer_secret = keys.readline().rstrip()
        access_key = keys.readline().rstrip()
        access_secret = keys.readline().rstrip()

        keys.close()

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

        mentions = self.api.mentions_timeline(count=1)

        for mention in mentions:
            print mention.id
            print mention.text
            print mention.user.screen_name

        self.latestId = mention.id
        self.stefon = stefon.Stefon()

    def check_and_reply(self):
        mentions = self.api.mentions_timeline(count=1)
        new_id = self.latestId
        new_text = ""
        new_user_screen_name = ""
        for mention in mentions:
            print mention
            new_id = mention.id
            new_text = mention.text
            new_user_screen_name = mention.user.screen_name

        print new_id
        print self.latestId
        if new_id > self.latestId:
            self.latestId = new_id
            try:
                self.api.update_status(status=".@" + new_user_screen_name + " " + self.stefon.new_yorks_hottest_club_is())
            except TweepError:
                pass
            try:
                self.api.update_status(status=".@" + new_user_screen_name + " " + self.stefon.club_description())
            except TweepError:
                pass
            try:
                self.api.update_status(status=".@" + new_user_screen_name + " " + self.stefon.theyve_got_everything())
            except TweepError:
                pass
            time.sleep(300)


if __name__ == '__main__':
    stefon_bot = StefonBot()
    while True:
        stefon_bot.check_and_reply()
        time.sleep(60)
