# Seminar Extraction
### 2nd Year Natural Language Processing coursework

Written in python, these scripts are designed to batch process raw text from emails, extracting and tagging key information about seminars, then group the seminars based on the subjects they belong to.
This project was completed as formal assessment for a Natural Language Processing module in 2nd of studing Computer Science at the University of Birmingham.
The aim was to use a variety of appropriate NLP techniques to achieve reasonable results, and the evaluation of these techniques, rather than the actual accuracy of system itself.
This was my first time using the python language, and first time using `nltk`.
Overall, I achieved an grade of __95%__ for this assignment.

The script expects a 

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
The script should tag all relevant information and nothing more

### Methodology


### Evaluation 
