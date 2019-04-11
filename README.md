# Seminar Extraction
### Natural Language Processing project to extract key information about seminars from raw email text

Written in python, these scripts are designed to batch process raw text from emails, extracting and tagging key information about seminars, then group the seminars based on the subjects they belong to.
This project was completed as formal assessment for a Natural Language Processing module while studing Computer Science at the University of Birmingham in 2018.

The aim was to use a variety of appropriate NLP techniques to achieve reasonable results, and the evaluation of these techniques, rather than the actual accuracy of system itself.
Despite this being the first time I used python, I achieved an grade of __95%__ for this assignment.

The script expects equivalent untagged and tagged training data to be stored in `/data/email/training/untagged` and `/data/email/training/pretagged` respectively. 
Similarly, it expects equivalent test data in the same format in `/data/email/test/...`.
These have been prepopulated with sample data.

### Dependancies
As well as my own code, the system relies on the following utilities that are not bundled due to their size. 
All were used under open source licenses and are easily accessible.

- [NLTK](https://www.nltk.org/), a library for building NLP scripts in python
- [word2vec](https://code.google.com/archive/p/word2vec/), preprocessed word-embedding data structure used for ontology
- [Gensim](https://radimrehurek.com/gensim/), allows us to use word2vec (written in C) in python

## 1. Tagging
### Description
Part 1 of the assignment was to tag various different information points in raw text from emails about seminars.
These key information points were:

| Tag         | Description |
|:-----------:| ----------- |
| `paragraph` | Each block of text within the body of the email |
| `sentence`  | Each segment of text within the paragraphs that has a complete semantic meaning distinct from it's surroundings |
| `stime`     | The time the seminar is due to start |
| `etime`     | The time the seminar is due to end |
| `location`  | The location of the seminar |
| `speaker`   | The name of the speaker in the seminar |

For example, the script should take in 

`The seminar will start at 3:30.`

and return 

`<sentence>The seminar will start at <stime>3:30<\stime>.<\sentence>`

Sometimes not all the information is contained in the email, sometimes the information is duplicated. 
The script should tag all relevant information and nothing more.

### Methodology & Evaluation
I'll quickly summarise the approach, techniques used and effectiveness here;
a full evaluation can be found in `taggingEvaluation.md`.

The actual tagging itself takes place within `EntityTagging.py`.
The script cycles through all found emails and searches for each tag one by one.
After this, `AccuracyCalculator` can be used to calculate the F1 score for each tag in turn, and overall.

| Tag                 | Method | F1 |
|:-------------------:| ------ |:---:|
| `paragraph`         | Tagged first to avoid other tags getting in the way. Uses regex to identify a start and end of a paragraph and select all the content in between. | 71.92% |
| `sentence`          | Tagged at same time as paragraph so other tags don't get in the way. Applies `nltk.sent_tokenize()` to paragraphs. | 75.40%
| `stime` and `etime` | Prioritising different segments of the email, uses regex to pull out strings in a time format and converts them to numbers. The smallest number is selected as start time and (if it exists) the largest number is selected as end time. All instances of these times are then tagged. | 91.36% and 85.64%
| `location`          | Extracts string next to _"Place:"_ if it exists. Else, searches a list of already know locations (extracted from training data via `GetTaggedLocations.py`) tagging any of these if they exists. | 81.07%
| `speaker`           | The most difficult to accurately tag. Searches for _"Speaker:"_, _"Who:"_ or _"WHO:"_ and tags remaining string. | 50.60% 

Overall F1 was __75.96%__


## 2. Ontology
### Description
Using the information about each seminar so far, assign a topic to it.
For Example, a seminar about _Neural Networks_ could be tagged as _Computer Science_.

### Methodology
`makeWordrank.py` sorts through all the words found in all the training emails, calculates their frequency, then normalises this  down to a probability.
For each word, it then calculates the frequency it appears in a large corpora (specifically reuters), finds the normalised probability.
The word is then assigned a value of difference between the probability of appearing in the emails to that of the corpora.
Words are then ranked by this value in descending order, and this gives us an understanding of the most 'significant' words. 
The words that appear more frequently than expected and will probably give us more information about the email. 
This is stored in `/data/ontology/wordrank.txt`

`Ontology.py` uses a hardcoded dictionary to map different topics and sub-topics together.
It then performs on word2vec on each word in an email's topic tag against each word in the dictionary, accumulating a rank of probability for each topic.
Once an email's topic tag has been exhausted, the most probable topic is assigned to that email.
The email name is then appended to that topic in `/data/ontology/predictions.txt`

It's difficult to evaluate how successful this approach was as we don't have a concrete scoring system for it.
As before, a full written up evaluation is available in `ontologyEvaluation.md`
