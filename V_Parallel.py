from multiprocessing import Process
import threading

dict_obj = {0:"Jupiter",
            1:"Mars",
            2:"Mercury",
            3:"Neptune",
            4:"Pluto",
            5:"Saturn",
            6:"Earth",
            7:"Uranus",
            8:"Venus"}

dict_atr = {0:"small",
            1:"medium",
            2:"large",
            3:"near",
            4:"far",
            5:"yes",
            6:"no"}

def read_matrix(filename):
    file = open(filename, 'r')
    mat = []
    m = 0
    for line in file:
        m = m + 1
        n = 0
        cells = line.strip()
        row = []
        for cell in cells:
            if cell != ' ':
                row.append(int(cell))
                n = n + 1
        mat.append(row)
    return mat, m, n


I, m, n = read_matrix("small_planets.txt")
X = [i for i in range(0, m)]
Y = [i for i in range(0,n)]

print(str(m) + " " + str(n))
#for i in range(m):
#    print(mat[i])
#print(mat[1][1])

rows = []
for y in range(0, n):
    objs = []
    for x in range(0, m):
        if I[x][y]:
            objs.append(x)
    objs_ind = [0 for _ in range(0, m)]
    for i in range(0, len(objs)):
        objs_ind[objs[i]] = 1
    rows.append(objs_ind)
    
#print(rows)

def intersection(P, Q):
    indices =[]
    for i in range(len(P)):
        if P[i] == Q[i]:
            indices.append(i)
    return indices


def computeClosure(A, B, y):
    global I, m, n, rows
    C = []
    D = []
    for i in range(m):
        C.append(0)
    for j in range(n):
        D.append(1) 
    for i in intersection(A, rows[y]):
        C[i] = 1
        for j in range(0, n):
            if I[i][j] == 0:
                D[j] = 0
    return C, D

def generateFrom(A, B, y):
    global X, Y, I, m, n
    #print("------------------")
    #print("A=")
    #print([i for i in range(len(A)) if A[i] == 1])
    #print("B=")
    #print([i for i in range(len(B)) if B[i] == 1])
    #print("------------------")
    if [i for i in range(len(B)) if B[i] == 1] == Y or y > n:
        return
    for j in range(y, n):
        #print(j)
        if B[j] == 0:
            C, D = computeClosure(A, B, j)
            skip = False
            for k in range(0, j-1):
                if D[k] != B[k]:
                    skip = True
                    break
            if skip == False:
                generateFrom(C, D, j+1)
    return

A = []
B = []

A = [1 for i in range(0, m)]
B = [0 for _ in range(0, n)]

#generateFrom(A, B, 0)
def target_f(l):
    for i in range(len(l)):
        A_q = l[i][0]
        B_q = l[i][1]
        y_q = l[i][2]
        generateFrom(A_q, B_q, y_q)
    
P = 6
L = 4
queue = [[] for _ in range(P)]
pss = []
def parallelGenerateFrom(A, B, y, l):
    global L, X, Y, I, m, n, queue, pss
    if l == L:
        sum = 0
        for s in queue:
            sum += len(s)
        r = sum % P
        queue[r].append([A, B, y])
        return
    #process B
    print("------------------")
    print("A=")
    print([dict_obj[i] for i in range(len(A)) if A[i] == 1])
    print("B=")
    print([dict_atr[i] for i in range(len(B)) if B[i] == 1])
    print("------------------")
    jump = False
    if [i for i in range(len(B)) if B[i] == 1] == Y or y > n:
        jump = True
    if jump == False:
         for j in range(y, n):
            #print(j)
            if B[j] == 0:
                C, D = computeClosure(A, B, j)
                skip = False
                for k in range(0, j-1):
                    if D[k] != B[k]:
                        skip = True
                        break
                if skip == False:
                    parallelGenerateFrom(C, D, j+1, l+1)
    if l == 0:
        for r in range(1, P):
            p = threading.Thread(target=target_f, args=(queue[r],))
            pss.append(p)
            pss[-1].start()
            #pss[-1].join()
        #print(queue[0])
        target_f(queue[0])
    return

parallelGenerateFrom(A, B, 0, 0)

for p in pss:
    p.join()

        
        