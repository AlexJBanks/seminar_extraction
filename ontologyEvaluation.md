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
and saved to `normalised_word_popularity.txt`.
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

This was further improved by reducing the scope, first to look at just `Topic:` segment
```regexp
(?m)^(.+?):\s*(.*(?:\n\s+.*)*)
```

Also, by tweaking the definition of a 'word' so that parts of email etc weren't included
```regexp
(?i)(?<=[\s\-(])(\w*[a-z]\w*)(?=[.,')\-\/\s])
``` 

### 2. Defining Departments

## Accuracy


## Further Improvements