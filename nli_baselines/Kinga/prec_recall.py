class Classification:
    def __init__(self):
        self.TP = 0
        self.FN = 0
        self.FP = 0

    def precision(self):
        return self.TP / (self.TP + self.FP)

    def recall(self):
        return self.TP / (self.TP + self.FN)

    def harmonic(self):
        return 2 / ((1/self.precision()) + (1/self.recall()))
