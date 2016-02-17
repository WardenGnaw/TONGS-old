# sentiment-data

Data about the sentiment (typically valence) of words.
All data files are comma separated with fields quoted with double quotes and a header row.
Valence is always between 0 and 10 (inclusive), but you should not try to compare valence from different methods.

## anew.csv
Data straight from [ANEW (Affective Norms for English Words)](http://www.uvm.edu/~pdodds/teaching/courses/2009-08UVM-300/docs/others/everything/bradley1999a.pdf).
ANEW provides many different sentiment value for words, valence is often the most useful.

## stopwords.csv
Just some standard stopwords.

## tcr.csv
Valence generated from our "Tweet Concurrence Rating" method.
TCR works like VGS but instead of using a search engine, the SPOONS tweet corpus is used.
See [Detecting Netflix Service Outages Through Analysis Of Twitter Posts](http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1765&context=theses).

## tcr_terms.csv
The positive and negative values used to calculate VGS and TCR.

## vgs.csv
Valence generated from our "Valence Generation Search" method.
VGS uses a search engine and compares the number of results returned when a word is searched with known good or bad words (see tcr_terms.csv) for these words.
See [Detecting Netflix Service Outages Through Analysis Of Twitter Posts](http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1765&context=theses).

## sentiment-word-list.csv
http://sentiwordnet.isti.cnr.it/
