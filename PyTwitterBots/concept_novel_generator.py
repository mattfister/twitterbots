import random
import generate_concept_sentence
from wordtools import wordLists, names
from conceptnet import conceptnet_searcher

names = names.Names()
words = wordLists.WordLists()

def generate_character():
    choice = random.random()
    if choice < 0.9:
        return names.get(random.choice(["male", "female"]))
    else:
        return words.get_celeb()

def setting_sentence(characters, setting):
    sentence = ''
    for i in range(len(characters)):
        sentence += characters[i]
        if i < len(characters) - 2:
            sentence += ', '
        elif i == len(characters) - 2:
            sentence += ', and ' 
    sentence += ' were in a ' + setting + '.'
    return sentence

def generate_setting():
    while True:
        setting = words.get_place()
        try: 
            conceptnet_searcher.get_concept_relations(setting)
            return setting
        except Exception:
            continue

def generate_novel():
    characters = [generate_character(), generate_character(), generate_character()]
    setting = generate_setting()
    print setting_sentence(characters, setting)
    for i in range(10):
        print generate_concept_sentence.generate_concept_sentence(random.choice((random.choice(characters), None)), setting)


if __name__ == '__main__':
    generate_novel()
