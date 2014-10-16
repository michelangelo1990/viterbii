import math
import sys

f=open("model_hydro.txt", "r")
##ucitavamo duljinu modela
dmod=int(f.readline())

def make_float(v):
    for i in range(len(v)):
        v[i]=float(v[i])
        
def mmake_float(v):
    for i in range(len(v)):
        for j in range(len(v[i])):
            v[i][j]=float(v[i][j])

def stanje(razina, br):
    return razina*3+br

stup=dmod+2

T=[[0 for x in xrange(stup*3)] for x in xrange(stup*3)]
Me=[]
Ie=[]
razina=0
for i in range(3*dmod):
    mt=[]
##oznacava da citam tranzicijsku matricu
    if i%3==0:
        for j in range(3):
            line=f.readline()
            if not line.strip():
                line=f.readline()
            ls=line.split()
            make_float(ls)
            T[i+j][3*razina+1]=ls[1]
            T[i+j][3*razina+3]=ls[0]
            T[i+j][3*razina+5]=ls[2]
        razina=razina+1
##oznacava da citam emisijsku matricu match stanja
    if i%3==1:
        line=f.readline()
        if not line.strip():
            line=f.readline()
        ls=line.split()
        make_float(ls)
        Me.append(ls)
##oznacava da citam emisijsku matricu insert stanja
    if i%3==2:
        line=f.readline()
        if not line.strip():
            line=f.readline()
        ls=line.split()
        make_float(ls)
        Ie.append(ls)
f.close()

ak=['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']

def mylog(x):
    if x==0:
        return -100000000
    else:
        return math.log(x)

def viterbi(a):
    L=len(a)
    ops=[]
    for k in range(L):
        s=str.rstrip(a[k])
        ops.append(s)
    
    V=[]
    pi=[-1 for i in range(L)]
    ptr=[]
    vec=[]
#inicijalizacija
    for l in range(3*d+3):
        vec.append(mylog(0))
    for i in range(L+1):
        V.append(vec[:])
    V[0][0]=mylog(1)
    for i in range(L):
        V[i][0]=mylog(0)
    
#rekurzija    
    for i in range(1,L):
        for l in range(1,d):
                if stanja[l]==1:#insert
                    niz=[V[i-1][l+k]*mylog(T[l][j][1]) for j in range(0,3)]
                    maks=max(niz)
                    V[i][l]=mylog(Ie[l][ak.index(ops[i])]/Ie[i][ak.index(ops[i])])+maks

                elif k==0:#match
                    niz=[V[i-1][l+k-1]*mylog(T[l][k][0]) for k in range(0,3)]
                    maks=max(niz)
                    V[i][l]=mylog(Me[l][ak.index(ops[i])]/Ie[i][ak.index(ops[i])])+maks

                elif k==2:#delete
                    niz=[V[i][l+k-1]*mylog(T[(l-l%3)/3][k][2]) for k in range(0,3)]
                    V[i][l]=max(niz)        
    put=[]
    for i in range(n):
        for k in range(3):
            if(V[L][i+k]+mylog(T[i][k][0])==V[L][-1]):
                y=i
                put.append(y)
#traceback
    print put
viterbi(['H','P','E','W'])







    
