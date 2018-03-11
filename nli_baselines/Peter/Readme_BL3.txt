This is the simplest of the baselines as it only does two things.

First it removes all stopwords from the second sentence, the hypothesis, then it tries to find a best fit for each remaining token, using spacy.
We store those similarities in a list, average them, then pass them on for evaluation.

It also contains a basic contradiction condition, if the statements together contain an odd number of negations, and they are prevously judged as entailment:
Judge it as contradiction instead.

The Similarity Threshold between Entailment and Neutral is set by the user once the averaging completes for all 10k sentences.
