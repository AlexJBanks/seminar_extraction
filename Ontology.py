from os import listdir
from os.path import isfile, join

myPath = 'data/email/training/'
onlyFiles = [f for f in listdir(myPath+'untagged/') if isfile(join(myPath+'untagged/', f))]


def rank_words(email):
    full_email = open(myPath + 'untagged/' + str(email)).read()
    pass


for email in onlyFiles:
    print(email)
    rank_words(email)
