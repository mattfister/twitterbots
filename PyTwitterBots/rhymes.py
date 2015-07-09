import nltk
import sys

def rhyme(inp):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     numSyllables = len(syllables[0][1])-1
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-numSyllables:] == syllable[-numSyllables:]]
     filteredRhymes = []
     for rhyme in rhymes:
          if len(nltk.corpus.wordnet.synsets(rhyme)) > 0 \
             and not rhyme in inp and not inp in rhyme:
               filteredRhymes += [rhyme]
     return set(filteredRhymes)


print rhyme(sys.argv[1])

