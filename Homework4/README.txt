Unique Name: haoyoliu
Name: Haoyou Liu

---- Part A - IBM Models 1 & 2 ----
1).
IBM Model 1
---------------------------
Average AER: 0.665

2).
IBM Model 2
---------------------------
Average AER: 0.650

3).
Sentence pair:
[u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']
[u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']

IBM Model 1:
0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1
AER: 0.75

IBM Model 2:
0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0
AER: 0.666666666667

From the two values of AER, we can see that IBM Model 2 computed a more accurate alignment on this pair. This is because IBM model 1 just simply sets all alignment parameters to a fixed value, while IBM model 2 caculated the alignment parameters for different word pairs. As a result, IBM model 2 is more accurate.

4).
The number of iterations:1
IBM Model 1
---------------------------
Average AER: 0.873
Time:3.764237

The number of iterations:2
IBM Model 1
---------------------------
Average AER: 0.684
Time:7.562141

The number of iterations:3
IBM Model 1
---------------------------
Average AER: 0.641
Time:12.043653

The number of iterations:4
IBM Model 1
---------------------------
Average AER: 0.630
Time:15.211019

The number of iterations:5
IBM Model 1
---------------------------
Average AER: 0.627
Time:19.212498

The number of iterations:6
IBM Model 1
---------------------------
Average AER: 0.626
Time:21.386344

The number of iterations:7
IBM Model 1
---------------------------
Average AER: 0.629
Time:22.084356

The number of iterations:8
IBM Model 1
---------------------------
Average AER: 0.631
Time:24.068949

The number of iterations:9
IBM Model 1
---------------------------
Average AER: 0.628
Time:27.594938

The number of iterations:10
IBM Model 1
---------------------------
Average AER: 0.665
Time:34.348829

The number of iterations:11
IBM Model 1
---------------------------
Average AER: 0.666
Time:40.166036

The number of iterations:12
IBM Model 1
---------------------------
Average AER: 0.666
Time:44.716077

The number of iterations:13
IBM Model 1
---------------------------
Average AER: 0.666
Time:48.610106

The number of iterations:14
IBM Model 1
---------------------------
Average AER: 0.665
Time:46.88751

The number of iterations:15
IBM Model 1
---------------------------
Average AER: 0.665
Time:46.383235

The number of iterations:16
IBM Model 1
---------------------------
Average AER: 0.665
Time:47.935891

The number of iterations:17
IBM Model 1
---------------------------
Average AER: 0.662
Time:61.407689

The number of iterations:18
IBM Model 1
---------------------------
Average AER: 0.661
Time:63.221593

The number of iterations:19
IBM Model 1
---------------------------
Average AER: 0.661
Time:56.761951

The number of iterations:1
IBM Model 2
---------------------------
Average AER: 0.646
Time:36.073017

The number of iterations:2
IBM Model 2
---------------------------
Average AER: 0.644
Time:41.07088

The number of iterations:3
IBM Model 2
---------------------------
Average AER: 0.644
Time:48.922241

The number of iterations:4
IBM Model 2
---------------------------
Average AER: 0.642
Time:78.162102

The number of iterations:5
IBM Model 2
---------------------------
Average AER: 0.644
Time:62.686058

The number of iterations:6
IBM Model 2
---------------------------
Average AER: 0.647
Time:69.720958

The number of iterations:7
IBM Model 2
---------------------------
Average AER: 0.646
Time:91.427811

The number of iterations:8
IBM Model 2
---------------------------
Average AER: 0.649
Time:107.034068

The number of iterations:9
IBM Model 2
---------------------------
Average AER: 0.649
Time:131.860307

The number of iterations:10
IBM Model 2
---------------------------
Average AER: 0.650
Time:115.590067

The number of iterations:11
IBM Model 2
---------------------------
Average AER: 0.649
Time:117.990936

The number of iterations:12
IBM Model 2
---------------------------
Average AER: 0.650
Time:131.24384

The number of iterations:13
IBM Model 2
---------------------------
Average AER: 0.652
Time:131.494854

The number of iterations:14
IBM Model 2
---------------------------
Average AER: 0.652
Time:192.653714

The number of iterations:15
IBM Model 2
---------------------------
Average AER: 0.650
Time:152.926792

The number of iterations:16
IBM Model 2
---------------------------
Average AER: 0.650
Time:160.50283

The number of iterations:17
IBM Model 2
---------------------------
Average AER: 0.651
Time:195.165754

The number of iterations:18
IBM Model 2
---------------------------
Average AER: 0.651
Time:176.035699

The number of iterations:19
IBM Model 2
---------------------------
Average AER: 0.651
Time:162.843907

From the results above, we can see that when the number of iterations equals 6, IBM model 1 has the lowest AER, which is 0.626. And when the number of iterations equals 4, IBM model 2 has the lowest AER, which is 0.642.
Relationship: In the begining, as the number of iterations increases, the average AERs of the two models decreases. And after the average AERs reach the lowest point, they start increase. And finally, the average AER of IBM model 1 seems to stabilize at around 0.66 and the average AER of IBM model 2 seems to stabilize at around 0.65.

---- Part B  - Berkeley Aligner ----
4).
Berkeley Aligner
---------------------------
Average AER: 0.548

From part A, we knew that the average AER of IBM model 1 is 0.665 and IBM model 2 is 0.650. So compared to both the IBM models, the average AER of the berkeley aligner is much less, which means that the berkeley aligner is better than both the IBM models.

5).
Same sentence pair from part A:
[u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']
[u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']

Berkeley Aligner:
0-0 1-1 2-0 3-2 4-7 5-10 6-10 7-7 8-10 9-3 10-11
AER: 0.6

We can see that the berkeley aligner computed a more accurate alignment on this pair than IBM model 1 and IBM model 2. This is because the berkeley aligner considers two directions, that is, from English to German as well as from German to English, while both the IBM models only consider one direction. 

