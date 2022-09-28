import csv
from collections import defaultdict
import copy
import re
import sre_yield
import sys

# check if the crossword is filled
# if yes, return 1
# else return 0


def filled(t):
    b = 1
    for i in t.values():
        if i[0] == "":
            b = 0
            break
    return b

# function to get the words from the regular expressions in
# the txt file


def getWords(regex_file):
    input_filename = regex_file
    g = defaultdict(list)
    r = {}
    # open the csv file
    with open(input_filename) as regex_input:
        # iterate over all the regular expressions in the file
        for regex in regex_input:
            # mark the regular expression as not used
            r[regex.strip()] = "NOT USED"
            # generate all the words
            w = list(sre_yield.AllStrings(regex.strip(), max_count=5))
            for word in w:
                # add the word to the dictionary
                node = [regex.strip(), word, "NOT USED"]
                # check if the word is usefull, match the length of any variable (word)
                if len(word) in sizes.values():
                    if node not in g[len(word)]:
                        g[len(word)].append(node)
    return g, r

# find the word with the most spaces filled to start from


def findStart(t):
    if len(list(t.keys())) == 0:
        max = -1
        word = -1
        for x in w_prototype.keys():
            c = 0
            for y in w_prototype[x][1]:
                if y != ".":
                    c = c + 1
            if c > max:
                word = x
                max = c
    else:
        r = list(t.keys())
        s = list(crossword_data[r[0]].keys())
        word = s[0]
    return word

# read the crossword data from the csv file


def getData(crossword_file):
    all_data = {}
    sizes = {}
    w_prototype = {}
    f = {}
    # open the csv file
    with open(crossword_file) as csv_file:
        # split the csv by the , delimiter
        csv_reader = csv.reader(csv_file, delimiter=",")
        # iterate over all the rows in the csv file
        for row in csv_reader:
            d = {}
            d = {}
            # add the data to the dictionary
            # add the characters provided
            # add the intersection points
            r = re.match("^[a-zA-Z]+$", row[1])
            if r:
                w_prototype[int(row[0])] = [row[1], row[1]]
                f[int(row[0])] = row[1]
            else:
                w_prototype[int(row[0])] = ["", row[1]]
            for i in range(len(row)):
                if i % 2 == 0 and i > 1:
                    d[int(row[i])] = int(row[i+1])
            sizes[int(row[0])] = len(row[1])
            all_data[int(row[0])] = d
    return all_data, sizes, w_prototype, f


# start with an empty stack
stack = []


def crossword_fill(from_word, current_word):
    # append a word
    stack.append(current_word)
    d_current = crossword_data[current_word]
    possible_fits = words[sizes[current_word]]

    # get all the possible words that can fit in the current word
    possible_fits = list(filter(lambda z: z[2] == "NOT USED", possible_fits))
    possible_fits = list(
        filter(lambda s: regex[s[0]] == "NOT USED", possible_fits))

    # filter out all the words that do not fit with characters provided
    c = 0
    for y in w_prototype[current_word][1]:
        if y != ".":
            possible_fits = list(filter(lambda z: z[1][c] == y, possible_fits))
        c = c+1

    for x in d_current.keys():
        d_adj = crossword_data[x]
        if w[x][1][d_current[x]] != ".":
            possible_fits = list(filter(
                lambda z: z[1][d_adj[current_word]] == w[x][1][d_current[x]], possible_fits))

    stuck = 1
    # if there are no words that fit, backtrack
    # else, add the word to the crossword
    if not len(possible_fits) == 0:
        stuck = 0
        # add the word to the crossword
        for i in possible_fits:
            w[current_word] = [i[0], i[1]]
            p = words[sizes[current_word]].index(i)
            words[sizes[current_word]][p][2] = "USED"
            regex[i[0]] = "USED"
            # continiue filling the crossword starting from the neighbours of the current word
            for x in d_current.keys():
                # check if the word is not filled
                if w[x][0] == "":
                    # call again the recursive function to fill
                    stuck = crossword_fill(current_word, x)
                    if stuck == 1:
                        # if the crossword is stuck, backtrack
                        while stack[-1] != current_word:

                            r = stack.pop()
                            if w[r][0] != "":
                                # mark the word as not used
                                p = words[sizes[r]].index(
                                    [w[r][0], w[r][1], "USED"])
                                words[sizes[r]][p][2] = "NOT USED"
                                regex[w[r][0]] = "NOT USED"
                            w[r] = w_prototype[r]
                        break
            # if the crossword is stuck, backtrack
            if stuck == 1:
                # mark the word as not used
                p = words[sizes[current_word]].index(i)  # w[i]
                words[sizes[current_word]][p][2] = "NOT USED"
                regex[i[0]] = "NOT USED"
                w[current_word] = w_prototype[current_word]

            # if the crossword is filled stop the recursion
            if filled(w) or stuck == 0:
                break

    if len(possible_fits) == 1 and current_word == starting and from_word == -1 and stuck == 1:
        p = list(crossword_data[current_word].keys())
        crossword_fill(-1, p[0])
    return stuck

# mark the regular expressions as not used


def save_filled(k):
    for i in list(k.keys()):
        regex[k[i]] = "USED"


# first, read the crossword data from the csv file
crossword_data, sizes, w_prototype, f = getData(sys.argv[1])
# then, read the words from the txt file
words, regex = getWords(sys.argv[2])
w = copy.copy(w_prototype)
save_filled(f)
starting = findStart(f)
# start the recursive algo to fill the crossword
crossword_fill(-1, starting)
# print the crossword solution
for r in range(0, len(w.keys())):
    print(r, w[r][0], w[r][1])
