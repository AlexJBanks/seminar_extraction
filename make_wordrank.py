import re
from collections import Counter
from os import listdir
from os.path import isfile, join

from nltk.corpus import reuters, brown
myPath = 'data/email/training/'
onlyFiles = [f for f in listdir(myPath+'untagged/') if isfile(join(myPath+'untagged/', f))]


def words(text): return re.findall(r"(?i)(?<=[\s\-\/'(])(\w*[a-z]{2,}\w*)(?=[.,'):\-\/\s])", text.lower())


def get_prob(frequencies):
    probability = {}
    total = sum(frequencies.values())
    for word in frequencies.most_common():
        probability[word[0]] = word[1] / total
    return probability


all_head = []
for email in onlyFiles:
    full_email = open(myPath + 'untagged/' + str(email)).read()
    if 'Topic:' in full_email:
        for word in words(open(myPath + 'untagged/' + str(email)).read().split('Topic:')[1].split(':')[0]):
            all_head.append(word)
head_freq = Counter(all_head)
head_prob = get_prob(head_freq)

comp_words = []
for word in reuters.words():
    comp_words.append(word.lower())
comp_freq = Counter(comp_words)
comp_prob = get_prob(comp_freq)

delta = {}
for word in head_prob:
    print(word)
    print(head_prob[word])
    if word in comp_prob:
        print(comp_prob[word])
        delta[word] = head_prob[word] - comp_prob[word]
    else:
        print()
        delta[word] = head_prob[word]

sorted_delta = sorted(delta, key=delta.get, reverse=True)
print(sorted_delta)

file_content = ""
for word in sorted_delta:
    file_content = file_content + word + '\n'

with open('data/ontology/normalised_word_popularity.txt', 'w') as head_file:
    head_file.write(file_content[:-1])

#