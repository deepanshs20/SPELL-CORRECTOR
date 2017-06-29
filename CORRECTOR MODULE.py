from __future__ import division
import re
from time import time
import numpy
from collections import Counter

with open('newdb.txt') as f:
    Text=f.read()
filelen=len(Text)
print (filelen)

def tokens(text):    
    return re.findall('[a-z]+',text.lower())
     

words=tokens(Text);

COUNTS={}
COUNTS = Counter(words)
    
count=len(COUNTS)
print (count)
print ("database has been analyzed")

def prob(word):
    return COUNTS[word]/filelen

def correct(word):
    Corr={}
    F=mostprob(word)
    for charac in F:
        Corr[charac]=prob(charac)

    return max(Corr, key=Corr.get)

 
def mostprob(word):
    return (knownwords([word]) or knownwords(possibilities(word)) or knownwords(possibilities2(word))
             or knownwords(possibilities3(word)) or [word])
    

def knownwords(words):
    return {w for w in words if w in COUNTS}

def possibilities2(word):
        return {p2 for p1 in possibilities(word) for p2 in (possibilities(p1))}
    
def possibilities3(word):
        wdlist=knownwords(possibilities2(word))
        return {p3 for p2 in wdlist for p3 in knownwords(possibilities(p2))}

def possibilities(word):
    pairs=splits(word)
    
    deletes    = [a+b[1:]           for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
    inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
    S= set(deletes + transposes + replaces + inserts)
    return S




def splits(word): 
    return [(word[:i], word[i:])
            for i in numpy.arange(len(word)+1)]
        

alphabet = 'abcdefghijklmnopqrstuvwxyz'
     
def correct_text(text):
    return re.sub('[a-zA-z]+', correct_match, text)

def correct_match(match):
    word=match.group()
    return case_of(word)(correct(word.lower()))

def case_of(text):
    return (str.upper if text.isupper() else
            str.lower if text.islower() else
            str.title if text.istitle() else
            str)


def runproj(filename):
    with open(filename) as f:
        Str=f.read()
    tfb=tokens(Str)
    open("CORRECT.txt","w").close()
    for wrd in tfb:
        corrstr=correct_text(wrd)
        with open("CORRECT.txt","a+") as myfile:
            myfile.write(corrstr)
            myfile.write(' ')
    print ("DONE!")

time_run=time()    
runproj('DeepanshProject.txt')
print(time()-time_run)

'''
def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correct_text(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in COUNTS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, COUNTS[w], right, COUNTS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

spelltest(Testset(open('test1.txt')))
spelltest(Testset(open('test3.txt')))'''