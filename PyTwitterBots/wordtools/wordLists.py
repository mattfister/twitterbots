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
    living_thing_adjs = [line.rstrip('\n') for line in open(os.path.join('words', 'livingThingAdjs.txt'))]
    fantasy_places = [line.rstrip('\n') for line in open(os.path.join('words', 'fantasyPlaces.txt'))]
    fantasy_props = [line.rstrip('\n') for line in open(os.path.join('words', 'fantasyProps.txt'))]

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

    def get_fantasy_place(self):
        return random.choice(WordLists.fantasy_places)

    def get_ogden_basic_noun(self):
        return random.choice(WordLists.ogdenBasicNouns)

    def get_living_thing_adj(self):
        return random.choice(WordLists.living_thing_adjs)

    def get_fantasy_prop(self):
        return random.choice(WordLists.fantasy_props)

if __name__ == "__main__":
    w = WordLists()
    print w.get_noun()
    print w.get_adj()
    print w.get_celeb()
    print w.get_living_thing()
    print w.get_place()
