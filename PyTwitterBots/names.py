import random

class Names:
    def __init__(self):
        
        self.maleFirsts = [line.rstrip('\n').title() for line in open('maleFirstNames.txt')]
        self.femaleFirsts = [line.rstrip('\n').title() for line in open('femaleFirstNames.txt')]
        self.lasts = [line.rstrip('\n').title() for line in open('lastNames.txt')]
    
    def getFirst(self, gender):
        if gender == 'male':
            return random.choice(self.maleFirsts)
        else:
            return random.choice(self.femaleFirsts)
    
    def getLast(self):
        return random.choice(self.lasts)
        

    def get(self, gender):
        return self.getFirst(gender) + " " + self.getLast()

if __name__ == "__main__":
    n = Names()
    print n.get(random.choice(['male', 'female']))
