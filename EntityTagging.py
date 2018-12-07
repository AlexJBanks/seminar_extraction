from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from os import listdir
from os.path import isfile, join
mypath = 'C:/Users/alexb/AppData/Roaming/nltk_data/corpora'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
corpusroot = join(mypath, 'pretagged')
corpus = PlaintextCorpusReader(corpusroot, onlyfiles)

file0 = open("/data/email/pretagged/0.txt").read()

print(file0)

# TODO sentence
# TODO paragraph
# TODO stime
# TODO etime
# TODO speaker
# TODO location

# TODO Tokenisation
# TODO PoS
# TODO Named Entity Recognition
# https://canvas.bham.ac.uk/courses/31164/pages/first-steps-in-the-assignment
# https://canvas.bham.ac.uk/courses/31164/pages/more-tips-for-the-assignment
