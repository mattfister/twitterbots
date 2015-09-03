import sys
from conceptnet import conceptnet_searcher
import random
from wordtools import aOrAn
import language_check

tool = language_check.LanguageTool('en-US')

all_relations = ('RelatedTo', 'IsA', 'PartOf', 'MemberOf', 'HasA', 'UsedFor', 'CapableOf', 'AtLocation', 'Causes', 'HasSubevent', 'HasFirstSubevent', 'HasLastSubevent', 'HasPrerequisite', 'HasProperty', 'MotivatedByGoal', 'ObstructedBy', 'Desires', 'CreatedBy', 'Synonym', 'Antonym', 'DerivedFrom', 'TranslationOf', 'DefinedAs')

#relations = ('RelatedTo', 'IsA', 'PartOf', 'HasA')
relations = ['HasA']

def correct_sentence(sentence):
    matches = tool.check(sentence)
    return language_check.correct(sentence, matches)


def related_to_sentence(person, concept, subject):
    sentence = person + ' thought about how a ' + concept + ' is like ' + aOrAn.aOrAn(subject) + " " + subject + '.'
    return sentence

def is_a_sentence(person, concept, subject):
    relation_verb = random.choice(('is', 'can be'))
    sentence =  person + ' considered how a ' + concept + ' ' + relation_verb + ' '  + aOrAn.aOrAn(subject) + " " + subject + '.'
    return sentence

def part_of_sentence(person, concept, subject):
    sentence =  person + ' noticed the ' + concept + ' was part of ' +  aOrAn.aOrAn(subject) + ' ' + subject + '.'
    return sentence 

def has_a_sentence(person, concept, subject):
    sentence = person + ' noticed the ' + concept + ' had ' + aOrAn.aOrAn(subject) + ' ' + subject + '.'
    return sentence

def generate_concept_sentence(person, concept, relation):
    pass




def prep_part(part):
    return part.replace('_', ' ')
    

def generate_concept_sentence(person, concept):
    concept_relations = conceptnet_searcher.get_concept_relations(concept)
    relation = ""
    while not relation in relations:
        concept_relation = random.choice(concept_relations)
        relation = concept_relation[0]
        subject = concept_relation[1]
    print (concept, relation, subject)
    concept_part = prep_part(concept)
    subject_part = prep_part(subject)
    if relation == 'RelatedTo':
        print related_to_sentence(person, concept_part, subject_part)
    elif relation == 'IsA':
        print is_a_sentence(person, concept_part, subject_part)
    elif relation == 'PartOf':
        print part_of_sentence(person, concept_part, subject_part)
    elif relation == 'HasA':
        print has_a_sentence(person, concept_part, subject_part)



if __name__ == '__main__':
    generate_concept_sentence('Justin', sys.argv[1])

