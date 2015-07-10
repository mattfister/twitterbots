#!/usr/bin/python
#what do you call a...
#copied from http://computationalhumor.tumblr.com/
import sys, random, nltk, urllib, string
from nltk.corpus import wordnet as wn

def main():

    f = open('synHom.txt', 'w')
    
    keepGoing = 1
    
    while keepGoing == 1:
        
        rawHomoPh = open('homophones.html').read()
        homophonesList = map(lambda x: x.split()[1:],rawHomoPh.split("<p>")[1].split("<br>"))
        homophones = dict([(x[0],x[1:]) for x in homophonesList if len(x) > 1])
        #adjective list wordnet
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
        #generate nouns that have homophones that are adjectives,
        #or vice versa
        again = 1
        while again == 1:
            x = string.lower(random.choice(homophones.keys()))
            if x in adjs:
                adj2 = x
                for h in homophones[adj2]:
                    if h in nouns:
                        noun2 = h
                        try: 
                            nounS = wn.synset(noun2 + ".n.01").lemma_names()
                            noun1 = string.lower(random.choice(nounS))
                            adjS = wn.synset(adj2 + ".a.01").lemma_names()
                            adj1 = string.lower(random.choice(adjS))
                            again = 0
                        except nltk.corpus.reader.wordnet.WordNetError:
                            break
                        break
            elif x in nouns:
                noun2 = x
                for h in homophones[noun2]:
                    if h in adjs:
                        adj2 = h
                        try: 
                            nounS = wn.synset(noun2 + ".n.01").lemma_names()
                            noun1 = string.lower(random.choice(nounS))
                            adjS = wn.synset(adj2 + ".a.01").lemma_names()
                            adj1 = string.lower(random.choice(adjS))
                            again = 0
                        except nltk.corpus.reader.wordnet.WordNetError:
                            break
                        break
        
        #print to command line and file
        if noun2 != noun1 and adj2 != adj1:
            x = "What do you call a " + adj1 + " " + noun1 + "?\nA " + adj2 + " " + noun2 + "!\n"      
            print>>f, x
            print x
            
if __name__ == "__main__":
    main()
