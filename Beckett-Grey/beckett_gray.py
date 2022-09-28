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
    l = list(x)
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
    x = "0"*n
    final = []
    final.append(x)
    for i in delta:
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
    if l[n-1-i] == "0":
        l[n-1-i] = "1"
    else:
        l[n-1-i] = "0"
    x = "".join(l)
    return x

# check if the code is Canonical
def check_canonical(code):
    d = {}
    for i in range(0, n):
        d[i] = 0
    for c in code:
        if d[int(c)] == 0:
            for k in range(0, int(c)):
                if d[k] == 0:
                    return 0
            d[int(c)] = 1

    return 1


def flip2(x, i, k, queue):
    po = -1
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


def GC_DFS(d, x, max_cord, n, gc):

    if d == (2**n):
        p = gc[:]
        r = find_cyrcle(x)
        p.append(r)
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
        for i in all_codes:
            if i[-1] == -1:
                i.remove(-1)
                print("P", end=" ")
                for k in i:
                    print(k, end="")
                print()
                if args.f:
                    print("P", end=" ")
                    m = full_binary(n, i, -1)
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()

                if args.m:
                    m = full_binary(n, i, -1)
                    print_in_matrix(m)
            else:
                print("C", end=" ")
                for k in i:
                    print(k, end="")
                print()
                if args.m:
                    m = full_binary(n, i, 1)
                    print_in_matrix(m)
                if args.f:
                    print("C", end=" ")
                    m = full_binary(n, i, 1)
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
    
    # find cyclical codes
    if args.c:
        for i in all_codes:
            if i[-1] != -1:
                print("C", end=" ")
                for k in i:
                    print(k, end="")
                print()
                if args.m:
                    m = full_binary(n, i, 1)
                    print_in_matrix(m)
    # find Gray paths
    if args.p:
        for i in all_codes:
            if i[-1] == -1:
                i.remove(-1)
                print("P", end=" ")
                for k in i:
                    print(k, end="")
                print()
                if args.f:
                    print("P", end=" ")
                    m = full_binary(n, i, -1)
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()

                if args.m:
                    m = full_binary(n, i, -1)
                    print_in_matrix(m)
# if we need to find Beckett codes or find the Gray paths (not the cycles)
elif args.b or args.u:
    all = []

    all_codes = []
    n = args.number_of_bits
    arr = [None] * n
    generateAllBinaryStrings(n, arr, 0)
    x = "0" * n
    visited[x] = 1
    queue = []
    GC_BECKETT_DFS(1, x, 0, n, gc, queue)

    # if there are no becket-gray cycles found, show the unfinished ones

    u = 0
    for i in all_codes:
        if i[-1] == -1:
            u = u + 1

    b = len(all_codes) - u

    becket_c = []
    becket_u = []

    # find the Beckett-Gray codes
    if args.b:
        for i in all_codes:
            if i[-1] == -1:
                i.remove(-1)
                becket_u.append(i)
                if b == 0:
                    print("U", end=" ")
                    for k in i:
                        print(k, end="")
                    print()
                    if args.f:
                        print("U", end=" ")
                        m = full_binary(n, i, -1)
                        for i in m:
                            for k in i:
                                print(k, end="")
                            print(" ", end="")
                        print()
                    if args.m:
                        m = full_binary(n, i, -1)
                        print_in_matrix(m)
            else:
                becket_c.append(i)
                print("B", end=" ")
                for k in i:
                    print(k, end="")
                print()
                if args.f:
                    print("Β", end=" ")
                    m = full_binary(n, i, 1)
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
                if args.m:
                    m = full_binary(n, i, 1)
                    print_in_matrix(m)
    # find the Beckett-Gray paths (not the cycles)
    if args.u:
        for i in all_codes:
            if i[-1] == -1:
                i.remove(-1)
                print("U", end=" ")
                for k in i:
                    print(k, end="")
                print("")
                if args.f:
                    print("U", end=" ")
                    m = full_binary(n, i, -1)
                    for i in m:
                        for k in i:
                            print(k, end="")
                        print(" ", end="")
                    print()
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
        if i[-1] == "-1":
            i.pop()
        code = ""
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

        for permutation in l:
            code = ""
            for k in code_searching:
                code = code + permutation[int(k)]
            new_isomorphic.append(code)
        for i in new_isomorphic:
            lo = list(i)
            lo.reverse()
            rev = "".join(lo)
            if check_canonical(rev):
                if rev in all_codes_new and rev not in matches[code_searching] and code_searching not in matches[rev]:
                    if rev != code_searching:
                        matches[code_searching].append(rev)
                        print(code_searching, "<=>", rev)
