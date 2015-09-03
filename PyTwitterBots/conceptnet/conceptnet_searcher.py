import csv
import pickle
import sPickle

files = ['part_00.csv', 'part_01.csv', 'part_02.csv', 'part_03.csv', 'part_04.csv', 'part_05.csv', 'part_06.csv',
         'part_07.csv']

relation_dict = {}


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

                if concept not in relation_dict:
                    relation_dict[concept] = []

                relation_dict[concept].append((relation, object))

sPickle.s_dump(relation_dict, open('conceptnet_reduced_en_5_4.p', 'wb'))