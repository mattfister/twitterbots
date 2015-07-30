#!/usr/bin/python
# what do you call a blank blank, a blah, blah, where the blahs rhyme
# based on code from http://computationalhumor.tumblr.com
import sys, random, nltk, urllib, string
import rhymes
from nltk.corpus import wordnet as wn
from aOrAn import aOrAn
import pattern.en
import names
import wordLists

names = names.Names()
words = wordLists.WordLists()

def getClubCeleb():
    celeb = words.getCeleb()
    choice = random.random()
    if choice < 0.7:
        pass
    elif choice < 0.9:
        celeb = "a " + celeb + " impersonator"
    elif choice < 1.0:
        relation = random.choice(["father", "mother", "sister", "brother", "twin", "uncle", "aunt", "grandfather", "grandmother"])
        celeb = celeb + "'s " + relation
    return celeb

def maybe(value):
    if random.random() > 0.5:
        return value + " "
    else:
        return ""

def acronymize(s):
    a = ""
    sep = random.choice([".", " "])
    for c in s:
        if not c==" ":
            a = a + c + sep
        else:
            a = a + c
    return a

def newYorksHottestClubIs():
    choice = random.random()
    if choice < .5:
        clubName = words.getNoun()
    elif choice < 0.9:
        clubName = words.getAdj() + " " + words.getNoun()
    else:
        clubName = words.getAdj() + " " + words.getAdj() + " " + words.getNoun()
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
        thing = maybe(words.getAdj()) + words.getAdj() + " " + pattern.en.pluralize(words.getNoun())
    elif choice < 0.6:
        thing = pattern.en.pluralize(words.getNoun())
    elif choice < 0.7:
        collective = random.choice(["groups", "bunches", "packs", "a swimming pool full", "a pit of"]) 
        thing = collective + " of " + maybe(words.getAdj()) + pattern.en.pluralize(words.getLivingThing())
    elif choice < 0.95:
        prep = random.choice(["with", "holding", "next to", "near", "thinking about", "getting", "wanting", "using", "feeling", "showing", "offering", "serving", "selling", "buying", "carrying"])
        thing = pattern.en.referenced(maybe(words.getAdj()) + words.getLivingThing()) + " " + prep + " " +  pattern.en.referenced(maybe(words.getAdj()) + words.getOgdenBasicNoun())
    else:
        thing = getClubCeleb()
    return thing

def theyveGotEverything():
    return  "They've got everything: " + clubThing() + ", "  + clubThing() + ", " + clubThing() + ", " + clubThing() + "..."


def getFounder():
    choice = random.random()
    if choice < 0.9:
        return names.get(random.choice(["male", "female"]))
    else:
        return words.getCeleb()


def clubDescription():
    description =  "Founded in " + str(random.randint(1800, 2015)) + " by " + getFounder() + ", this club "
    descriptionTransitive = random.choice(["is located in", "resembles", "was built in", "is decorated like", "looks like"])
    description += descriptionTransitive + " " +  pattern.en.referenced(maybe(words.getPlaceAdj()) + words.getPlace()) + "."
    return description
    


def main():
    while True:
        print newYorksHottestClubIs()
        print clubDescription()
        print theyveGotEverything()
        print

if __name__ == "__main__":
    main()
