#!/usr/bin/python
# what do you call a blank blank, a blah, blah, where the blahs rhyme
# based on code from http://computationalhumor.tumblr.com
import sys, random, nltk, urllib, string
import rhymes
from nltk.corpus import wordnet as wn
from aOrAn import aOrAn
import pattern.en

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
for line in nounLines:
    n = line.split()
    nouns += (n[:1])
#living things
livingThings = []
livingThingsRaw = open("livingThings.txt").read()
livingThingsLines = livingThingsRaw.split("\n")
for line in livingThingsLines:
    l = line.split()
    livingThings += (l[:1])
#living things
celebs = [line.rstrip('\n') for line in open('celebs.txt')]

def getNoun():
    return random.choice(nouns).replace("_", " ")

def getAdj():
    return random.choice(adjs)

def getLivingThing():
    return random.choice(livingThings).replace("_", " ")

def getCeleb():
    return random.choice(celebs)

def maybe(value):
    if random.random() > 0.5:
        return value + " "
    else:
        return ""

def acronymize(s):
    a = ""
    sep = random.choice(["/", "|", ".", " ", "-", "*"])
    for c in s:
        if not c==" ":
            a = a + c + sep
        else:
            a = a + c
    return a

def newYorksHottestClubIs():
    choice = random.random()
    if choice < .5:
        clubName = getNoun()
    elif choice < 0.9:
        clubName = getAdj() + " " + getNoun()
    else:
        clubName = getAdj() + " " + getAdj() + " " + getNoun()
    if random.random() < 0.5:
        clubName = clubName.upper()
    else:
        clubName = clubName.title()

    if random.random() < 0.5:
        clubName = acronymize(clubName)
    return "New York's hottest club is " + clubName


def clubThing():
    thing = ""
    choice = random.random()
    if choice < 0.3:
        thing = maybe(getAdj()) + getAdj() + " " + pattern.en.pluralize(getNoun())
    elif choice < 0.8:
        thing = pattern.en.pluralize(getNoun())
    elif choice < 0.95:
        prep = random.choice(["with", "by"])
        thing = pattern.en.referenced(maybe(getAdj()) + getLivingThing()) + " " + prep + " " +  pattern.en.referenced(maybe(getAdj()) + getNoun())
    else:
        thing = getCeleb()
    return thing

def theyveGotEverything():
    return  "They've got everything: " + clubThing() + ", "  + clubThing() + ", " + clubThing() + ", " + clubThing() + "..."

def main():
    while True:
        print newYorksHottestClubIs()
        print theyveGotEverything()

if __name__ == "__main__":
    main()
