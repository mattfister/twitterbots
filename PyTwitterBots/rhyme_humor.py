#!/usr/bin/python
# what do you call a blank blank, a blah, blah, where the blahs rhyme
# based on code from http://computationalhumor.tumblr.com
import random
import string

import nltk
from nltk.corpus import wordnet as wn

import rhymes
from wordtools.aOrAn import aOrAn
from wordtools import wordLists


def random_rhyme():
    while True:
        adj2 = string.lower(wordLists.WordLists().get_adj())
        adj2_rhymes = rhymes.rhyme(adj2)
        if adj2_rhymes:
            for adj2_rhyme in adj2_rhymes:
                if adj2_rhyme in wordLists.WordLists.nouns:
                    noun2 = adj2_rhyme
                    try:
                        noun2_synset = wn.synset(noun2 + ".n.01").lemma_names()
                        for noun_syn in noun2_synset:
                            noun1 = string.lower(noun_syn)
                            adj2_synset = wn.synset(adj2 + ".a.02").lemma_names()
                            for adj2_syn in adj2_synset:
                                adj1 = string.lower(random.choice(adj2_synset))
                                if noun2 != noun1 and adj2 != adj1:
                                    x = "What do you call " + aOrAn(adj1) + " " + adj1.replace('_',' ') + " " + noun1.replace('_', ' ') + "?\n" + aOrAn(adj2).title() + " " + adj2.replace('_',' ') + " " + noun2.replace('_', ' ') + "!\n"
                                    return x
                    except nltk.corpus.reader.wordnet.WordNetError:
                        continue

def main():
    while True:
        print random_rhyme()


if __name__ == "__main__":
    main()
