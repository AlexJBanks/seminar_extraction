# Ontology Evaluation
###### Alex Banks

## General Approach
Ontology went through a series of 

### 1. Gathering Data
The first step was to gather some data.
I wanted to know which words were most popular in the emails,
but needed to account for some words being popular anyway.

This was achieved by finding the popularity of words in the training emails,
the popularity of words in a large corpus 
(I initially used `brown` but found `reuters` to be more modern and appropriate),
and subtracting brown popularity from the email popularity.
This data is then ordered with the most unique words first,
and saved to `wordrank.txt`.
An excerpt:
```
cmu
cs
edu
...
to
of
the
```
This was further improved by reducing the scope, 
initially looking at `Topic:` and abstract/body together but I found reducing to just `Topic:` more useful.
```regexp
(?m)^(.+?):\s*(.*(?:\n\s+.*)*)
```

Also, by iterative tweaking on the definition of a 'word' so that email addresses, names etc aren't included
the data produces much more valuable words.
```regexp
(?i)(?<=[\s\-\/'(])(\w*[a-z]{2,}\w*)(?=[.,'):\-\/\s])
``` 

### 2. Defining Departments
The easiest way to do this was to hard code in some subjects I was looking for.
Looking at the university website, I copied over a list of departments and colleges, reducing them down to single words.
I put this all into a dictionary, where each entry pointed to either a broader department or an empty string 
(symbolising you had reached the end of the chain)

Once a subject was found for the email you could recursively call that data structure until you get an empty string
e.g. 

`Astronomy -> Physics -> EPS`

`Mechanics -> Engineering -> EPS`

### 3. Word2Vec
The final piece of the puzzle was getting word2vec to play nice.
I initially had issues with setting it up due to my python version 
but it can now successfully report back similarities between word pairs.

Currently, I am using word2vec to compare a word in an email's `Topic:` to each Department, 
then remember the maximum similarity department.
Do this for each word in `Topic:`,
then select the most frequent maximum similarity department, and assign that as the subject.

## Accuracy & Further Improvements
Thus far, ontology is not that accurate.
To begin with, some emails don't have a `Topic:` and so aren't being assigned a subject.

Also, when looking for a subject I'm looking through the entire list of departments including the colleges, 
and the colleges are getting way too many assignments, stealing them from real departments.
Perhaps converting the recursive dictionary structure to a tree data structure would be useful. 
Then I'd only search across leaf nodes of the tree and stop greedy nodes such as `EPS` matching with everything.

An overall improvement could be to take advantage of the ordered list generated in part 1.
Weighting the more common words or more unusual words to have a bigger impact on the data could improve precision.
It could also throw the whole system into chaos, 
and so the weights must be carefully balanced in order to find an appropriate weighting.
It would be unclear as to why that specific weighting would be optimal.

The final improvement would be to use something completely different: e.g. wordnet or wikification 
This could be used to try and find meanings in the most unique words in the hope of finding a clear meaning 
and link to one of the subjects so seminars could be assigned that way.
