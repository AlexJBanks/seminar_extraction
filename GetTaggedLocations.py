import re
from os import listdir
from os.path import isfile, join
import AccuracyCalculator


def get_loc(cur_email, path):
    full_email = open(path + '/' + str(cur_email)).read()
    content = re.compile(loc_regex).findall(full_email)
    detagged = []
    for loc in content:
        detagged.append(AccuracyCalculator.detag(loc).strip().replace(' \n', ' ').replace('\n', ''))
    return detagged


trainPath = 'data/email/training/pretagged'
trainFiles = [f for f in listdir(trainPath) if isfile(join(trainPath, f))]

loc_regex = AccuracyCalculator.get_tag_regex('location')

locations = set()
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
