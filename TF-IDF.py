import pandas as pd

def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]

def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf

csv=r'C:\Users\navee\Downloads\000000_0.csv'
keys=[]
d={}

with open(csv,'r') as f:
    x=f.readlines()
    for each in x:
        q=each.split(',')
        keys.append(q[-1].rstrip())
              
keys=list(dict.fromkeys(keys))
print "the top 10 users userID is"
print keys

for val in keys:
    for each in x:
        q=each.split(',')
        if q[-1].rstrip() == val:
            for each in q[:-1]:
                set_key(d,val,each)

for each in keys:
    body=[]
    title=[]
    body.append(d[each][0::2])
    title.append(d[each][1::2])
    for i in range(0,len(body)):
        docA=str(body[i])
        docB=str(title[i])  
        bowA = docA.split(" ")
        bowB = docB.split(" ")   
        wordSet = set(bowA).union(set(bowB))
        wordDictA = dict.fromkeys(wordSet, 0) 
        wordDictB = dict.fromkeys(wordSet, 0)
        for word in bowA:
            wordDictA[word]+=1
        for word in bowB:
            wordDictB[word]+=1
        pd.DataFrame([wordDictA, wordDictB])
        tfBowA = computeTF(wordDictA, bowA)
        tfBowB = computeTF(wordDictB, bowB)
        idfs = computeIDF([wordDictA, wordDictB])
        tfidfBowA = computeTFIDF(tfBowA, idfs)
        tfidfBowB = computeTFIDF(tfBowB, idfs)
        pd.DataFrame([tfidfBowA, tfidfBowB])
        c=len(tfidfBowA)
        print "top 10 TF-IDF values of user with userID:{}".format(each)
        for key, value in sorted(tfidfBowA.items(), key=lambda item: item[1] , reverse=True)[:10]:
            print("%s: %s" % (key, value))
        
        
