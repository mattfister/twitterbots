#! /usr/bin/python
#How is a different than b?

import sys, random, nltk, urllib, string
from nltk.corpus import wordnet as wn

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


def findTwoRelatedNouns():
    while 1:
        noun1 = random.choice(nouns)
        noun2 = random.choice(nouns)
        word1 = wn.synset( noun1 + ".n.01")
        word2 = wn.synset( noun2 + ".n.01")
        if word1.path_similarity(word2) > 0.8:
            return [noun1, noun2]
        
def findVerbRelatedToNoun(noun):
    while 1:
        verb = random.choice(verbs)
        nounSynset = wn.synset( noun + ".n.01")
        verbSynset = wn.synset( verb + ".v.01")
        if nounSynset.path_similarity(verbSynset) > 0.4:
            return verb

def findVerbRelatedToOneNounButUnrelatedToAnother(noun1, noun2):
    while 1:
        verb = random.choice(verbs)
        verbSynset = wn.synset( verb + ".v.01")
        noun1Synset = wn.synset( noun1 + ".n.01")
        noun2Synset = wn.synset( noun2 + ".n.02")
        if noun1Synset.path_similarity(verbSynset) > 0.4 \
           && noun2Synset.path_similarity(verbSynset) < 0.05:
            return verb
            

def main():
    [word1, word2] = findTwoRelatedNouns()
    if (random.random() < 0.5):
        print 'How is a ' + word1 + ' different than a ' + word2 + "?"
        verb1 = findVerbRelatedToNoun(str(word1))
        verb2 = findVerbRelatedToNoun(str(word2))
        print 'A ' + word1 + ' ' + verb1 + ', but a ' + word2 + ' ' + verb2 + '!'
    else:
        print 'How is a ' + word1 + ' different than a ' + word2 + "?"
        verb = findVerbRelatedToOneNounButUnrelatedToAnother(noun1, noun2)

    
    
     
if __name__ == "__main__":
    main()
