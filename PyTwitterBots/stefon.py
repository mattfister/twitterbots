#!/usr/bin/python
# generates python clubs
import random

import pattern.en
from wordtools import wordLists, names


class Stefon:
    def __init__(self):
        self.names = names.Names()
        self.words = wordLists.WordLists()

    def get_club_celeb(self):
        celeb = self.words.get_celeb()
        choice = random.random()
        if choice < 0.7:
            pass
        elif choice < 0.9:
            celeb = "a " + celeb + " impersonator"
        elif choice < 1.0:
            relation = random.choice(
                ["father", "mother", "sister", "brother", "twin", "uncle", "aunt", "grandfather", "grandmother"])
            celeb = celeb + "'s " + relation
        return celeb

    def maybe(self, value):
        if random.random() > 0.5:
            return value + " "
        else:
            return ""

    def acronymize(self, s):
        a = ""
        sep = random.choice([".", " "])
        for c in s:
            if not c == " ":
                a = a + c + sep
            else:
                a = a + c
        return a

    def new_yorks_hottest_club_is(self):
        choice = random.random()
        if choice < .5:
            club_name = self.words.get_noun()
        elif choice < 0.9:
            club_name = self.words.get_adj() + " " + self.words.get_noun()
        else:
            club_name = self.words.get_adj() + " " + self.words.get_adj() + " " + self.words.get_noun()
        if random.random() < 0.5:
            club_name = club_name.upper()
        else:
            club_name = club_name.title()

        if random.random() < 0.5:
            club_name = self.acronymize(club_name)
            return "New York's hottest club is " + club_name

    def club_thing(self):
        thing = ""
        choice = random.random()
        if choice < 0.3:
            thing = self.maybe(self.words.get_adj()) + self.words.get_adj() + " " + pattern.en.pluralize(
                self.words.get_noun())
        elif choice < 0.6:
            thing = pattern.en.pluralize(self.words.get_noun())
        elif choice < 0.7:
            collective = random.choice(["groups", "bunches", "packs", "a swimming pool full", "a pit of"])
            thing = collective + " of " + self.maybe(self.words.get_living_thing_adj()) + pattern.en.pluralize(
                self.words.get_living_thing())
        elif choice < 0.95:
            prep = random.choice(
                ["with", "holding", "next to", "near", "thinking about", "getting", "wanting", "using", "feeling",
                 "showing", "offering", "serving", "selling", "buying", "carrying"])
            thing = pattern.en.referenced(self.maybe(
                self.words.get_living_thing_adj()) + self.words.get_living_thing()) + " " \
                + prep + " " + pattern.en.referenced(
                self.maybe(self.words.get_adj()) + self.words.get_ogden_basic_noun())
        else:
            thing = self.get_club_celeb()
        return thing

    def theyve_got_everything(self):
        return "They've got everything: " + self.club_thing() + ", " + self.club_thing() + ", " + self.club_thing() + ", " + self.club_thing() + "..."

    def get_founder(self):
        choice = random.random()
        if choice < 0.9:
            return self.names.get(random.choice(["male", "female"]))
        else:
            return self.words.get_celeb()

    def club_description(self):
        description = "Founded in " + str(random.randint(1800, 2015)) + " by " + self.get_founder() + ", this club "
        description_transitive = random.choice(
            ["is located in", "resembles", "was built in", "is decorated like", "looks like"])
        description += description_transitive + " " + pattern.en.referenced(
            self.maybe(self.words.get_place_adj()) + self.words.get_place()) + "."
        return description

    def main(self):
        while True:
            print self.new_yorks_hottest_club_is()
            print self.club_description()
            print self.theyve_got_everything()
            print


if __name__ == "__main__":
    stefon = Stefon()
    stefon.main()
