import csv
import pickle
import json
import sys

files = ['part_00.csv', 'part_01.csv', 'part_02.csv', 'part_03.csv', 'part_04.csv', 'part_05.csv', 'part_06.csv',
         'part_07.csv']

num_parts = 50
dictionary_parts = []
for i in range(num_parts):
    dictionary_parts.append({})

def string_hash(concept):
    sum = 0
    for i in range(len(concept)):
        sum += i*ord(concept[i])

    return sum % num_parts

def get_part_dict(concept):
    return dictionary_parts[string_hash(concept)]

def chop_csvs():

    for part in files:
        print part
        with open('conceptnet/' + part) as csvfile:
            datareader = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)

            for row in datareader:

                # print row[0]
                triplet = row[0].split(',')
                # print triplet
                relation = triplet[0].split('/')[4]
                concept_array = triplet[1].split('/')
                # print concept_array
                concept = triplet[1].split('/')[3]
                concept_locale = triplet[1].split('/')[2]
                object = triplet[2].split('/')[3]
                object_locale = triplet[2].split('/')[2]
                
                if (concept_locale == 'en' and object_locale == 'en'):
                    #print 'new concept'
                    #print relation
                    #print concept
                    #print object
                
                    relation_dict = get_part_dict(concept) 

                    if concept not in relation_dict:
                        relation_dict[concept] = []


                    relation_dict[concept].append((relation, object))

    for i in range(len(dictionary_parts)):
        with open ('conceptnet_reduced_en_' + str(i) + '.json', 'w') as outfile:
            json.dump(dictionary_parts[i], outfile)


def get_concept_relations(concept):
    with open('conceptnet/conceptnet_reduced_en_' + str(string_hash(concept)) + '.json', 'r') as f:
        m = json.load(f)
        return m[concept]
    

if __name__ == '__main__':
    print get_concept_relations(sys.argv[1])
