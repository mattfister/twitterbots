import csv


files =['part_00.csv', 'part_01.csv', 'part_02.csv', 'part_03.csv', 'part_04.csv', 'part_05.csv', 'part_06.csv', 'part_07.csv']

for part in files:
    with open('conceptnet/' + part) as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE)
        for row in datareader:
            pass
