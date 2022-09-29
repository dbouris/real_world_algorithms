import time
import argparse

# initialize and parameterize the parser
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-a', action='store_true', default="")
group.add_argument('-b', action='store_true', default="")
group.add_argument('-u', action='store_true', default="")
group.add_argument('-c', action='store_true', default="")
group.add_argument('-p', action='store_true', default="")
group.set_defaults(type="a")

parser.add_argument('-r', action='store_true')
parser.add_argument('-f', action='store_true')
parser.add_argument('-m', action='store_true')
parser.add_argument('number_of_bits', type=int,)
args = parser.parse_args()

# if none of the options are selected, then the default is -a
if not any((args.a, args.b, args.u, args.c, args.p)):
    args.a = True


visited = {}
l = []


def generateAllBinaryStrings(n, arr, i):

    if i == n:
        printTheArray(arr, n)
        return

    arr[i] = 0
    generateAllBinaryStrings(n, arr, i + 1)

    arr[i] = 1
    generateAllBinaryStrings(n, arr, i + 1)

# function to print the array
def printTheArray(arr, n):
    l = []
    s = ""
    for i in range(0, n):
        l.append(str(arr[i]))
        s = s + str(arr[i])
    visited[s] = 0
    all.append(l)

# function to find the cycle in the code
def find_cyrcle(x):
    # the the code in string format
    l = list(x)
    # iterate over the code
    for i in range(0, len(x)):
        if l[i] == "1":
            l[i] = "0"
            x2 = "".join(l)
            if x2 == "0" * n:
                return n-1-i
        l = list(x)
    return -1

# function to get the full binary representation of the code
def full_binary(n, delta, par):
    # instantiate the list as the same size of the code
    x = "0"*n
    final = []
    final.append(x)
    # iterate over the code
    for i in delta:
        # find the corresponding bit
        l = list(x)
        if l[n-1-int(i)] == "0":
            l[n-1-int(i)] = "1"
        else:
            l[n-1-int(i)] = "0"
        x = "".join(l)
        final.append(x)
    if par != -1:
        final.pop(-1)
    return final

# function to prin the code in matrix form
def print_in_matrix(full):
    for i in range(0, n):
        for x in full:
            print(x[n-i-1], end=" ")
        print()

# the function changes the value of bit i in the code x
def flip(x, i, k):
    l = list(x)
    # if the bit is 0, then change it to 1
    if l[n-1-i] == "0":
        l[n-1-i] = "1"
    # if the bit is 1, then change it to 0
    else:
        l[n-1-i] = "0"
    # rejoing the list to a string and return 
    x = "".join(l)
    return x

# check if the code is Canonical
def check_canonical(code):
    # each coordinate k should appear in the sequence before 
    # the first appearance of coordinate k+1

    # initialize the dictionary, values 0
    d = {}
    for i in range(0, n):
        d[i] = 0
    # iterate over the code
    for c in code:
        # if we havent seen the code
        if d[int(c)] == 0:
            # if all the codes less than the current code have not yet appeared
            for k in range(0, int(c)):
                # if we havent yet seen the node
                if d[k] == 0:
                    # then the code is not canonical
                    return 0
            # mark the node as seen
            d[int(c)] = 1
    # return 1 if the code is canonical
    return 1

# second version of the flip function
def flip2(x, i, k, queue):
    po = -1
    # get the list representation of the code
    l = list(x)
    if l[n-1-i] == "0":
        l[n-1-i] = "1"
        queue.append(n-1-i)
        po = 1
    else:
        if len(queue) == 0:
            l[n-1-i] = "0"
        else:
            fi = queue[0]
            if n-1-i == fi:
                l[n-1-i] = "0"
                queue.pop(0)
                po = 0
            else:
                return x, -1, po
    x = "".join(l)
    return x, 1, po


# The algorithm builds Gray codes one at a time
all_codes = []
gc = []

# The algorithm builds Gray codes one at a time using the stack gc 
# and it collects them in the list all_codes, which is initially empty. 
# To call the algorithm, we must initialize the array visited 
# with all its elements set to false, apart from from visited[0]which will 
# be set to true; the gc tack will initially contain element 0
# The algorithm's parameters include the recursion depth, d starting from d=1,
# so that we can define the condition to stop the recursion—when we have visited all 2n 
# nodes of the hypercube. The algorithm uses function 𝙵𝚕𝚒𝚙(x,i) which changes the value 
# of bit i in x When we start x is zero, while max_coord as we don't want to use a 
# coordinate before we use the smaller coordinates, is also zero.
# Author: Panos Louridas


def GC_DFS(d, x, max_cord, n, gc):
    # if we have exhausted the recursion depth
    if d == (2**n):
        p = gc[:]
        r = find_cyrcle(x)
        p.append(r)
        # add the code to the list of all codes
        all_codes.append(p)
        return

    for i in range(0, min(n, max_cord+1)):
        x = flip(x, i, 1)
        if not visited[x]:
            visited[x] = 1
            gc.append(i)
            GC_DFS(d+1, x, max(i+1, max_cord), n, gc)
            visited[x] = 0
            gc.pop()
        x = flip(x, i, 2)


all_codes = []
gc = []

# Implementation of the algorithm GC_DFS, to find the BECKETT codes
def GC_BECKETT_DFS(d, x, max_cord, n, gc, queue):

    if d == (2**n):

        p = gc[:]
        r = find_cyrcle(x)
        p.append(r)
        all_codes.append(p)
        return

    for i in range(0, min(n, max_cord+1)):
        (x, r, ar) = flip2(x, i, 1, queue)
        if visited[x]:
            if ar == 1:
                queue.pop()
            elif ar == 0:
                queue.insert(0, n-1-i)

        if not visited[x] and r != -1:
            visited[x] = 1
            gc.append(i)
            GC_BECKETT_DFS(d+1, x, max(i+1, max_cord), n, gc, queue)
            if ar == 1:
                queue.pop()
            elif ar == 0:
                queue.insert(0, n-1-i)

            visited[x] = 0
            gc.pop()
        if ar != -1:
            x = flip(x, i, 2)

# if we need to find all the codes or find the Gray paths
# or find the cyclical codes
if args.a or args.p or args.c:
    all = []

    all_codes = []
    n = args.number_of_bits
    arr = [None] * n
    generateAllBinaryStrings(n, arr, 0)
    x = "0"*n
    visited[x] = 1
    queue = []
    GC_DFS(1, x, 0, n, gc)

    # find all the codes (cycles and paths)
    if args.a:
        # iterate over all the codes
        for i in all_codes:
            # if the code is canonical
            if i[-1] == -1:
                # remove the last element from the list (-1)
                i.remove(-1)
                # print the code in line form
                print("P", end=" ")
                for k in i:
                    print(k, end="")
                print()
                # if we need to print codes in the full binary representation
                if args.f:
                    print("P", end=" ")
                    # get the full binary representation of the code
                    m = full_binary(n, i, -1)
                    # print the code in line form
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
                # if we need to print the codes in tabular form
                if args.m:
                    # get the full binary
                    m = full_binary(n, i, -1)
                    # print in matrix, tabular form
                    print_in_matrix(m)
            # if the code is cyclical
            else:
                # print the cyclical code in line form
                print("C", end=" ")
                for k in i:
                    print(k, end="")
                print()
                # if we need to print codes in tabular form
                if args.m:
                    # get the full binary
                    m = full_binary(n, i, 1)
                    print_in_matrix(m)
                # if we need to print codes in the full binary representation
                if args.f:
                    print("C", end=" ")
                    # get the full binary representation of the code
                    m = full_binary(n, i, 1)
                    # print in line form
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
    
    # find cyclical codes
    if args.c:
        # iterate over all the codes
        for i in all_codes:
            # if the code is cyclical
            if i[-1] != -1:
                print("C", end=" ")
                for k in i:
                    print(k, end="")
                print()
                # if we need to print codes in the full binary representation
                if args.m:
                    # get the full binary
                    m = full_binary(n, i, 1)
                    # print in matrix, tabular form
                    print_in_matrix(m)
    # find Gray paths
    if args.p:
        # iterrate over all the codes
        for i in all_codes:
            # if the code is canonical
            if i[-1] == -1:
                i.remove(-1)
                # print the code in line form
                print("P", end=" ")
                for k in i:
                    print(k, end="")
                print()
                # if we need to print codes in the full binary representation
                if args.f:
                    print("P", end=" ")
                    # get the full binary representation
                    m = full_binary(n, i, -1)
                    # print in line form
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
                # if we need to print codes in tabular form
                if args.m:
                    m = full_binary(n, i, -1)
                    print_in_matrix(m)
# if we need to find Beckett codes or find the Gray paths (not the cycles)
elif args.b or args.u:
    all = []

    all_codes = []
    n = args.number_of_bits
    arr = [None] * n
    # get all the binary strings
    generateAllBinaryStrings(n, arr, 0)
    x = "0" * n
    visited[x] = 1
    queue = []
    # use the algorithm GC_BECKETT_DFS to find the Beckett codes
    GC_BECKETT_DFS(1, x, 0, n, gc, queue)

    # if there are no becket-gray cycles found, show the unfinished ones
    # get the unfinished codes, the canonical codes
    u = 0
    for i in all_codes:
        if i[-1] == -1:
            u = u + 1

    b = len(all_codes) - u

    becket_c = []
    becket_u = []

    # find the Beckett-Gray codes
    if args.b:
        # iterate over all the codes
        for i in all_codes:
            # if the code is canonical, not cyclic
            if i[-1] == -1:
                i.remove(-1)
                becket_u.append(i)
                if b == 0:
                    print("U", end=" ")
                    for k in i:
                        print(k, end="")
                    print()
                    # if we need to print codes in the full binary representation
                    if args.f:
                        print("U", end=" ")
                        # get the full binary representation
                        m = full_binary(n, i, -1)
                        for i in m:
                            for k in i:
                                print(k, end="")
                            print(" ", end="")
                        print()
                    # if we need to print codes in tabular form
                    if args.m:
                        m = full_binary(n, i, -1)
                        print_in_matrix(m)
            # if the code is cyclical
            else:
                becket_c.append(i)
                # print the code in line form
                print("B", end=" ")
                for k in i:
                    print(k, end="")
                print()
                # if we need to print codes in the full binary representation
                if args.f:
                    print("Β", end=" ")
                    # get the full binary representation
                    m = full_binary(n, i, 1)
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
                # if we need to print codes in tabular form
                if args.m:
                    # get the full binary
                    m = full_binary(n, i, 1)
                    # print 
                    print_in_matrix(m)
    # find the Beckett-Gray paths (not the cycles)
    if args.u:
        # iterate over all the codes
        for i in all_codes:
            # if the code is canonical, not cyclic
            if i[-1] == -1:
                i.remove(-1)
                # print the code in line form
                print("U", end=" ")
                for k in i:
                    print(k, end="")
                print("")
                # if we need to print codes in the full binary representation
                if args.f:
                    # print in line form
                    print("U", end=" ")
                    # get the full binary representation
                    m = full_binary(n, i, -1)
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
                # if we need to print codes in tabular form
                if args.m:
                    m = full_binary(n, i, -1)
                    print_in_matrix(m)

# find the reverse isomorphic codes
if args.r:

    if b > 0:
        all_codes = becket_c
    else:
        all_codes = becket_u

    # get all the codes in a string form
    all_codes_new = []
    for i in all_codes:
        # if the code is not cyclic
        if i[-1] == "-1":
            i.pop()
        code = ""
        # get the code and append in the new codes list
        for k in i:
            code = code + str(k)
        all_codes_new.append(code)

    import itertools
    s = ""
    for k in range(0, n):
        s = s + str(k)
    l = list(itertools.permutations(s, n))
    l.pop(0)
    found = []

    li = []
    for i in all_codes_new:
        for permutation in l:
            code = ""
            for k in i:
                code = code + permutation[int(k)]
            li.append(code)

    f = []
    for i in li:
        lo = list(i)
        lo.reverse()
        rev = "".join(lo)
        if check_canonical(rev):
            f.append(rev)

    matches = {}
    for i in all_codes_new:
        matches[i] = []

    # ADDITIONS add check for when the same string is produced from a code
    # AND do not print the code that has no isomorphic codes produced from it
    for code_searching in all_codes_new:
        # find all the possible metathesis
        # reverse them
        # check if they are canonical

        new_isomorphic = []
        reversed = []
        # find all the possible permutations
        for permutation in l:
            code = ""
            for k in code_searching:
                code = code + permutation[int(k)]
            new_isomorphic.append(code)
        # iterate over all the possible permutations
        for i in new_isomorphic:
            lo = list(i)
            # reverse the code
            lo.reverse()
            rev = "".join(lo)
            # check if the code is canonical
            if check_canonical(rev):
                if rev in all_codes_new and rev not in matches[code_searching] and code_searching not in matches[rev]:
                    if rev != code_searching:
                        matches[code_searching].append(rev)
                        print(code_searching, "<=>", rev)
