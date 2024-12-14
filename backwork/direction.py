from math import*

from numpy import flatiter


def tourne(ditem, direction, vitesse):
    if abs(ditem-direction)>pi:
        if rot(-ditem, direction)>0:
            ditem=rot(vitesse,ditem)
        else:
            ditem=rot(-vitesse,ditem)
    elif  abs(ditem-direction)>vitesse:
        if ditem<direction:
            ditem=rot(vitesse,ditem)
        else:
            ditem=rot(-vitesse,ditem)
    else:
        ditem=direction
    return(ditem)

def avix(a,d):
    x=cos(d)*a
    return(x)

def aviy(a,d):
    x=sin(d)*a
    return(x)

def dis(a,b,x,y):
    x1=x-a
    y1=y-b
    n=sqrt(y1**2+x1**2)
    return(n)

def disrap(a,b,x,y):
    x1=x-a
    y1=y-b
    n=y1**2+x1**2
    return(n)

def rot(r,d):
    d+=r
    if d>pi:
        d=d-(2*pi)
    if d<-pi:
        d=d+(2*pi)
    return(d)

def dir(a,b,d,x,y):
    x1=x-a
    y1=y-b
    L=0
    d=-d
    if x1>0:
        if y1>=0:
            L=atan(y1/x1)
        else:
            L=atan(y1/x1)
    elif x1<0:
        if y1>=0:
            L=atan(y1/x1)+pi
        else:
            L=atan(y1/x1)+pi
    else:
        if y1<0:
            L=-pi/2
        else:
            L=pi/2
    L=rot(d,L)
    return(L)

def lim(x,x1,y,y1,a,b,d):
    if b<y or b>y1:
        d=-d
    if a<x:
        d=-d-pi
    if a>x1:
        d=-d+pi
    return(d)

def limxy(a,b,x,x1,y,y1):
    while a<x:
        a=x+5
    while a>x1:
        a=x1-5
    while b<y:
        b=y+5
    while b>y1:
        b=y1-5
    return(a,b)

def scalar(v1:tuple[float, float], v2:tuple[float, float])->float:
    return v1[0]*v2[0]+v1[1]*v2[1];

# positif si v2 à droite de v1)
def side(v1:tuple[float, float], v2:tuple[float, float])->float:
    return v1[1]*v2[0]-v1[0]*v2[1];

def rotate(v:tuple[float, float])->tuple[float, float]:
    return -v[1], v[0]

def change_ref(x:float,y:float, coords:tuple[tuple[float, float]])->tuple[tuple[float, float]]:
    return tuple([tuple([i[0]+x, i[1]+y]) for i in coords])

def vector(a:tuple[float,float], b:tuple[float,float])->tuple[float, float]:
    return b[0]-a[0],b[1]-a[1]

def sum_vectors(a:tuple[float,float], b:tuple[float,float])->tuple[float, float]:
    return a[0]+b[0],a[1]+b[1]

def multiply_vector(a:tuple[float,float], fact:float)->tuple[float, float]:
    return a[0]*fact,a[1]*fact

def moy_vector(a:tuple[float,float], b:tuple[float,float]):
    return (a[0]+b[0])/2,(a[1]+b[1])/2

def norme2(a:tuple[float,float]):
    return (a[0]**2) + (a[1]**2)

def norme(a:tuple[float,float]):
    return sqrt((a[0]**2) + (a[1]**2))

def unit_vect(a:tuple[float,float]):
    n = norme(a);
    return a[0] / n, a[1] / n