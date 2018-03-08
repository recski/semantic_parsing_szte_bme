convert.py: To run this script you need Googles' pretrained model, which can be downloaded here: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
It takes a lot of time to run, so the output of the script can be found here as well.
prec_recall.py: Very simple classification class. Can be used to calculate f1 score, precision and recall.
baseline.ipynb: Jupyther notebook containing my attempts.
  avg_diff: Finds the best matching root and its neigbours, then calculates an average. If the value is above the threshold, I classify it as "connection" (entailment or contradiction).
  threshold_diff: Finds the best matching root and its neigbours, then I check if the root and the neighbours are above a given threshold. If so, I classify it as "connection" (entailment or contradiction).
