# Entity Tagging Evaluation
###### Alex Banks

## General Approach
The base approach I took for the individual tags was to capture as much as possible with RegEx and perform incremental improvements.
For some tags, this base approach was good enough, but others required a lot more work.

## Tags

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
This is to avoid *False Positives* such as tagging the time the email was sent.
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
Any improvments would be minor and only hunting for specific edge cases.

### Paragraphs
#### Technique
Through a series of trial and error, I incrementally improved upon the RegEx for
```regexp
(?m)(?:^)\s+?([A-Z0-9].+?(?:\n.+?)*?[.!?])\s+?(?:$)
```
#### Accuracy
``` 
Precision: 0.7465437788018433
Recall:    0.6937901498929336
F1:        0.7192008879023308
```
#### Improvements

### Sentences
#### Technique
#### Accuracy
``` 
Precision: 0.7426132632961261
Recall:    0.7657413676371022
F1:        0.7540000000000001
```
#### Improvements

### Location
#### Technique
#### Accuracy
``` 
Precision: 0.9104477611940298
Recall:    0.8531468531468531
F1:        0.8808664259927798
```
#### Improvements

### Speaker
#### Technique
#### Accuracy
``` 
Precision: 0.782608695652174
Recall:    0.37388724035608306
F1:        0.5060240963855421
```
#### Improvements

## Overall Accuracy
```
Precision: 0.7902952154733628
Recall:    0.7436143039591315
F1:        0.7662444481000165
```




