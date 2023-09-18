from ast import literal_eval as make_tuple
from copy import deepcopy
import numpy as np

'''
pubkey = Matrix(ZZ, [
    [47, -77, -85],
    [-49, 78, 50],
    [57, -78, 99]
])
'''

# read all lines
with open('enc.txt', 'r') as f:
    lines = f.readlines()

lines = [make_tuple(line.strip()) for line in lines]

print(lines)

potential_r3 = []

def bf_r(x, potential_r3, potential_r4, potential_r5):
    potential_c= []

    sol_r3 = []
    for i in range(0,100+1):
        for j in range(0,100+1):
            for r3 in potential_r3:
                t = x[0] - i*(-49) - j*(57) - r3
                if t % 47 == 0:
                    c = t // 47
                    if c > 0 and c < 255:
                        sol_r3.append((i,j,c,r3))
    
    #print("len after r3", len(sol_r3))
    
    sol_r4 = []
    for i,j,c,r3 in sol_r3:
        for r4 in potential_r4:
            t = x[1] - i*(78) - j*(-78) - r4
            if t % (-77) == 0 and t // -77 == c:
                    sol_r4.append((i,j,c,r3,r4))
                    #if(i==80):
                            #print(i,j,r3,r4)
    #print("len after r4", len(sol_r4))
    
        
    sol_r5 = []
    for i,j,c,r3, r4, in sol_r4:
        for r5 in potential_r5:
            t = x[2] - i*(50) - j*(99) - r5
            if t % (-85) == 0 and t//(-85) == c:
                    sol_r5.append((i,j,c,r3,r4,r5))
                    potential_c.append(c)
                    #if(i==80):
                            #print(i,j, r3, r4, r5)
    #print("len after r5", len(sol_r5))
    #print("potential c:", set(potential_c))
    return sol_r5

potential_r = set()

l = [i for i in range(-50,100)]
result = bf_r(lines[0], deepcopy(l), deepcopy(l) ,deepcopy(l))
potential_r3 =  set([(r3) for i,j,c,r3,r4,r5 in result])
potential_r4 =  set([(r4) for i,j,c,r3,r4,r5 in result])
potential_r5 =  set([(r5) for i,j,c,r3,r4,r5 in result])
potential_r = set([(r3 ,r4, r5) for i,j,c,r3,r4,r5 in result])

for line in lines:

    result = bf_r(line, potential_r3, potential_r4 ,potential_r5)

    potential_r3 =  set([(r3) for i,j,c,r3,r4,r5 in result])
    potential_r4 =  set([(r4) for i,j,c,r3,r4,r5 in result])
    potential_r5 =  set([(r5) for i,j,c,r3,r4,r5 in result])


    potential_r = potential_r.intersection(set([(r3 ,r4, r5) for i,j,c,r3,r4,r5 in result]))
    assert potential_r != set(), "No potential r found!"
    print(potential_r)

open('potential_r.txt', 'w').write("\n".join([str(r) for r in potential_r]))
print(f"\n\nFound {len(potential_r)} potential r values: {potential_r}\n")

for r3,r4,r5 in potential_r:
    flag = ""
    for x0,x1,x2 in lines:
        a = np.array([[47,-49,57],
                      [-77,78,-78],
                      [-85,50,99]])
        b = [x0-r3,x1-r4,x2-r5]
        x = np.linalg.solve(a,b)
        x = np.round_(x)

        flag += chr(int(x[0]))
    print(flag)
