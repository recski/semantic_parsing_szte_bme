convert.py
To run this script you need Googles' pretrained model, which can be downloaded here: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
It takes a lot of time to run, so the output of the script can be found here as well.
The logic is the following: in each hypothesis and premise pair I gather the roots of the sentences and meausure the similarity between them. I can do this using spacy for the sentense analysis and gensim with Googles' pretrained model for the distance between the words. Then I take the direct neighbours (children) of these roots and find the best matching children from the premise to the hypothesis.

prec_recall.py
Very simple classification class. Can be used to calculate f1 score, precision and recall.

baseline.ipynb
Jupyther notebook containing my attempts.
  avg_diff: Finds the best matching root and its neigbours (children), then calculates an average. If the value is above the threshold, I classify it as "connection" (entailment or contradiction).
  threshold_diff: Finds the best matching root and its neigbours (children), then I check if the root distance and the best neighbour distance are above a given threshold. If so, I classify it as "connection" (entailment or contradiction).
