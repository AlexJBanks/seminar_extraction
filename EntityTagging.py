import re
from os import listdir
from os.path import isfile, join

import nltk


def tag_times(full_email):

    stime = None
    etime = None
    if "Time:" in full_email:
        headtimes = get_times(full_email.split("Time:")[1].split("\n")[0])
        if len(headtimes) > 0:
            stime = min(headtimes)
            if len(headtimes) > 1:
                etime = max(headtimes)

    if etime is None and "Abstract:" in full_email:
        bodytimes = get_times(full_email.split("Abstract:")[1])
        if stime is None and len(bodytimes) > 0:
            stime = min(bodytimes)
        if len(bodytimes) > 0 and max(bodytimes) != stime:
            etime = max(bodytimes)

    if stime is None:
        return full_email

    alltimes = get_times(full_email)

    for time in alltimes[stime]:
        full_email = tag_element(full_email, time, "stime")
    if etime is not None:
        for time in alltimes[etime]:
            full_email = tag_element(full_email, time, "etime")

    return full_email


def get_times(text):

    time_exp = r"(?i)(?P<hrs>\d{1,2})(?::(?P<min0>\d{2}) ?(?P<ap0>[ap]).?m|:(?P<min1>\d{2})| ?(?P<ap1>[ap]).?m)"
    time_iter = re.compile(time_exp).finditer(text)

    times = {}
    for time_obj in enumerate(time_iter):

        valid = True
        time = int(time_obj[1].group('hrs')) * 100

        if (time_obj[1].group('ap0') is not None and time_obj[1].group('ap0').lower() == 'p') \
                or (time_obj[1].group('ap1') is not None and time_obj[1].group('ap1').lower() == 'p'):
            time = time + 1200

        if time > 2400:
            valid = False

        mins = 0
        if time_obj[1].group('min0') is not None:
            mins = int(time_obj[1].group('min0'))
        if time_obj[1].group('min1') is not None:
            mins = int(time_obj[1].group('min1'))

        if mins > 59 or mins < 0:
            valid = False
        time = time + mins

        if valid:
            times.setdefault(time, set())
            times[time].add(time_obj[1][0])

    return times


def tag_para_sent(full_email):
    para_exp = r"(?m)^\s+?([A-Z0-9].+?(?:\n.+?)*?[.!?])\s+?$"
    list_of_sents = []
    if "Abstract:" in full_email:
        for sent in nltk.sent_tokenize(full_email.split("Abstract:")[1]):
            list_of_sents.append(sent)

        for paragraph in re.compile(para_exp).findall(full_email.split("Abstract:")[1]):
            full_email = tag_element(full_email, paragraph, "paragraph")

        for sent in list_of_sents:
            full_email = tag_element(full_email, sent.strip()[:-1], "sentence")

    return full_email


def tag_loc(full_email):
    raw_loc = open('data/locations.txt').read()
    all_loc = raw_loc.split('\n')
    if 'Place:' in full_email:
        loc = full_email.split('Place:')[1].split('\n')[0].strip()
        full_email = tag_element(full_email, loc, 'location')
        return full_email

    for loc in all_loc:
        if loc in full_email:
            full_email = tag_element(full_email, loc, 'location')
            return full_email

    return full_email


def tag_speak(full_email):
    speak = None
    if 'Who:' in full_email:
        speak = full_email.split('Who:')[1].split('\n')[0].split(',')[0].split('/')[0].strip()
    if 'WHO:' in full_email:
        speak = full_email.split('WHO:')[1].split('\n')[0].split(',')[0].split('/')[0].strip()
    if 'SPEAKER:' in full_email:
        speak = full_email.split('SPEAKER:')[1].split('\n')[0].split(',')[0].split('/')[0].strip()
    if speak is not None:
        full_email = tag_element(full_email, speak, 'speaker')
    return full_email


def tag_element(text, element, tag):
    element = element.strip()
    tag = tag.strip()
    return text.replace(element, "<" + tag + ">" + element + "</" + tag + ">")


def tag_email(cur_email):

    full_email = open(myPath + 'untagged/' + str(cur_email)).read()

    full_email = tag_para_sent(full_email)

    full_email = tag_speak(full_email)

    full_email = tag_times(full_email)

    full_email = tag_loc(full_email)
    # TODO speaker

    with open(myPath + 'tagged/' + str(cur_email), 'w') as file:
        file.write(full_email)
    return full_email


myPath = 'data/email/test/'
onlyFiles = [f for f in listdir(myPath+'untagged/') if isfile(join(myPath+'untagged/', f))]

for email in onlyFiles:
    print(email)
    tag_email(email)

tag_email('364.txt')
