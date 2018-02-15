The code for now can only determine wether the sentence pair relation is entailment or neutral, poorly at that.
Efficiency rate is slightly above 50%

The first, larger sentence, sentence1 will be referred to as A. Sentence2 will be referred to as B.

The code uses POS and Dependency parsing to evaluate the pair.

The Decision making method:
Example for demonstrative purposes: "In 2030, the World Cup was in Russia, but the hungarian team didn't qualify.

1: Does B have dobj or iobj , in other words, does it have a target. Ex: "The World Cup were held by Russia" the pobj of the Sentence is Russia
(using spaCy, one can not only find words, but groups of worlds in relation with one another)
2a: If it does, identify the subject and object of B and find suitable counterparts in A using spaCy. If it doesn't find good matches, the pair is neutral.
3a: If it does find good matches, tag them in both sentences as Subject 1 and 2, Target 1 and 2. 2 for B, 1 for A
4a: Gather the shared ancestors in the dependency tree of Subject 1 and Target 1 and compare them with Subject 2 and Target 2.
5a: If the Targets, Subjects, and their shared ancestors are all determined to be similiar: Entailment (or possibly contradiction), if any of these does not match: Neutral

2b: If it does not find pobj dependencies, then just compare find a match for B's subject in A.
3b: If found, separate the subject and the rest of the sentence. Find the Root dependency of B and find a matching counter part in A. Criteria: Is a VERB and is ancestor of the subject.
4b: Compare the descendants of the suitable ROOT found in A, with B minus it's subject.
5b: If that matches, tag as entailment. If the subjects didn't match or the ROOT descendants didn't match: tag as neutral.

Current success rate: 3560/6787


Version 0.3 Due to too many false negatives, I lightened the constrictions on what I the algorithm considers a matching subject and object.

Current success rate: 3637/6787
When considering entailment vs neutral:

False Neg:  2206 /was entailment, but judged as neutral
False Pos:  759 /was neutral but judged as entailment
True Neg:  2364 /was neutral, correctly judged
True Pos:  1273 /was entailment, correctly judged

Version 0.4

Added the ability to detect Contradictions based on a very simple method:
If the sentence pairs look like an entailment, check how many "neg" dependencies are in each sentence.
In other words: if the Subj and Obj matches but if they contain an uneven number of nots and didn'ts and wasn'ts etc.
Example: Susie went to meet Mike. Susie didn't go out to see Mike.

Added new analysis tags: True Hit Neutral/Entailment/Contradiction and Judged N/E/C When N/E/C
Here are the statistics:
THE:  537
THN:  2851
THC:  279
JEWN:  221
JEWC:  255
JCWN:  51
JCWE:  76
JNWC:  2679
JNWE:  2866
3667  /  10000

Notes on this iteration: This way of looking for contradictions seems alright as 279 out of 406 C judgements were correct.
The code decides too easily that the pair is Neutral: 2851 correct out of more than 8400 N judgements.
Entailment is 537 out of 1013.
To do: Compare the A branch and B branch effectiveness. Take a closer look at JNWE as it seems to be the largest source of errors
and find out why so many sentence pairs get tagged as Neutral.

Version 1.0 : BASELINE:

Optimised speed, now should finish analyzing the corpus in the fraction of the original time.
Added stopword removal into the analysis of the relationship between subject and object.
Added adjustable threshold: HOW TO:
Change the path to the NLI Corpus in the code before you run it.
Install spaCy
Install jsonlines
Download the english spaCy language module
Run the code
When it says 10000/10000 input a number between 0 and 1,
that will be the threshold above which you consider two tokens, chunks or sentences similiar.
Observe the statistics of your choice in the output.


