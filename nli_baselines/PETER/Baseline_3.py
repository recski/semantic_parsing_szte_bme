import spacy
import jsonlines
nlp=spacy.load('en')

def pair_avg(sent1,sent2):
    doc=nlp(sent1)
    docx=nlp(sent2)
    simple2=[]
    simple1=[]
    for token in docx:
      if token.is_stop==False:
        simple2.append(token)

    for token in doc:
        if token.is_stop == False:
            simple1.append(token)



    averages=[]
    for token in simple2:
        maxsim=0
        for tick in simple1:
            try:
                SIM=token.similarity(tick)
            except TypeError:
                if len(token.text)==1 and len(token.text)==1:
                    SIM=1
                else:
                    SIM=0


            if SIM>maxsim:
                maxsim=SIM
        averages.append(maxsim)
        negated=False
    for token in doc:
        if token.dep_=='neg':
            negated=not negated
    for token in docx:
        if token.dep_=='neg':
            negated=not negated
    tog=sum(averages)
    avg=sum(averages)/len(averages)
    if negated:
        #return tog,tog,tog,'cont'
        return avg,avg,avg,'cont'
    if not negated:
        #return tog,tog,tog,'ncont'
        return avg,avg,avg,'ncont'

all=0
success=0
True_Hit_Entailment=0
True_Hit_Neutral=0
True_Hit_Contradiction=0
Judged_Entailment_When_Neutral=0
Judged_Entailment_When_Contradiction=0
Judged_Contradiction_When_Neutral=0
Judged_Contradiction_When_Entailment=0
Judged_Neutral_When_Contradiction=0
Judged_Neutral_When_Entailment=0

simlist=[]
labellist=[]
with jsonlines.open(multinli_1.0_dev_matched.jsonl') as f: # opening file in binary(rb) mode
   for item in f:
        all=all+1
        labellist.append(item['gold_label'])
        simlist.append(pair_avg(item['sentence1'],item['sentence2']))
        print(all, "/10000")
print(len(simlist))
print(len(labellist))
CRIT=0.9
while CRIT!=0:

    alli = 0
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
    CRIT=input()
    CRIT=float(CRIT)
    if CRIT==0:        break


    for i in range(10000):
        alli=alli+1
        print (simlist[i])
        if simlist[i][3] == 'cont':
            Result='contradiction'
        if simlist[i][3] == 'ncont' and simlist[i][2]>CRIT:
            Result='entailment'
        for t in simlist[i][0:2]:
            if t<CRIT:
                Result='neutral'


        if Result=='entailment' and labellist[i]== 'entailment':
            True_Hit_Entailment=True_Hit_Entailment+1
            success=success+1
        if Result=='contradiction' and labellist[i]== 'contradiction':
            True_Hit_Contradiction=True_Hit_Contradiction+1
            success=success+1
        if Result=='neutral' and labellist[i]== 'neutral':
            True_Hit_Neutral=True_Hit_Neutral+1
            success=success+1
        if Result=='contradiction' and labellist[i]== 'neutral':
            Judged_Contradiction_When_Neutral=Judged_Contradiction_When_Neutral+1
        if Result=='contradiction' and labellist[i]== 'entailment':
            Judged_Contradiction_When_Entailment=Judged_Contradiction_When_Entailment+1
        if Result=='neutral' and labellist[i]== 'contradiction':
            Judged_Neutral_When_Contradiction=Judged_Neutral_When_Contradiction+1
        if Result=='neutral' and labellist[i]== 'entailment':
            Judged_Neutral_When_Entailment=Judged_Neutral_When_Entailment+1
        if Result=='entailment' and labellist[i]== 'contradiction':
            Judged_Entailment_When_Contradiction=Judged_Entailment_When_Contradiction+1
        if Result=='entailment' and labellist[i]== 'neutral':
            Judged_Entailment_When_Neutral=Judged_Entailment_When_Neutral+1
        if labellist[i]!='entailment' and labellist[i]!='contradiction' and labellist[i]!='neutral':
            print ("Error:" , labellist[i])
        print("THE: ",True_Hit_Entailment)
        print("THN: ",True_Hit_Neutral)
        print("THC: ",True_Hit_Contradiction)
        print("JEWN: ",Judged_Entailment_When_Neutral)
        print("JEWC: ",Judged_Entailment_When_Contradiction)
        print("JCWN: ",Judged_Contradiction_When_Neutral)
        print("JCWE: ",Judged_Contradiction_When_Entailment)
        print("JNWC: ",Judged_Neutral_When_Contradiction)
        print("JNWE: ",Judged_Neutral_When_Entailment)
        print(success, " / ", alli)




    TPE=True_Hit_Entailment
    FPE=Judged_Entailment_When_Neutral+Judged_Entailment_When_Contradiction
    TNE=all-FPE-TPE-Judged_Contradiction_When_Entailment-Judged_Neutral_When_Entailment
    FNE=Judged_Contradiction_When_Entailment+Judged_Neutral_When_Entailment
    try:
        EPrec=TPE/(TPE+FPE)
        ERec=TPE/(TPE+FNE)
        Fscore_E=2/(1/EPrec+1/ERec)
    except ZeroDivisionError:
        Fscore_E=0


    TPC=True_Hit_Contradiction
    FPC=Judged_Contradiction_When_Entailment+Judged_Contradiction_When_Neutral
    TNC=all-FPC-TPC-Judged_Entailment_When_Contradiction-Judged_Neutral_When_Contradiction
    FNC=Judged_Entailment_When_Contradiction+Judged_Neutral_When_Contradiction

    CPrec=TPC/(TPC+FPC)
    CRec=TPC/(TPC+FNC)
    Fscore_C=2/(1/CPrec+1/CRec)

    TPN=True_Hit_Neutral
    FPN=Judged_Neutral_When_Entailment+Judged_Neutral_When_Contradiction
    FNN=Judged_Contradiction_When_Neutral+Judged_Entailment_When_Neutral
    TNN=all-TPN-FPN-FNN
    try:
        NPrec=TPN/(TPN+FPN)
    except ZeroDivisionError:
        NPrec=0
    try:
        NRec=TPN/(TPN+FNN)
    except ZeroDivisionError:
        NRec=0
    try:
        Fscore_N=2/(1/NPrec+1/NRec)
    except ZeroDivisionError:
        Fscore_N=0
    print("Neutral Recall: ",NRec)
    print("Neutral Precision: ",NPrec)
    print("Neutral Fscore: ",Fscore_N)

    print("Contradiction Recall: ",CRec)
    print("Contradiction Precision: ",CPrec)
    print("Contradiction Fscore: ",Fscore_C)

    print("Enatilment Recall: ",ERec)
    print("Enatilment Precision: ",EPrec)
    print("Enatilment Fscore: ",Fscore_E)

print(success, " / ",all)
