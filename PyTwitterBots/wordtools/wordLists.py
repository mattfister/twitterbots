import random
import os.path


class WordLists:
    adjs = [line.rstrip('\n') for line in open(os.path.join('words', 'a.txt'))]
    nouns = [line.rstrip('\n') for line in open(os.path.join('words', 'n.txt'))]
    verbs = [line.rstrip('\n') for line in open(os.path.join('words', 'v.txt'))]
    living_things = [line.rstrip('\n') for line in open(os.path.join('words', 'livingThings.txt'))]
    celebs = [line.rstrip('\n') for line in open(os.path.join('words', 'celebs.txt'))]
    places = [line.rstrip('\n') for line in open(os.path.join('words', 'places.txt'))]
    place_adjs = [line.rstrip('\n') for line in open(os.path.join('words', 'placeAdjs.txt'))]
    ogdenBasicNouns = [line.rstrip('\n') for line in open(os.path.join('words', 'ogdenBasicNouns.txt'))]

    def __init__(self):
        pass

    def get_noun(self):
        return random.choice(WordLists.nouns).replace("_", " ")

    def get_adj(self):
        return random.choice(WordLists.adjs)

    def get_celeb(self):
        return random.choice(WordLists.celebs)

    def get_living_thing(self):
        return random.choice(WordLists.living_things)

    def get_place(self):
        return random.choice(WordLists.places)

    def get_place_adj(self):
        return random.choice(WordLists.place_adjs)

    def get_ogden_basic_noun(self):
        return random.choice(WordLists.ogdenBasicNouns)

    def get_living_thing_adj(self):
        return random.choice(WordLists.place_adjs)

if __name__ == "__main__":
    w = WordLists()
    print w.get_noun()
    print w.get_adj()
    print w.get_celeb()
    print w.get_living_thing()
    print w.get_place()
