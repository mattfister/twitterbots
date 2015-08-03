#!/usr/bin/python
# spits out a stephon joke
# based on code from http://computationalhumor.tumblr.com
import sys, random, nltk, urllib, string
import rhymes
from nltk.corpus import wordnet as wn
from aOrAn import aOrAn
import pattern.en
import names
import wordLists

class Stefon:

    def __init__(self):
        self.names = names.Names()
        self.words = wordLists.WordLists()

    def getClubCeleb(self):
        celeb = self.words.getCeleb()
        choice = random.random()
        if choice < 0.7:
            pass
        elif choice < 0.9:
            celeb = "a " + celeb + " impersonator"
        elif choice < 1.0:
            relation = random.choice(["father", "mother", "sister", "brother", "twin", "uncle", "aunt", "grandfather", "grandmother"])
            celeb = celeb + "'s " + relation
        return celeb

    def maybe(self, value):
        if random.random() > 0.5:
            return value + " "
        else:
            return ""

    def acronymize(self, s):
        a = ""
        sep = random.choice([".", " "])
        for c in s:
            if not c==" ":
                a = a + c + sep
            else:
                a = a + c
        return a

    def newYorksHottestClubIs(self):
        choice = random.random()
        if choice < .5:
            clubName = self.words.getNoun()
        elif choice < 0.9:
            clubName = self.words.getAdj() + " " + self.words.getNoun()
        else:
            clubName = self.words.getAdj() + " " + self.words.getAdj() + " " + self.words.getNoun()
        if random.random() < 0.5:
            clubName = clubName.upper()
        else:
            clubName = clubName.title()

        if random.random() < 0.5:
            clubName = self.acronymize(clubName)
            return "New York's hottest club is " + clubName


    def clubThing(self):
        thing = ""
        choice = random.random()
        if choice < 0.3:
            thing = self.maybe(self.words.getAdj()) + self.words.getAdj() + " " + pattern.en.pluralize(self.words.getNoun())
        elif choice < 0.6:
            thing = pattern.en.pluralize(self.words.getNoun())
        elif choice < 0.7:
            collective = random.choice(["groups", "bunches", "packs", "a swimming pool full", "a pit of"]) 
            thing = collective + " of " + self.maybe(self.words.getLivingThingAdj()) + pattern.en.pluralize(self.words.getLivingThing())
        elif choice < 0.95:
            prep = random.choice(["with", "holding", "next to", "near", "thinking about", "getting", "wanting", "using", "feeling", "showing", "offering", "serving", "selling", "buying", "carrying"])
            thing = pattern.en.referenced(self.maybe(self.words.getLivingThingAdj()) + self.words.getLivingThing()) + " " + prep + " " +  pattern.en.referenced(self.maybe(self.words.getAdj()) + self.words.getOgdenBasicNoun())
        else:
            thing = self.getClubCeleb()
        return thing

    def theyveGotEverything(self):
        return  "They've got everything: " + self.clubThing() + ", "  + self.clubThing() + ", " + self.clubThing() + ", " + self.clubThing() + "..."


    def getFounder(self):
        choice = random.random()
        if choice < 0.9:
            return self.names.get(random.choice(["male", "female"]))
        else:
            return self.words.getCeleb()


    def clubDescription(self):
        description =  "Founded in " + str(random.randint(1800, 2015)) + " by " + self.getFounder() + ", this club "
        descriptionTransitive = random.choice(["is located in", "resembles", "was built in", "is decorated like", "looks like"])
        description += descriptionTransitive + " " +  pattern.en.referenced(self.maybe(self.words.getPlaceAdj()) + self.words.getPlace()) + "."
        return description


    def main(self):
        while True:
            print self.newYorksHottestClubIs()
            print self.clubDescription()
            print self.theyveGotEverything()
            print

if __name__ == "__main__":
    stefon = Stefon()
    stefon.main()
