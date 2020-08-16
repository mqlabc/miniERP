import random as rd
for i in range(100):
    a=[]
    b=[]
    if rd.randint(0,1):
        a.append(1)
        b.append(rd.randint(2,6))
    else:
        a.append(rd.randint(2,6))
        b.append(1)