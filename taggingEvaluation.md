# Entity Tagging Evaluation
###### Alex Banks

## General Approach
The base approach I took for the individual tags was to capture as much as possible with RegEx and perform incremental improvements.
For some tags, this base approach was good enough, but others required a lot more work.

I messed around with the order the tags were applied too, finding that the larger scope tags 
(`paragraph`, `sentence`) worked better when applied before smaller scope tags (`stime`/`etime`)

## Tags

### Paragraphs
#### Technique
Through a series of trial and error, I incrementally improved upon the RegEx for paragraph until it was suitable enough.
```regexp
(?m)^\s+?([A-Z0-9].+?(?:\n.+?)*?[.!?])\s+?$
```
Looking for the start of a line, with some optional whitespace,
the first character should be a capital or number, then the rest of the line, 
numerous other optional lines until you reach some punctuation, optional whitespace then the end of a line.
#### Accuracy
``` 
Precision: 0.7465437788018433
Recall:    0.6937901498929336
F1:        0.7192008879023308
```
#### Improvements
There's a few edge cases not accounted for, such as paragraphs starting with punctuation, e.g. `(`, `<` 
but this is rare for this application. 
I tried including these and **recall** improved slightly, but **precision** took a major hit, *lowering* **F1**.
The script was attempting to tag metadata in the Abstract.

I also apply the script on the abstract and body, 
but sometimes the regex likes to unnecessarily tag lines in the abstract, leading to lower **precision**.
Reducing the scope to just the body may improve this.

### Sentences
#### Technique
Like other tags, I initially tried to capture this with RegEx but both **precision** and **recall** were too poor.
Instead, the sentence tagged now makes use of `nltk.sent_tokenize()`, returning a list of sentences from email.
In an attempt to improve **precision**, I previously reduced the scope down to just my paragraphs,
but the low **paragraph recall** lead to sentence tagging having an *even less* **recall**
Instead, the scope now is just the abstract and body
#### Accuracy
``` 
Precision: 0.7426132632961261
Recall:    0.7657413676371022
F1:        0.7540000000000001
```
#### Improvements
As discussed above, An improvement to **paragraph recall** would mean 
I could change the scope of the tokenizer to just the paragraphs, in an attempt to improve **precision**.

### Start / End times
#### Technique
As both Start and End times have similar formats, I capture these at the same time.
This also avoids me accidentally tagging the same time as both `stime` and `etime`.
The easiest way to capture all times throughout the document was RegEx:
```regexp
(?i)(?P<hrs>\d{1,2})(?::(?P<min0>\d{2}) ?(?P<ap0>[ap]).?m|:(?P<min1>\d{2})| ?(?P<ap1>[ap]).?m)
```
Ignoring case, the regex looks for 1 or 2 digits, followed by either:
- a colon, then 2 digits
- am or pm (with or without a space, with or without dots)
- or both *but not neither*

For this particular RegEx, I made great use of Named Capture Groups as this improves readability of my code.

Once all possible times are captured, they are parsed to an integer
(e.g. `3pm -> 1500` `13:45 -> 1345`),
the times validated (e.g. `3672` is not valid) and a dictionary of sets is generated
where the the key is the int and the set is all strings in each email represented by the int.
This allows me to pick one `stime`/`etime` and tag all strings that fit those times.

Picking the times is pretty easy, I just select the smallest time as `stime` and largest times as `etime`,
with integers making the comparison easy, ensuring they aren't equivalent.
In order to improve accuracy, I change the scope that this analysis is performed over.
1. Just the `Time:` line in the head (if it exists)
2. Just the abstract and body

If `stime` or `etime` haven't been allocated by this point then they aren't tagged. 
This is to avoid reducing **precision** by tagging irrelevant times such as the time the email was sent.
#### Accuracy
Start Time
``` 
Precision: 0.9136125654450262
Recall:    0.9136125654450262
F1:        0.9136125654450262
```
End Time
``` 
Precision: 0.8659217877094972
Recall:    0.8469945355191257
F1:        0.8563535911602211
```
#### Improvements
I'm really happy with the F1 for both `stime` and `etime` and 
I think they realistically can't be improved much further.
Any improvements would be minor and only hunting for specific edge cases.

### Location
#### Technique
The first step of tagging location, is simply to look in the header / abstract and pull out `Place:` if it exists.
This already gave me a great **precision** but only an ok **recall**.

The second method of this is to lookup possible locations in a premade list.
`GetTaggedLocations.py` does this by iterating through all known pretagged emails, 
pulling out location, ordering them by length (largest first), and saving them all to a text file.
Now, if `Place:` doesn't exist then we iterate through this list until we find a match, not tagging anything if we don't.
#### Accuracy
``` 
Precision: 0.8945147679324894
Recall:    0.7412587412587412
F1:        0.8107074569789675
```
#### Improvements
The use of these two completely separate techniques gave me a great F1.
I tried adding other key words to look for such as `Location:` or `WHERE:` but both of these made no effect -
those cases were all already captured by `Place:`

Potentially some Named Entity Recognition would work well for improving **Recall** here,
but that would increase the complexity of the analysis for not much payoff, and potentially reduce **Precision** a lot.

### Speaker
#### Technique
Similar to location, the first step is to look for a series of key words that would indicate the speaker.
`Speaker:`, `Who:` and `WHO:` all worked pretty good at pulling out the already known speakers.
Unfortunately, this only accounts for not even half the the corpus.
#### Accuracy
``` 
Precision: 0.782608695652174
Recall:    0.37388724035608306
F1:        0.5060240963855421
```
#### Improvements
I tried a similar technique to Location by saving a list of all known speakers and looking them up,
but this significantly reduced **precision** with little improvement to **recall**, so was omitted.

I noticed in test data speakers were sometimes alone on a single line,
I attempted to use RegEx to pull out these speakers:
```regexp
--+\s*?(\w+(?:.? \w+)*.?)\n
```
A line of minuses, followed by some words on a different line.
Again, this identified a few edge cases and improved **recall** a little but drastically reduced **precision**,
so was omitted.

There was also the possibility of extracting names using the text file of names provided,
but these lists are not exhaustive and do very little to improve **recall**

The only realistic way I can see to improve this score is to use some advanced Named Entity Recognition.
This would drastically improve pulling out names but there are often multiple names in the emails.
You would still have to somehow rank which name is more likely to be the speaker,
with ambiguities leading to lower **precision** but this would be counteracted by the large increase in **recall**

Once the NER is setup, it could be used to help improve `location` tagging too.

Alternatively, the `names` package in `nltk` may have been useful 
but probably suffered from the same problems as the text files.
## Overall Accuracy
```
Precision: 0.7877229080932785
Recall:    0.7333971902937421
F1:        0.7595899470899472
```
On the whole, both **precision** and **recall** rank over 70% and so seem pretty successful to me.
The vast majority of tags the system is making are correct
and the system is tagging the vast majority of possible tags.
The inaccuracies are mostly the edge cases which are obviously more difficult to tag correctly.
The only way to realistically improve these scores are to make better use of the specific tools available in `nltk`,
such as a NER system or POS tagger. 