import csv
from collections import defaultdict
import copy
import re
import sre_yield
import sys

def filled(t):
    b= 1
    for i in t.values():
        if i[0] =="":
            b=0
            break
    return b

def getWords(regex_file):
    input_filename = regex_file
    g = defaultdict(list)
    r ={}

    with open(input_filename) as regex_input:
        for regex in regex_input:
            r[regex.strip()]="NOT USED"
            w = list(sre_yield.AllStrings(regex.strip(),max_count=5))
            for word in w:
                node = [regex.strip(),word,"NOT USED"]
                if len(word) in sizes.values():
                    if node not in g[len(word)]:
                        g[len(word)].append(node)
    return g,r
                
def findStart(t):
    if len(list(t.keys()))==0:
        max = -1
        word = -1
        for x in w_prototype.keys():
            c=0
            for y in w_prototype[x][1]:
                if y != ".":
                    c = c +1
            if c > max:
                word = x
                max = c 
    else: 
        r = list(t.keys())
        s= list(crossword_data[r[0]].keys())
        word = s[0]
    return word

def getData(crossword_file):
    all_data ={}
    sizes = {}
    w_prototype={}
    f = {}
    with open(crossword_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter= ",")
        for row in csv_reader:
            d={}
            d={}
            r = re.match("^[a-zA-Z]+$",row[1])
            if r:
                w_prototype[int(row[0])]=[row[1],row[1]]
                f[int(row[0])]=row[1]
            else:
                w_prototype[int(row[0])]=["",row[1]]
            for i in range(len(row)):
                if i % 2==0 and i>1:
                    d[int(row[i])]=int(row[i+1])
            sizes[int(row[0])]= len(row[1])
            all_data[int(row[0])]=d
    return all_data, sizes,w_prototype,f


stack = []
def crossword_fill(from_word, current_word):
    stack.append(current_word)
    d_current = crossword_data[current_word]
    possible_fits = words[sizes[current_word]]
    
    possible_fits = list(filter(lambda z: z[2]== "NOT USED", possible_fits))
    possible_fits = list(filter(lambda s: regex[s[0]]=="NOT USED",possible_fits))

    c = 0 
    for y in w_prototype[current_word][1]:
        if y != ".":
            possible_fits = list(filter(lambda z: z[1][c]==y , possible_fits))
        c= c+1

    for x in d_current.keys():
        d_adj = crossword_data[x]
        if w[x][1][d_current[x]] != ".":
            possible_fits = list(filter(lambda z: z[1][d_adj[current_word]]==w[x][1][d_current[x]],possible_fits))
              
    stuck = 1
    if not len(possible_fits)==0:
        stuck = 0
        for i in possible_fits:
            w[current_word]=[i[0],i[1]]
            p = words[sizes[current_word]].index(i)
            words[sizes[current_word]][p][2] = "USED"
            regex[i[0]]="USED"
            
            for x in d_current.keys():
                if w[x][0] == "":
                    stuck = crossword_fill(current_word, x)
                    if stuck == 1:
                        while stack[-1]!= current_word:

                            r = stack.pop()
                            if w[r][0] !="":
                                
                                p = words[sizes[r]].index([w[r][0],w[r][1],"USED"])
                                words[sizes[r]][p][2] = "NOT USED"
                                regex[w[r][0]]="NOT USED"
                            w[r]=w_prototype[r] 
                        break 
                
            if stuck ==1:
                p = words[sizes[current_word]].index(i) # w[i]
                words[sizes[current_word]][p][2] = "NOT USED" 
                regex[i[0]]="NOT USED"
                w[current_word]=w_prototype[current_word] 
            
            if filled(w) or stuck==0:
                break
    
    if len(possible_fits)==1 and current_word==starting and from_word==-1 and stuck ==1:
        p = list(crossword_data[current_word].keys())
        crossword_fill(-1,p[0])
    return stuck
                
def save_filled(k):
    for i in list(k.keys()):
        regex[k[i]]="USED"

crossword_data,sizes,w_prototype,f= getData(sys.argv[1])
words,regex = getWords(sys.argv[2])
w = copy.copy(w_prototype)
save_filled(f)
starting = findStart(f)     
crossword_fill(-1,starting)
for r in range(0,len(w.keys())):
    print(r, w[r][0],w[r][1])

