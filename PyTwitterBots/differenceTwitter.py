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
import nltk
from nltk.corpus import wordnet as wn
from pattern.en import conjugate, SINGULAR
from nltk import word_tokenize, Text, pos_tag

nouns = []
nounRaw = open("n.txt").read()
nounLines = nounRaw.split("\n")
for line in nounLines:
    n = line.split()
    nouns += (n[:1])

verbs = []
verbRaw = open("v.txt").read()
verbLines = verbRaw.split("\n")
for line in verbLines:
    v = line.split()
    verbs += (v[:1])


def aOrAn(word):
    if word[0] in 'aeiou':
        return 'an'
    else:
        return 'a'


def findTwoRelatedNouns():
    while 1:
        threshold = 0.9
        noun1 = random.choice(nouns)
        noun2 = random.choice(nouns)
        word1 = wn.synset(noun1 + ".n.01")
        word2 = wn.synset(noun2 + ".n.01")
        threshold -= 0.001
        if noun1 != noun2 and word1.path_similarity(word2) > threshold:
            return [noun1, noun2]


def findVerbRelatedToNoun(noun):
    threshold = 0.5
    while 1:
        verb = random.choice(verbs)
        nounSynset = wn.synset(noun + ".n.01")
        verbSynset = wn.synset(verb + ".v.01")
        threshold -= 0.01

        if (nounSynset.path_similarity(verbSynset) > threshold or verbSynset.path_similarity(nounSynset) > threshold):
            return verb


def findVerbRelatedToOneNoun(noun1, noun2):
    threshold = 0.5
    while 1:
        verb = random.choice(verbs)
        noun1Synset = wn.synset(noun1 + ".n.01")
        noun2Synset = wn.synset(noun2 + ".n.01")
        verbSynset = wn.synset(verb + ".v.01")

        sim1 = verbSynset.path_similarity(noun1Synset)
        sim2 = verbSynset.path_similarity(noun2Synset)

        threshold -= 0.01
        print verb + " " + noun1 + " " + noun2 + " " + str(threshold) + " " + str(sim1) + " " + str(sim2)
        if (sim1 > threshold and sim2 < threshold):
            return verb


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

if __name__ == '__main__':
    while 1:
        [word1, word2] = findTwoRelatedNouns()
        question = 'How is ' + aOrAn(word1) + " " + word1 + ' different than ' + aOrAn(word2) + " " + word2 + "?"
        if True:
            verb1 = findVerbRelatedToNoun(str(word1))
            verb2 = findVerbRelatedToNoun(str(word2))
            verb1 = conjugate(verb1, number=SINGULAR)
            verb2 = conjugate(verb2, number=SINGULAR)
            answer = aOrAn(word1).capitalize() + " " + word1 + ' ' + verb1 + ', but ' + aOrAn(
                word2) + " " + word2 + ' ' + verb2 + '!'
        else:  # This doesn't work
            verb = findVerbRelatedToOneNoun(word1, word2)
            answer = "You can " + verb + " " + aOrAn(word1) + " " + word1 + " but you can't " + verb + " " + aOrAn(
                word2) + " " + word2 + "!"
        print question + "\n" + answer
        api.update_status(status=question + "\n" + answer)
        time.sleep(60 * 2)
