import spacy

import jsonlines
from spacy.symbols import nsubj,nsubjpass, VERB


nlp=spacy.load('en')

def does_itfit(word1,word2):
    comparable1=nlp(word1)
    comparable2=nlp(word2)
    try:
        chance=comparable1.similarity(comparable2)
        return chance
    except TypeError:
        return 1
    


def does_it_fit(comparable1,comparable2):
    try:

        chance = comparable1.similarity(comparable2)
        return chance

    except TypeError:
        return 1


def entailment(string1,string2):
    print("doesn't have obj")
    negated=False
    doc=nlp(string2)
    docx=nlp(string1)
    maxs=0
    for chunk2 in doc.noun_chunks:
        for chunk1 in docx.noun_chunks:
            if chunk2.root.dep_=='nsubj' or chunk2.root.dep_=='nsubjpass' :
                if does_it_fit(chunk1,chunk2)>maxs or does_it_fit(chunk1.root,chunk2.root)>maxs:
                    Subject2=chunk2
                    Subject1=chunk1
                    maxs=max(does_it_fit(chunk1,chunk2),does_it_fit(chunk1.root, chunk2.root))


    if maxs==0:
        return 0,1,0,'ncont'
    ROOT2=None
    for token in doc:
        if token.dep_=='ROOT':
            ROOT2=token
            Relation2=set()
            Relation2.add(token)
    if ROOT2==None:
        return maxs,1,0,'ncont'

    for child in ROOT2.children:
        helper = False
        for token in Subject2:
            if token.text==child.text:
                helper=True
        if helper==False:
            Relation2.add(child)

    ROOT1 = None
    maxr=0
    for token in docx:
        if token.pos_=='VERB':
            if does_it_fit(ROOT2,token)>maxr:
                ROOT1=token
                maxr=does_it_fit(ROOT2,token)

    Relation1 = set()
    Relation1.add(ROOT1)
    if ROOT1==None:
        return maxs,1,0,'ncont'
    for child in ROOT1.children:
        helper = False
        for token in Subject1:
            if token.text==child.text:
                helper=True
        if helper==False:
            Relation1.add(child)

    for token in Relation1:
        if token.dep_=='neg':
            negated=not negated
    for token in Relation2:
        if token.dep_=='neg':
            negated=not negated
    removallist = []
    for item in Relation2:
        if item.is_stop:
            removallist.append(item)
    for item in removallist:
        Relation2.remove(item)
    removallist = []
    for item in Relation1:
        if item.is_stop:
            removallist.append(item)
    for item in removallist:
        Relation1.remove(item)
    rel1 = repr(Relation1)
    rel2 = repr(Relation2)

    maxrel=does_itfit(rel1, rel2)
    if negated==True:
        return maxs,1,maxrel,'cont'
    else:
        return maxs,1,maxrel,'ncont'


def entailment2(string1,string2):
    print("has obj")
    negated=False
    doc = nlp(string2)
    docx = nlp(string1)
    maxs=0
    maxo=0
    for chunk2 in doc.noun_chunks:
        for chunk1 in docx.noun_chunks:
            if chunk2.root.dep_ == 'nsubj' or chunk2.root.dep_ == 'nsubjpass':
                if does_it_fit(chunk1, chunk2) > maxs or does_it_fit(chunk1.root, chunk2.root)>maxs:
                    Subject2 = chunk2
                    Subject1 = chunk1
                    maxs = max(does_it_fit(chunk1, chunk2),does_it_fit(chunk1.root, chunk2.root))

    if maxs == 0:
        return 0,0,0,'ncont'
    for chunk2 in doc.noun_chunks:
        for chunk1 in docx.noun_chunks:
            if chunk2.root.dep_=='pobj' or chunk2.root.dep_=='iobj' or chunk2.root.dep_=='dobj':
                if does_it_fit(chunk1, chunk2) > maxo or does_it_fit(chunk1.root,chunk2.root)>maxo:
                    Object2=chunk2
                    Object1=chunk1
                    maxo=max(does_it_fit(chunk1, chunk2),does_it_fit(chunk1.root, chunk2.root))

    if maxo==0:
        return maxs, 0, 0, 'ncont'

    ROOT2=None
    for token in doc:
        if (Subject2.root.head==token and Object2.root.head==token) or (
                token.is_ancestor(Subject2.root.head) and token == Object2.root.head) or (
                token.is_ancestor(Object2.root.head) and token==Subject2.root.head) or (
                token.is_ancestor(Subject2.root.head) and token.is_ancestor(Object2.root.head)) :
            ROOT2=token
            Relation2=set()
            Relation2.add(token)
    if ROOT2==None:
        return maxs,maxo,0,'ncont'
    for child in ROOT2.children:
        if child.is_ancestor(Subject2.root) or child.is_ancestor(Object2.root) or child==Object2.root or child==Subject2.root :
            Relation2.add(child)

    Relation22=set()
    for item in Relation2:
        Relation22.add(item)
        for kid in item.children:
            Relation22.add(kid)


    ROOT1=None
    for token in docx:
        if (Subject1.root.head == token and Object1.root.head == token) or (
                token.is_ancestor(Subject1.root.head) and token == Object1.root.head) or (
                token.is_ancestor(Object1.root.head) and token == Subject1.root.head) or (
                token.is_ancestor(Subject1.root.head) and token.is_ancestor(Object1.root.head)):
            ROOT1=token
            Relation1=set()
            Relation1.add(token)
    if ROOT1==None:return maxs,maxo,0,'ncont'

    for child in ROOT1.children:
        if child.is_ancestor(Subject1.root) or child.is_ancestor(
            Object1.root) or child == Object1.root or child == Subject1.root:
                Relation1.add(child)

    Relation11 = set()
    for item in Relation1:
        Relation11.add(item)
        for kid in item.children:
            Relation11.add(kid)

    for token in Relation11:
        if token.dep_=='neg':
            negated=not negated
    for token in Relation22:
        if token.dep_=='neg':
            negated=not negated
    removallist=[]
    for item in Relation22:
        if item.is_stop:
            removallist.append(item)
    for item in removallist:
        Relation22.remove(item)

    removallist = []
    for item in Relation11:
        if item.is_stop:
            removallist.append(item)
    for item in removallist:
        Relation11.remove(item)

    rel1=repr(Relation11)
    rel2=repr(Relation22)
    maxrel=does_itfit(rel1, rel2)
    if negated==True:
        return maxs,maxo,maxrel,'cont'
    else:
        return maxs,maxo,maxrel,'ncont'




def ENTAIL(str1,str2):
    
    docx=nlp(str2)
    for token in docx:
        if token.dep_=='pobj' or token.dep_=='iobj'  or token.dep_=='dobj':
            ret=entailment2(str1,str2)
            return ret


    retrn=entailment(str1,str2)
    return retrn



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
with jsonlines.open('/home/csiszp/Downloads/multinli_1.0/multinli_1.0_dev_matched.jsonl') as f: # opening file in binary(rb) mode
   for item in f:
        all=all+1
        labellist.append(item['gold_label'])
        simlist.append(ENTAIL(item['sentence1'],item['sentence2']))
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

    EPrec=TPE/(TPE+FPE)
    ERec=TPE/(TPE+FNE)
    Fscore_E=2/(1/EPrec+1/ERec)

    TPC=True_Hit_Contradiction
    FPC=Judged_Contradiction_When_Entailment+Judged_Contradiction_When_Neutral
    TNC=all-FPC-TPC-Judged_Entailment_When_Contradiction-Judged_Neutral_When_Contradiction
    FNC=Judged_Entailment_When_Contradiction+Judged_Neutral_When_Contradiction

    CPrec=TPC/(TPC+FPC)
    CRec=TPC/(TPC+FNC)
    Fscore_C=2/(1/CPrec+1/CRec)

    TPN=True_Hit_Neutral
    FPN=Judged_Neutral_When_Entailment+Judged_Neutral_When_Contradiction
    FNN=all-Judged_Neutral_When_Entailment+Judged_Neutral_When_Contradiction
    TNN=all-TPN-FPN-FNN

    NPrec=TPN/(TPN+FPN)
    NRec=TPN/(TPN+FNN)
    Fscore_N=2/(1/NPrec+1/NRec)

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



