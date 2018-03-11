def evaluate(scores, labellist):
    Accuracies = []
    Contra_Prec = []
    Contra_Rec = []
    Contra_Fscore = []
    Neutral_Prec = []
    Neutral_Rec = []
    Neutral_Fscore = []
    Entail_Prec = []
    Entail_Rec = []
    Entail_Fscore = []
    for point in range(1, 999):
        threshold = point / 1000
        Results = []
        for score in scores:
            if abs(float(score)) > threshold:
                if float(score) > 0:
                    Result = "entailment"
                if float(score) < 0:
                    Result = "contradiction"
            if abs(float(score)) < threshold:
                Result = "neutral"
            Results.append(Result)

        all = 0
        success = 0
        True_Hit_Entailment = 0
        True_Hit_Neutral = 0
        True_Hit_Contradiction = 0
        Judged_Entailment_When_Neutral = 0
        Judged_Entailment_When_Contradiction = 0
        Judged_Contradiction_When_Neutral = 0
        Judged_Contradiction_When_Entailment = 0
        Judged_Neutral_When_Contradiction = 0
        Judged_Neutral_When_Entailment = 0
        outliers = []

        for i, Result in enumerate(Results):
            all += 1
            if Result == 'entailment' and labellist[i] == 'entailment':
                True_Hit_Entailment += 1
                success += 1
            if Result == 'contradiction' and labellist[i] == 'contradiction':
                True_Hit_Contradiction += 1
                success += 1
            if Result == 'neutral' and labellist[i] == 'neutral':
                True_Hit_Neutral += 1
                success += 1
            if Result == 'contradiction' and labellist[i] == 'neutral':
                Judged_Contradiction_When_Neutral += 1
                if point > 950:
                    outliers.append(i)
            if Result == 'contradiction' and labellist[i] == 'entailment':
                Judged_Contradiction_When_Entailment += 1
            if Result == 'neutral' and labellist[i] == 'contradiction':
                Judged_Neutral_When_Contradiction += 1
                if point < 50:
                    outliers.append(i)
            if Result == 'neutral' and labellist[i] == 'entailment':
                Judged_Neutral_When_Entailment += 1
                if point < 50:
                    outliers.append(i)
            if Result == 'entailment' and labellist[i] == 'contradiction':
                Judged_Entailment_When_Contradiction += 1
            if Result == 'entailment' and labellist[i] == 'neutral':
                Judged_Entailment_When_Neutral += 1
                if point > 950:
                    outliers.append(i)
            if labellist[i] != 'entailment' and labellist[i] != 'contradiction' and labellist[i] != 'neutral':
                outliers.append(i)

    # Calculating statistics

        TPN = True_Hit_Neutral
        FPN = Judged_Neutral_When_Entailment + Judged_Neutral_When_Contradiction
        FNN = Judged_Contradiction_When_Neutral + Judged_Entailment_When_Neutral
        TNN = all - TPN - FPN - FNN

        TPC = True_Hit_Contradiction
        FPC = Judged_Contradiction_When_Entailment + Judged_Contradiction_When_Neutral
        FNC = Judged_Neutral_When_Contradiction + Judged_Entailment_When_Contradiction
        TNC = all - FNC - FPC - TPC

        TPE = True_Hit_Entailment
        FPE = Judged_Entailment_When_Neutral + Judged_Entailment_When_Contradiction
        FNE = Judged_Contradiction_When_Entailment + Judged_Neutral_When_Entailment
        TNE = all - FPE - TPE - FNE

        try:
            CPrec = TPC / (TPC + FPC)
        except ZeroDivisionError:
            CPrec = 0

        try:
            CRec = TPC / (TPC + FNC)
        except ZeroDivisionError:
            CRec = 0

        try:
            Fscore_C = 2 / (1 / CPrec + 1 / CRec)
        except ZeroDivisionError:
            Fscore_C = 0

        try:
            EPrec = TPE / (TPE + FPE)
        except ZeroDivisionError:
            EPrec = 0

        try:
            ERec = TPE / (TPE + FNE)
        except ZeroDivisionError:
            ERec = 0

        try:
            Fscore_E = 2 / (1 / EPrec + 1 / ERec)
        except ZeroDivisionError:
            Fscore_E = 0

        try:
            NPrec = TPN / (TPN + FPN)
        except ZeroDivisionError:
            NPrec = 0

        try:
            NRec = TPN / (TPN + FNN)
        except ZeroDivisionError:
            NRec = 0

        try:
            Fscore_N = 2 / (1 / NPrec + 1 / NRec)
        except ZeroDivisionError:
            Fscore_N = 0

        Accuracies.append(success / all)
        Contra_Prec.append(CPrec)
        Contra_Rec.append(CRec)
        Contra_Fscore.append(Fscore_C)
        Neutral_Prec.append(NPrec)
        Neutral_Rec.append(NRec)
        Neutral_Fscore.append(Fscore_N)
        Entail_Prec.append(EPrec)
        Entail_Rec.append(ERec)
        Entail_Fscore.append(Fscore_E)
    return Accuracies,Contra_Prec,Contra_Rec,Contra_Fscore, \
           Neutral_Prec,Neutral_Rec,Neutral_Fscore, \
           Entail_Prec, Entail_Rec, Entail_Fscore, outliers

def evalrel(scores,labellist):
    RelPrec = []
    RelRec = []
    Fscores_R = []
    Acc = []
    outliers=[]
    for point in range(1, 999):
        threshold = point / 1000
        Results = []
        for score in scores:
            if abs(float(score)) > threshold:
                if float(score) > 0:
                    Result = "entailment"
                if float(score) < 0:
                    Result = "contradiction"
            if abs(float(score)) < threshold:
                Result = "neutral"
            Results.append(Result)

        all = 0
        success = 0
        True_Hit_Entailment = 0
        True_Hit_Neutral = 0
        True_Hit_Contradiction = 0
        Judged_Entailment_When_Neutral = 0
        Judged_Entailment_When_Contradiction = 0
        Judged_Contradiction_When_Neutral = 0
        Judged_Contradiction_When_Entailment = 0
        Judged_Neutral_When_Contradiction = 0
        Judged_Neutral_When_Entailment = 0

        for i, Result in enumerate(Results):
            all += 1
            if Result == 'entailment' and labellist[i] == 'entailment':
                True_Hit_Entailment += 1
                success += 1
            if Result == 'contradiction' and labellist[i] == 'contradiction':
                True_Hit_Contradiction += 1
                success += 1
            if Result == 'neutral' and labellist[i] == 'neutral':
                True_Hit_Neutral += 1
                success += 1
            if Result == 'contradiction' and labellist[i] == 'neutral':
                Judged_Contradiction_When_Neutral += 1

            if Result == 'contradiction' and labellist[i] == 'entailment':
                Judged_Contradiction_When_Entailment += 1
                success += 1
            if Result == 'neutral' and labellist[i] == 'contradiction':
                Judged_Neutral_When_Contradiction += 1

            if Result == 'neutral' and labellist[i] == 'entailment':
                Judged_Neutral_When_Entailment += 1

            if Result == 'entailment' and labellist[i] == 'contradiction':
                Judged_Entailment_When_Contradiction += 1
                success+=1

            if Result == 'entailment' and labellist[i] == 'neutral':
                Judged_Entailment_When_Neutral += 1

            if labellist[i] != 'entailment' and labellist[i] != 'contradiction' and labellist[i] != 'neutral':
                outliers.append(i)

        # Calculating statistics

        TPR = True_Hit_Contradiction + True_Hit_Entailment + Judged_Contradiction_When_Entailment + Judged_Entailment_When_Contradiction
        FPR = Judged_Entailment_When_Neutral + Judged_Contradiction_When_Neutral
        FNR = Judged_Neutral_When_Contradiction + Judged_Neutral_When_Entailment
        TNR = all - FNR - FPR - TPR

        try:
            RPrec = TPR / (TPR + FPR)
        except ZeroDivisionError:
            RPrec = 0

        try:
            RRec = TPR / (TPR + FNR)
        except ZeroDivisionError:
            RRec = 0

        try:
            Fscore_R = 2 / (1 / RPrec + 1 / RRec)
        except ZeroDivisionError:
            Fscore_R = 0

        RelPrec.append(RPrec)
        RelRec.append(RRec)
        Fscores_R.append(Fscore_R)
        Acc.append(success / all)

    return Acc, RelPrec, RelRec, Fscores_R

