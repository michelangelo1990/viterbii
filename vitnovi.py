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
        return -100000000000000
    else:
        return math.log(x)

put=dict()

def vrati_put(p,k,l):
    if k==0 and l==0:
        return [0]
    prije=p[(k,l)]
    vp=vrati_put(p,prije[0],prije[1])
    vp.append(k)
    return vp

def viterbi(a):
    L=len(a)
    x=[]
    for k in range(L):
        s=str.rstrip(a[k])
        x.append(s)

    VM=[[mylog(0) for i in range(dmod+2)] for j in range(L+1)]
    VI=[[mylog(0) for i in range(dmod+1)] for j in range(L+1)]
    VD=[[mylog(0) for i in range(dmod+1)] for j in range(L+1)]
    VM[0][0]=0
    
    
    for st in range(1,(dmod+1)*3+1):
        for i in range(1,L+1):
            j=(st)%3
            razina=st/3
            if razina==dmod+1:
                m=max(zip([VM[i][razina-1]+mylog(T[razina-1][0][0]),
                           VI[i][razina-1]+mylog(T[razina-1][1][0]),
                           VD[i][razina-1]+mylog(T[razina-1][2][0])],[0,1,2]))
                VM[i][razina]=m[0]
                if VM[i][razina]<-100000000000000:
                    VM[i][razina]=-100000000000000
                put[(st,i)]=((razina-1)*3+m[1],i)

            elif j==0:   
                m=max(zip([VM[i-1][razina-1]+mylog(T[razina][0][0]),
                           VI[i-1][razina-1]+mylog(T[razina][1][0]),
                           VD[i-1][razina-1]+mylog(T[razina][2][0])],[0,1,2]))
                VM[i][razina]=m[0]+mylog(Me[razina][ak.index(x[i-1])])
                if VM[i][razina]<-100000000000000:
                    VM[i][razina]=-100000000000000
                put[(st,i)]=((razina-1)*3+m[1],i-1)
                print "stanje %d,%d= %f" %(st,i,VM[i][razina])
            elif j==1:
                m=max(zip([VM[i-1][razina]+mylog(T[razina][0][1]),
                           VI[i-1][razina]+mylog(T[razina][1][1]),
                           VD[i-1][razina]+mylog(T[razina][2][1])],[0,1,2]))
                VI[i][razina]=m[0]+mylog(Ie[razina][ak.index(x[i-1])])
                if VI[i][razina]<-100000000000000:
                    VI[i][razina]=-100000000000000
                put[(st,i)]=(razina*3+m[1],i-1)
                print "stanje %d,%d= %f" %(st,i,VI[i][razina]) 
            elif j==2:
                m=max(zip([VM[i][razina-1]+mylog(T[razina][0][2]),
                      VI[i][razina-1]+mylog(T[razina][1][2]),
                      VD[i][razina-1]+mylog(T[razina][2][2])],[0,1,2]))
                VD[i][razina]=m[0]
                if m[0]<-100000000000000:
                    VD[i][razina]=-100000000000000
                put[(st,i)]=((razina-1)*3+m[1],i)
                print "stanje %d,%d= %f" %(st,i,VD[i][razina])
    p=math.exp(VM[L][dmod+1])
    return vrati_put(put,(dmod+1)*3,L),p

vv=viterbi(['H','P','E','W'])






















    

