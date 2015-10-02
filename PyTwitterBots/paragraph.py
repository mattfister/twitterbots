import generate_concept_sentence
from conceptnet import conceptnet_searcher
import random
from person import Person
from wordtools import wordLists

class Paragraph:


    def __init__(self, chars, setting):
        self.chars = chars
        self.setting = setting
        self.topic = ""
        self.words = wordLists.WordLists()

    
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

    def generate_sentences(self):
        self.props = [i[1] for i in conceptnet_searcher.get_concept_relations(self.setting) if i[0] == 'HasA']
        
        for i in range(0, random.randint(0,2)):
            self.props.append(self.words.get_ogden_basic_noun())

        print self.props

        print self.setting_sentence(self.chars, self.setting)

        for i in range(10):
            if random.random() < 0.5:
                print generate_concept_sentence.generate_concept_sentence(random.choice((random.choice(self.chars).first_name, None)), self.setting)
            elif len(self.props) > 0:
                try:
                    print generate_concept_sentence.generate_concept_sentence(random.choice((random.choice(self.chars).first_name, None)), random.choice(self.props))
                except Exception:
                    continue
