Unique name: haoyoliu
Name: Haoyou Liu


-----Dependency graphs-----

1. How to determine if a dependency graph is projective?
For any arc in the dependency graph which connects a specific child and a specific parent, if there is another arc which connects one node which locates within the subsentence between that child and that parent and another node which locates outside the subsentence between that child and that parent, then the dependency graph is non-projective.
In other words, dependency graph can be determined as projective unless there are no crossing denpendency arcs.

2. Examples of a projective sentence and a non-projective sentence
Projective sentence: Tony enjoys listening to music in his spare time.
Non-projective sentence: What does Tony enjoy doing in his spare time?

-----Manipulating configurations-----

The performance of my parser using badfeatures.model:
UAS: 0.229038040231
LAS: 0.125473013344

-----Dependency parsing-----

1. For Swedish:

Scores before adding any features:
UAS: 0.304321848237
LAS: 0.178848834893

Socres after adding only CPOSTAG:
UAS: 0.718581955786
LAS: 0.61262696674
Complexity of CPOSTAG: O(n)

Scores after adding only POSTAG:
UAS: 0.76976697869
LAS: 0.655247958574
Complexity of POSTAG: O(n)

Scores after adding only LEMMA:
UAS: 0.302330213105
LAS: 0.17924716192
Complexity of LEMMA: O(n)

Scores after adding only DISTANCE (distance between the word on top of the stack and the first word in the input buffer):
UAS: 0.313881696873
LAS: 0.181437960566
Complexity of DISTANCE: O(n)

Scores after adding only DES (the number of children of a particular word, divided into left children and right children):
UAS: 0.357697669787
LAS: 0.226448914559
Complexity of DES: O(n^2)

Scores after adding all five features(the swedish.model):
UAS: 0.787890858395
LAS: 0.679944234216
Complexity of feature extractor: O(n^2)

2. For Danish:

Scores before adding any features:
UAS: 0.711377245509
LAS: 0.628143712575

Socres after adding only CPOSTAG:
UAS: 0.760878243513
LAS: 0.69001996008

Scores after adding only POSTAG:
UAS: 0.792215568862
LAS: 0.712574850299

Scores after adding only LEMMA:
UAS: 0.708183632735
LAS: 0.627944111776

Scores after adding only DISTANCE (distance between the word on top of the stack and the first word in the input buffer)
UAS: 0.724550898204
LAS: 0.644111776447

Scores after adding only DES (the number of children of a particular word, divided into left children and right children)
UAS: 0.743512974052
LAS: 0.657684630739

Scores after adding all five features(the danish.model):
UAS: 0.797804391218
LAS: 0.717964071856

3. For English:
Scores before adding any features:
UAS: 0.404938271605
LAS: 0.323456790123

Socres after adding only CPOSTAG:
UAS: 0.585185185185
LAS: 0.555555555556

Scores after adding only POSTAG:
UAS: 0.679012345679
LAS: 0.649382716049

Scores after adding only LEMMA:
UAS: 0.397530864198
LAS: 0.323456790123

Scores after adding only DISTANCE (distance between the word on top of the stack and the first word in the input buffer)
UAS: 0.437037037037
LAS: 0.343209876543

Scores after adding only DES (the number of children of a particular word, divided into left children and right children)
UAS: 0.503703703704
LAS: 0.40987654321

Scores after adding all five features(the english.model):
UAS: 0.750617283951
LAS: 0.718518518519

The complexity of the arc-eager shift-reduce parser:
The arc-eager shift-reduce parser itself has linear time complexity, which is O(n).
But since I implemented some features and the complexity of my feature extractor is O(n^2), the complexity of my arc-eager shift-reduce parser is O(n^3)

What tradeoffs it makes:
As I added more features, the accuray of the arc-eager shift-reduce parser increased but the complexity of the parser increased too, so there is a tradeoff between speed and accuracy.