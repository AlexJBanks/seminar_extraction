import re
from collections import Counter
from os import listdir
from os.path import isfile, join

import EntityTagging


def extract_tags(email):
    tagged_full = open(myPath + 'tagged/' + str(email)).read()
    pretagged_full = open(myPath + 'pretagged/' + str(email)).read()

    for tag in tag_names:
        tag_regex = get_tag_regex(tag)
        tagged_freq = get_tag_contents(tag_regex, tagged_full)
        pretagged_freq = get_tag_contents(tag_regex, pretagged_full)

        classified[tag] = classified[tag] + sum(tagged_freq.values())
        tp_in_corpus[tag] = tp_in_corpus[tag] + sum(pretagged_freq.values())

        temp = 0
        for content in pretagged_freq:
            temp = temp + min(tagged_freq[content], pretagged_freq[content])

        tp_classified[tag] = tp_classified[tag] + temp


def get_tag_contents(tag_regex, tagged_full):
    content = re.compile(tag_regex).findall(tagged_full)
    detagged = []
    for text in content:
        detagged.append(detag(text).strip())
    content_freq = Counter(detagged)
    return content_freq


def get_tag_regex(tag):
    return r'(?s)<' + tag + r'>(.*?)<\/' + tag + r'>'


def detag(content):
    all_tags = {r'<stime>', r'</stime>', r'<etime>', r'</etime>', r'<paragraph>', r'</paragraph>',
                r'<sentence>', r'</sentence>', r'<speaker>', r'</speaker>', r'<location>', r'</location>'}
    for tag in all_tags:
        content = content.replace(tag, '')
    return content


def calculate_f():
    classified["all"] = 0
    tp_in_corpus["all"] = 0
    tp_classified["all"] = 0
    for tag in tag_names:

        classified["all"] = classified["all"] + classified[tag]
        tp_in_corpus["all"] = tp_in_corpus["all"] + tp_in_corpus[tag]
        tp_classified["all"] = tp_classified["all"] + tp_classified[tag]
        print()

        if classified[tag] == 0 or tp_in_corpus[tag] == 0 or tp_classified[tag] == 0:
            print("no tags found, can't compute F1 for " + tag)
        else:
            print(tag)
            precision = tp_classified[tag] / classified[tag]
            recall = tp_classified[tag] / tp_in_corpus[tag]
            f1 = 2 * precision * recall / (precision + recall)

            print("Precision: " + str(precision))
            print("Recall:    " + str(recall))
            print("F1:        " + str(f1))

    print()
    print("Overall")
    precision = tp_classified["all"] / classified["all"]
    recall = tp_classified["all"] / tp_in_corpus["all"]
    f1 = 2 * precision * recall / (precision + recall)

    print("Precision: " + str(precision))
    print("Recall:    " + str(recall))
    print("F1:        " + str(f1))


tag_names = {'stime', 'etime', 'paragraph', 'sentence', 'speaker', 'location'}

classified = {}
tp_in_corpus = {}
tp_classified = {}
for tag in tag_names:
    classified[tag] = 0
    tp_in_corpus[tag] = 0
    tp_classified[tag] = 0

myPath = 'data/email/test/'
onlyFiles = [f for f in listdir(myPath + 'untagged/') if isfile(join(myPath + 'untagged/', f))]
for email in onlyFiles:
    extract_tags(email)

print(classified)
print(tp_in_corpus)
print(tp_classified)

calculate_f()
