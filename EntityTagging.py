import re

file0 = open("data/email/pretagged/0.txt").read()

timeExp = r"(?i)(?P<hrs>\d{1,2})(?::(?P<min0>\d{2}) ?(?P<ap0>[ap]).?m|:(?P<min1>\d{2})| ?(?P<ap1>[ap]).?m)"
paraExp = r"(^|\n)[A-Z].+(\n.+)+?[.:!?](\n|$)"

timeIter = re.compile(timeExp).finditer(file0)
paraIter = re.compile(paraExp).finditer(file0)

times = {}
mintime = 2400
maxtime = 0
for timeObj in enumerate(timeIter):

    valid = True
    time = int(timeObj[1].group('hrs'))*100

    if (timeObj[1].group('ap0') is not None and timeObj[1].group('ap0').lower() == 'p')\
            or (timeObj[1].group('ap1') is not None and timeObj[1].group('ap1').lower() == 'p'):
        time = time + 1200

    if time > 2400: valid = False

    mins = 0
    if timeObj[1].group('min0') is not None:
        mins = int(timeObj[1].group('min0'))
    if timeObj[1].group('min1') is not None:
        mins = int(timeObj[1].group('min1'))

    if mins > 59 or mins < 0: valid = False
    time = time + mins

    if valid:
        times[time] = timeObj
        mintime = min(time, mintime)
        maxtime = max(time, maxtime)

print(times[mintime])
print(times[maxtime])







# TODO stime
# TODO etime
# TODO paragraph
# TODO sentence
# nltk.senttokenizer

# TODO speaker
# TODO location

# TODO Tokenisation
# TODO PoS
# TODO Named Entity Recognition
# https://canvas.bham.ac.uk/courses/31164/pages/first-steps-in-the-assignment
# https://canvas.bham.ac.uk/courses/31164/pages/more-tips-for-the-assignment
