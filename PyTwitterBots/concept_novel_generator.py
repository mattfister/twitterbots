import random
from wordtools import wordLists, names
from paragraph import Paragraph
from person import Person
from conceptnet import conceptnet_searcher

import sys


names = names.Names()
words = wordLists.WordLists()
scene_settings = []

def generate_character():
    choice = random.random()
    if choice < 0.9:
        return names.get(random.choice(["male", "female"]))
    else:
        return words.get_celeb()

def generate_setting():
    while True:
        setting = words.get_fantasy_place()
        try:
            print setting
            conceptnet_searcher.get_concept_relations(setting)
            return setting
        except Exception:
            print sys.exc_info()[0]
            continue

def generate_novel():
    characters = [Person(), Person(), Person()]
    for i in range(5):
        scene_settings.append(generate_setting())
    for setting in scene_settings:
        paragraph = Paragraph(characters, setting)
        paragraph.generate_sentences()
        print paragraph

if __name__ == '__main__':
    generate_novel()
