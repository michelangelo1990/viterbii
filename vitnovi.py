import math
import sys

f=open("model_test001.txt", "r")
##ucitavamo duljinu modela
dmod=int(f.readline())

def make_float(v):
    for i in range(len(v)):
        v[i]=float(v[i])
        
def mmake_float(v):
    for i in range(len(v)):
        for j in range(len(v[i])):
            v[i][j]=float(v[i][j])


T=[]
Me=[]
Ie=[]

for i in range(3*dmod+3):
    pom=[]
##oznacava da citam tranzicijsku matricu
    if i%3==0:
        for j in range(3):
            line=f.readline()
            if not line.strip():
                line=f.readline()
            ls=line.split()
            pom.append(ls[:])
        mmake_float(pom)
        T.append(pom)
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
put=dict()
def viterbi(a):
    L=len(a)
    x=[]
    for k in range(L):
        s=str.rstrip(a[k])
        x.append(s)

    VM=[[mylog(0) for i in range(dmod+2)] for j in range(L)]
    VI=[[mylog(0) for i in range(dmod+2)] for j in range(L)]
    VD=[[mylog(0) for i in range(dmod+2)] for j in range(L)]
    VM[0][0]=0
    
    for i in range(1,L):
        razina=0
        for st in range((dmod)*3):
            j=(st)%3
            if j==0:
                m=max(zip([VM[i-1][razina-1]+mylog(T[razina][0][0]),
                           VI[i-1][razina-1]+mylog(T[razina][1][0]),
                           VD[i-1][razina-1]+mylog(T[razina][2][0])],[0,1,2]))
                VM[i][razina]=m[0]+mylog(Me[razina][ak.index(x[i])])
                put[(st,i)]=(razina-1,m[1])
                
            elif j==1:
                m=max(zip([VM[i-1][razina]+mylog(T[razina][0][1]),
                           VI[i-1][razina]+mylog(T[razina][1][1]),
                           VD[i-1][razina]+mylog(T[razina][2][1])],[0,1,2]))
                VI[i][razina]=m[0]+mylog(Ie[razina][ak.index(x[i])])
                put[(st,i)]=(razina,m[1])
                razina+=1;
            elif j==2:
                m=max(zip([VM[i][razina-1]+mylog(T[razina][0][2]),
                      VI[i][razina-1]+mylog(T[razina][1][2]),
                      VD[i][razina-1]+mylog(T[razina][2][2])],[0,1,2]))
                VD[i][razina]=m[0]
                put[(st,i)]=(razina-1,m[1])
                
    p=math.exp(max(VM[L-1][:]))
    return put,p

vv=viterbi(['H','P','E','W'])
























    

