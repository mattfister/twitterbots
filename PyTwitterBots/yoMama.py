#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generats yoMama jokes of the form - yo mama so adj she makes n1 look like n2

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

adjs = []
adjsRaw = open("insultAdjectives.txt").read()
adjLines = adjsRaw.split("\n")
for line in adjLines:
    a = line.split()
    adjs += (a[:1])


def aOrAn(word):
    if word[0] in 'aeiou':
        return 'an'
    else:
        return 'a'


def findTwoRelatedNouns():
    threshold = 0.8
    while 1:
        noun1 = random.choice(nouns)
        noun2 = random.choice(nouns)
        word1 = wn.synset(noun1 + ".n.01")
        word2 = wn.synset(noun2 + ".n.01")
        sim = word1.wup_similarity(word2)
        if noun1 != noun2 and sim > threshold:
            print noun1 + " " + noun2 + " " + str(sim)
            return [noun1, noun2]


def findVerbRelatedToNoun(noun):
    threshold = random.uniform(0.2, 0.5)
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
        adj = random.choice(adjs)

        part1 = 'Yo mama so ' + adj + ', '

        [noun1, noun2] = findTwoRelatedNouns()
        part2 = 'she makes ' + aOrAn(noun1) + ' ' + noun1 + ' look like ' + aOrAn(noun2) + ' ' + noun2 + '!'

        print part1 + part2
        # api.update_status(status=part1+part2)
        # time.sleep(60*2)
