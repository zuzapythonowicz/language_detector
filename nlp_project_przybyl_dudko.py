from googletrans import Translator
from nltk.tag import pos_tag
import more_itertools  
import pprint
import matplotlib.pyplot as plt
import sys
import nltk
import spacy
import easygui
import io

text = ""

option = input("Welcome to Language Detector, enter 1 to write sentence or 2 to open a file\n")
if option == '1':
    text = input("Enter your sentence\n")
    
elif option == '2':
    path = easygui.fileopenbox()
    file = io.open(path, mode="r", encoding="utf-8")
    text = file.read()
    
else:
     exit()

for line in sys.stdin:
    text += line

translator = Translator()
s = 0
ix = []
ls = []
for sentence in text.split("."):
    if (len(sentence) == 0):
        continue
    ix.append([0])
    language = ""
    i=0
    for p in list(more_itertools.windowed(sentence.split(),n=2,step=1)):
        d = translator.detect(" ".join(p))
        if i == 0:
            language = d.lang
            ls.append(d.lang)
        if language != "":
           if d.lang != language and d.confidence == 1.0:
                ix[s].append(i)
                language = d.lang
                ls.append(d.lang)
        i = i+1
        #print(" ".join(p) + "   " + str(translator.detect(" ".join(p))))
    ix[s].append(len(sentence.split()))
    s=s+1

#print(ls)
#print(ix)
i = 0
s = 0


def pairToHtml(pair):
    tag = pair[0]
    content = pair[1]
    return "<"+tag+">"+content+"</"+tag+">"

dataForGraph = dict()

sentences = []

for xd in ix:
    sentence = []
    for [i1,i2] in more_itertools.windowed(xd, n=2,step=1):
        sentence.append((ls[i]," ".join(text.split(".")[s].split()[i1:i2])))
        #print(ls[i] + " -- " + " ".join(text.split(".")[s].split()[i1:i2]))
        if ls[i] in dataForGraph:
            dataForGraph[ls[i]] += len(text.split(".")[s].split()[i1:i2])
        else:
            dataForGraph[ls[i]] = len(text.split(".")[s].split()[i1:i2])
        i+=1
    sentences.append(sentence)
    s += 1

print(".&nbsp;".join(list(map(lambda x: "&nbsp;".join(list(map(pairToHtml,x))), sentences))))

nlp = spacy.load("xx_ent_wiki_sm")
doc = nlp(text)


for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)


fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
langs = dataForGraph.keys()
vals = dataForGraph.values()
ax.bar(langs,vals)
plt.show()