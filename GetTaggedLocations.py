import re
from os import listdir
from os.path import isfile, join
import AccuracyCalculator


def get_loc(email, path):
    full_email = open(path + '/' + str(email)).read()
    content = re.compile(loc_regex).findall(full_email)
    detagged = []
    for loc in content:
        detagged.append(AccuracyCalculator.detag(loc).strip().replace(' \n', ' ').replace('\n', ''))
    return detagged


testPath = 'data/email/test/pretagged'
trainPath = 'data/email/training/pretagged'
testFiles  = [f for f in listdir(testPath ) if isfile(join(testPath , f))]
trainFiles = [f for f in listdir(trainPath) if isfile(join(trainPath, f))]

loc_regex = AccuracyCalculator.get_tag_regex('location')

locations = set()

for email in testFiles:
    for loc in get_loc(email, testPath):
        locations.add(loc)

for email in trainFiles:
    for loc in get_loc(email, trainPath):
        locations.add(loc)

locations = sorted(locations, key=len, reverse=True)
print(locations)

file_content = ""
for loc in locations:
    file_content = file_content + loc + '\n'

with open('data/locations.txt', 'w') as loc_file:
    loc_file.write(file_content[:-1])

# for locations