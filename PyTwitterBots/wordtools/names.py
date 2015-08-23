import random
import os.path


class Names:
    maleFirsts = [line.rstrip('\n').title() for line in open(os.path.join('words', 'maleFirstNames.txt'))]
    femaleFirsts = [line.rstrip('\n').title() for line in open(os.path.join('words', 'femaleFirstNames.txt'))]
    lasts = [line.rstrip('\n').title() for line in open(os.path.join('words', 'lastNames.txt'))]

    def __init__(self):
        pass

    def get_first(self, gender):
        if gender == 'male':
            return random.choice(Names.maleFirsts)
        else:
            return random.choice(Names.femaleFirsts)

    def getLast(self):
        return random.choice(Names.lasts)

    def get(self, gender):
        return self.get_first(gender) + " " + self.getLast()


if __name__ == "__main__":
    n = Names()
    print n.get(random.choice(['male', 'female']))
