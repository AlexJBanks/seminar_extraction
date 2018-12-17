from collections import Counter
from os import listdir
from os.path import isfile, join
from gensim.models import KeyedVectors
from makeWordrank import words

model = KeyedVectors.load_word2vec_format('C:/Users/alexb/lib/GoogleNews-vectors-negative300.bin', binary=True)

myPath = 'data/email/training/'
onlyFiles = [f for f in listdir(myPath + 'untagged/') if isfile(join(myPath + 'untagged/', f))]


departments = { 'Accounting':           'Business',
                'African':              'Culture',
                'Culture':              'COSS',
                'Anthropology':         'Culture',
                'Arts':                 'CAL',
                'Astronomy':            'Physics',
                'Physics':              'EPS',
                'Biology':              'LES',
                'Business':             '',
                'Law':                  'CAL',
                'Engineering':          'EPS',
                'Chemistry':            'EPS',
                'Civil':                'Engineering',
                'Classics':             'History',
                'History':              'COSS',
                'CAL':                  '',
                'EPS':                  '',
                'COSS':                 '',
                'MDS':                  '',
                'LES':                  '',
                'Archaeology':          'History',
                'Computer':             'EPS',
                'Dentistry':            'MDS',
                'Management':           'Business',
                'Social':               'COSS',
                'Development':          'Social',
                'Disability':           'Social',
                'Drama':                'Arts',
                'Geography':            'Environment',
                'Environment':          'LES',
                'European':             'Language',
                'Language':             'Arts',
                'Ecology':              'Environment',
                'Economics':            'Business',
                'Education':            'Social',
                'Electronics':          'Engineering',
                'English':              'Language',
                'Literature':           'Language',
                'Film':                 'Arts',
                'Writing':              'English',
                'Finance':              'Business',
                'Global':               'Environmental',
                'Government':           'Law',
                'Health':               'MDS',
                'Marketing':            'Business',
                'Mathematics':          'EPS',
                'Mechanics':            'Engineering',
                'Medieval':             'History',
                'Materials':            'EPS',
                'Music':                'Arts',
                'Philosophy':           'Social',
                'Theology':             'Social',
                'Religion':             'Religion',
                'Physiotherapy':        'LES',
                'Political':            'Social',
                'Psychology':           'Social',
                'Sociology':            'Social',
                'Criminology':          'Social',
                'Sport':                'LES'}

def get_max_depart(word):
    maximum = 0
    depart = ""
    for department in departments:
        cur = model.similarity(word, department)
        if cur > maximum:
            maximum = cur
            depart = department
    return depart

all_predictions = {}
for email in onlyFiles:
    full_email = open(myPath + 'untagged/' + str(email)).read()
    if 'Topic:' in full_email:
        likely_departs = []
        for word in words(full_email.split('Topic:')[1].split(':')[0]):
            if word in model:
                likely_departs.append(get_max_depart(word))
        if len(likely_departs) > 0:
            pred = Counter(likely_departs).most_common()[0][0]
            all_predictions.setdefault(pred, [])
            all_predictions[pred].append(email)

file_content = ""
for depart in departments.keys():
    file_content = file_content + depart + '\n'
    all_predictions.setdefault(depart, [])
    for email in all_predictions[depart]:
        file_content = file_content + " " + email + '\n'
    file_content = file_content + '\n'

with open('data/ontology/predictions.txt', 'w') as file:
    file.write(file_content[:-2])
