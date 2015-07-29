#!/usr/bin/python
# what do you call a blank blank, a blah, blah, where the blahs rhyme
# based on code from http://computationalhumor.tumblr.com
import tweepy, time, sys
import sys, random, nltk, urllib, string
import rhymes
from nltk.corpus import wordnet as wn
from aOrAn import aOrAn

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



def main():

    f = open('synHom.txt', 'w')
    #adjective list
    adjs = []
    adjRaw = open("a.txt").read()
    adjLines = adjRaw.split("\n")
    for line in adjLines:
        a = line.split()
        adjs += (a[:1])
    #noun list wordnet
    nouns = []
    nounRaw = open("n.txt").read()
    nounLines = nounRaw.split("\n")
    index = 0
    for line in nounLines:
        n = line.split()
        nouns += (n[:1])
    while index < len(adjs):
        print '.',
        x = string.lower(adjs[index])
        print x,
        index += 1
        adj2 = x
        #print adj2
        rhymeSet = rhymes.rhyme(adj2)
        print str(len(rhymeSet)) + ' rhymes'
        if rhymeSet:
            for h in rhymeSet:
                if h in nouns:
                    noun2 = h
                    try: 
                        nounS = wn.synset(noun2 + ".n.01").lemma_names()
                        for nounSyn in nounS:
                            noun1 = string.lower(nounSyn)
                            adjS = wn.synset(adj2 + ".a.01").lemma_names()
                            for adjSyn in adjS:
                                adj1 = string.lower(random.choice(adjS))
                                if noun2 != noun1 and adj2 != adj1:
                                    x = "What do you call " + aOrAn(adj1) + " " +  adj1.replace('_', ' ') + " " + noun1.replace('_', ' ') + "?\n" + aOrAn(adj2).title() + " " + adj2.replace('_', ' ') + " " + noun2.replace('_', ' ') + "!\n" 
                            
                                    print>>f, x
                                    print '\n'
                                    print x
                                    try:
                                        api.update_status(status=x)
                                    except Exception:
                                        continue
                                    time.sleep(60)
                    except nltk.corpus.reader.wordnet.WordNetError:
                        continue
        




if __name__ == "__main__":
    main()
