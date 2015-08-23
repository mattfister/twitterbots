import random
import os.path

class WordLists:
    def __init__(self):
        self.adjs = [line.rstrip('\n') for line in open(os.path.join('words', 'a.txt'))]
        self.nouns = [line.rstrip('\n') for line in open(os.path.join('words', 'n.txt'))]
        self.verbs = [line.rstrip('\n') for line in open(os.path.join('words', 'v.txt'))]
        self.livingThings = [line.rstrip('\n') for line in open(os.path.join('words', 'livingThings.txt'))]
        self.celebs = [line.rstrip('\n') for line in open(os.path.join('words', 'celebs.txt'))]
        self.places = [line.rstrip('\n') for line in open(os.path.join('words', 'places.txt'))]
        self.placeAdjs = [line.rstrip('\n') for line in open(os.path.join('words', 'placeAdjs.txt'))]
        self.ogdenBasicNouns = [line.rstrip('\n') for line in open(os.path.join('words', 'ogdenBasicNouns.txt'))]
        
    def getNoun(self):
        return random.choice(self.nouns).replace("_", " ")
    
    def getAdj(self):
        return random.choice(self.adjs)
    
    def getCeleb(self):
        return random.choice(self.celebs)

    def getLivingThing(self):
        return random.choice(self.livingThings)

    def getPlace(self):
        return random.choice(self.places)

    def getPlaceAdj(self):
        return random.choice(self.placeAdjs)

    def getOgdenBasicNoun(self):
        return random.choice(self.ogdenBasicNouns)

if __name__ == "__main__":
    w = WordLists()
    print w.getNoun()
    print w.getAdj()
    print w.getCeleb()
    print w.getLivingThing()
    print w.getPlace()
