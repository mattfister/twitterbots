import generate_concept_sentence
from conceptnet import conceptnet_searcher
import random
from person import Person
from wordtools import wordLists
from wordtools import aOrAn

class Paragraph:


    def __init__(self, chars, setting):
        self.chars = chars
        self.setting = setting
        self.topic = ""
        self.words = wordLists.WordLists()
        self.props = []
        self.known_props = []

    
    def setting_sentence(self, chars, setting):
        sentence = ''
        for i in range(len(chars)):
            sentence += chars[i].full_name
            if i < len(chars) - 2:
                sentence += ', '
            elif i == len(chars) - 2:
                sentence += ', and ' 
            else:
                sentence += ' were in a ' + setting + '.'
        return sentence

    def discover_prop(self, char, prop, setting):
        self.props.remove(prop)
        self.known_props.append(prop)
        if char != None:
            return char + " " + random.choice(["discovered", "found", "noticed"]) + " " + aOrAn.aOrAn(prop) + " " + prop + " inside the " + setting + "."
        else:
            return "There was " + aOrAn.aOrAn(prop) + " " + prop + " inside the " + setting + "."

    def generate_sentences(self):
        self.props = [i[1].replace('_', ' ') for i in conceptnet_searcher.get_concept_relations(self.setting) if i[0] == 'HasA']

        for i in range(2):
            self.props.append(self.words.get_ogden_basic_noun())

        random.shuffle(self.props)
        self.props = self.props[:2]

        print self.props

        self.known_props = []

        print self.setting_sentence(self.chars, self.setting)

        for i in range(10):
            if random.random() < 0.5:
                print generate_concept_sentence.generate_concept_sentence(random.choice((random.choice(self.chars).first_name, None)), self.setting)
            else:
                if len(self.props) > 0:
                    print self.discover_prop(random.choice((random.choice(self.chars).first_name, None)), random.choice(self.props), self.setting)
                elif len(self.known_props) > 0:
                    try:
                        print generate_concept_sentence.generate_concept_sentence(random.choice((random.choice(self.chars).first_name, None)), random.choice(self.known_props))
                    except Exception:
                        continue
