import stefon
import tweepy
import time


class StefonBot:
    def __init__(self):
        keys = open('keys.txt', 'r')

        #enter the corresponding information from your Twitter application:
        CONSUMER_KEY = keys.readline().rstrip()
        CONSUMER_SECRET = keys.readline().rstrip()
        ACCESS_KEY = keys.readline().rstrip()
        ACCESS_SECRET = keys.readline().rstrip()

        keys.close()

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(auth)

        mentions = self.api.mentions_timeline(count=1)

        for mention in mentions:
            print mention.id
            print mention.text
            print mention.user.screen_name

        self.latestId = mention.id
        self.stefon = stefon.Stefon()

    def checkAndReply(self):
        mentions = self.api.mentions_timeline(count=1)
        newId = self.latestId
        newText = ""
        newUserScreenName = ""
        for mention in mentions:
            print mention
            newId = mention.id
            newText = mention.text
            newUserScreenName = mention.user.screen_name

        print newId
        print self.latestId
        if newId > self.latestId:
            self.latestId = newId
            self.api.update_status(status=".@" + newUserScreenName + " " + self.stefon.newYorksHottestClubIs())
            self.api.update_status(status=".@" + newUserScreenName + " " + self.stefon.clubDescription())
            self.api.update_status(status=".@" + newUserScreenName + " " + self.stefon.theyveGotEverything())
            time.sleep(300)
        
if __name__=='__main__':
    stefonBot = StefonBot()
    while True:
        stefonBot.checkAndReply()
        time.sleep(60)
