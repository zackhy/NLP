Unique name:haoyoliu
Name: Haoyou Liu

--------Part A - Lanuage Model--------
Run time: 11.623865 sec

1).
UNIGRAM natural: -13.766408817
BIGRAM natural that: -4.05889368905
TRIGRAM natural that he: -1.58496250072

2).
The perplexity for unigram is 1052.4865859
The perplexity for bigram is 53.8984761198
The perplexity for trigram is 5.7106793082

3).
The perplexity for linear interpolation is 12.5516094886

4).
The result is expected. Because as linear interpolation utilizes all three models and assign them the same weight, the perfomance of each N-gram will be balanced out.
So it will be better than just implement unigram or bigram and worse than just implement trigram.

5).
The perplexity for sample1 is 11.1670289158
The perplexity for sample2 is 1627571078.54
Apparently, sample1 belongs to the Brown dataset, and sample2 doesn't belong to Brown dataset because its perplexity is so large. 
It seems that all the words in sample2 don't exist in the training corpus.

--------Part B - Part-of-Speech Tagging--------
Run time: 375.03843 sec

2).
TRIGRAM CONJ ADV ADP: -2.9755173148
TRIGRAM DET NOUN NUM: -8.9700526163
TRIGRAM NOUN PRT PRON: -11.0854724592

4).
* *: 0.0
Night NOUN: -13.8819025994
Place VERB: -15.4538814891
prime ADJ: -10.6948327183
STOP STOP: 0.0
_RARE_ VERB: -3.17732085089

5).
The accuracy of my tagger: 91.714581664. My tagger's accuracy is 1.73% different from the accuray in the PDF.

6).
The accuracy of NLTK's tagger: 87.9985146677
