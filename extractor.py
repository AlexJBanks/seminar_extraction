from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from os import listdir
from os.path import isfile, join
mypath = 'C:/Users/alexb/AppData/Roaming/nltk_data/corpora'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
corpusroot = join(mypath, 'training')
corpus = PlaintextCorpusReader(corpusroot, onlyfiles)