import re
from os import listdir
from os.path import isfile, join


def tag_para(full_email):
    para_exp = r"(^|\n)[A-Z].+(\n.+)+?[.:!?](\n|$)"
    para_iter = re.compile(para_exp).finditer(full_email)
    # TODO paragraph


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
    for timeObj in enumerate(time_iter):

        valid = True
        time = int(timeObj[1].group('hrs')) * 100

        if (timeObj[1].group('ap0') is not None and timeObj[1].group('ap0').lower() == 'p') \
                or (timeObj[1].group('ap1') is not None and timeObj[1].group('ap1').lower() == 'p'):
            time = time + 1200

        if time > 2400:
            valid = False

        mins = 0
        if timeObj[1].group('min0') is not None:
            mins = int(timeObj[1].group('min0'))
        if timeObj[1].group('min1') is not None:
            mins = int(timeObj[1].group('min1'))

        if mins > 59 or mins < 0:
            valid = False
        time = time + mins

        if valid:
            times.setdefault(time, set())
            times[time].add(timeObj[1][0])

    return times


def tag_element(text, element, tag):
    element = element.strip()
    tag = tag.strip()
    return text.replace(element, "<" + tag + ">" + element + "</" + tag + ">")


def tag_email(cur_email):

    print(cur_email)
    full_email = open(myPath + 'untagged/' + str(cur_email)).read()

    full_email = tag_times(full_email)

    # head = full_email.split('Abstract:')[0]
    # body = full_email.split('Abstract:')[1]
    # TODO sentence
    # nltk.senttokenizer

    # TODO speaker
    # TODO location

    # TODO Tokenisation
    # TODO PoS
    # TODO Named Entity Recognition

    with open(myPath + 'tagged/' + str(cur_email), 'w') as file:
        file.write(full_email)
    return full_email


myPath = 'data/email/training/'
onlyFiles = [f for f in listdir(myPath+'untagged/') if isfile(join(myPath+'untagged/', f))]
for email in onlyFiles:
    tag_email(email)

# https://canvas.bham.ac.uk/courses/31164/pages/first-steps-in-the-assignment
# https://canvas.bham.ac.uk/courses/31164/pages/more-tips-for-the-assignment
