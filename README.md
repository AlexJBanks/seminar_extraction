# Seminar Extraction
### 2nd Year Natural Language Processing coursework

Written in python, these scripts are designed to batch process raw text from emails, extracting and tagging key information about seminars, then group the seminars based on the subjects they belong to.
This project was completed as formal assessment for a Natural Language Processing module in 2nd of studing Computer Science at the University of Birmingham.

The aim was to use a variety of appropriate NLP techniques to achieve reasonable results, and the evaluation of these techniques, rather than the actual accuracy of system itself.
This was my first time using the python language, and first time using `nltk`.
Overall, I achieved an grade of __95%__ for this assignment.

The script expects equivalent untagged and tagged training data to be stored in `/data/email/training/untagged` and `/data/email/training/pretagged` respectively. 
Similarly, it expects equivalent test data in the same format in `/data/email/test/...`.
These have been prepopulated with sample data.

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
