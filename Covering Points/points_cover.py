import itertools
from os import truncate
import pprint
import argparse
from typing import NewType
import time

# instantiate the parser and give the parameters, arguments and options
parser = argparse.ArgumentParser()
parser.add_argument("file", type=str,
                    help="the name of the points file")
parser.add_argument("-f", "--full", action="store_true",
                    help="run the full algorithm")
parser.add_argument("-g", "--ger", action="store_true",
                    help="use only kathetes/orizonties euthies")
args = parser.parse_args()

# create an empty dictionary to store the points
points = []
input_filename = args.file
# open the txt file and read the points
with open(input_filename) as dots:
    for d in dots:
        (u1, u2) = d.split()
        points.append((int(u1), int(u2)))

# find the line gradient
def find_λ(n):
    l = []
    x1, y1 = n
    for d in points:
        x2, y2 = d
        if x2-x1 == 0:
            if y2-y1 == 0:
                l.append(10000000000)
            else:
                l.append("-")
        else:
            l.append((y2-y1)/(x2-x1))
    return l

# inspect whether the line i found is already in
# there might be a line inside created from the permutation
def is_inside(line, lines):
    permutations = list(itertools.permutations(line, len(line)))
    is_in = 0
    for l in permutations:
        if l in lines:

            is_in = 1
            break
    return is_in


def is_inside_2(line, lines):
    parts = [i for i in line]
    found = False
    for l in lines:
        match = True
        if len(l) != len(line):
            continue
        # it will come here only if the line sizes match
        for p in l:
            if p not in parts:
                match = False
        if match == True:
            found = True
            break
    return found


# check if the points are covererd by the lines
def is_covered(d):
    c = 1
    for i in d.values():
        if i == "not":
            c = 0
            break
    return c


# find the lines
# find only the lines that are horizontal or vertical
if args.ger:
    start_time = time.time()
    lines = []
    new_points = []
    for n in points:
        katheti = 0
        orizontia = 0
        x1, y1 = n
        # add 2 lines with only one point for kathetes/orizonties
        for j in points:
            if n != j:
                x2, y2 = j
                l = []
                if (x2-x1) == 0:
                    λ = "-"
                else:
                    λ = (y2-y1)/(x2-x1)
                # only if λ = 0 or λ ="-" i will continue searching for lines and i will append the line
                if (λ == 0 or λ == "-"):  # if i find one of them, dont append the line with the one point
                    if λ == 0:
                        katheti = 1
                    if λ == "-":
                        orizontia = 1
                    l.append(n)
                    l.append(j)
                    ls = find_λ(j)
                    count = 0
                    for x in ls:
                        if λ == x:
                            if points[count] not in l:
                                l.append(points[count])
                        count = count + 1
                    # it could be a same one with another σειρα in
                    if not is_inside_2(tuple(l), lines):
                        l = sorted(l)
                        lines.append(tuple(l))

        if katheti+orizontia == 0:
            z1, z2 = n
            lines.append((n, (z1+1, z2)))
            new_points.append((z1+1, z2))

    for x in new_points:
        points.append(x)
    end_time = time.time()


else:
    new_points = []
    lines = []
    for n in points:
        x1, y1 = n
        for j in points:
            if n != j:
                x2, y2 = j
                l = []
                if (x2-x1) == 0:
                    λ = "-"
                else:
                    λ = (y2-y1)/(x2-x1)
                l.append(n)
                l.append(j)
                ls = find_λ(j)
                count = 0
                for x in ls:
                    if λ == x:
                        if points[count] not in l:
                            l.append(points[count])
                    count = count + 1
                # it could be a same one with another σειρα in
                if not is_inside_2(tuple(l), lines):
                    lines.append(tuple(l))


if args.full:  # full algorithm
    # get all the combinations
    comb = []
    for i in range(1, len(lines)+1):
        r = list(itertools.combinations(lines, i))
        for c in r:
            comb.append(c)

    # iterate over all the combinations and keep the one that covers all the points
    # and has the minimum number of lines
    best_comb = -1
    best_len = len(points)+1
    for i in comb:
        l = []
        # get all the points covered from the combination
        for j in i:
            for g in j:
                if g not in l:
                    l.append(g)
        # if the combination covers all the points
        if len(l) >= len(points):
            # if the combination has the minimum number of lines up to now
            if len(i) < best_len:
                best_comb = i
                best_len = len(i)
    lysi = sorted(best_comb)


else:  # greedy algorithm
    cov = {}
    for i in points:
        cov[i] = "not"
    lysi = []

    # sort the lines
    lines2 = sorted(lines)
    # iterate as long as the points are not covered
    while not is_covered(cov):
        stren = []
        # iterate over all the lines to find the one that covers the most points
        # and is not already in the solution
        for l in lines2:
            count = 0
            for i in l:
                if (i not in new_points) and cov[i] == "covered":
                    count = count + 1
                elif (i in new_points):
                    count = count + 1
            stren.append((l, len(l)-count))
        m = -1
        for l in stren:
            if l[1] > m:
                m = l[1]
                pl = l[0]
        # add the best line to the solution
        lysi.append(pl)
        # mark the points covered as covered
        for j in pl:
            cov[j] = "covered"

# print the lines of the solution
for line in lysi:
    for p in line:
        print(p, end=' ')
    print()
