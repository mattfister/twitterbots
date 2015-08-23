#!/usr/bin/python
# what do you call a blank blank, a blah, blah, where the blahs rhyme
# based on code from http://computationalhumor.tumblr.com
import random
import string

import nltk
from nltk.corpus import wordnet as wn

import rhymes
from wordtools.aOrAn import aOrAn


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
                    except nltk.corpus.reader.wordnet.WordNetError:
                        continue
        
            
if __name__ == "__main__":
    main()
