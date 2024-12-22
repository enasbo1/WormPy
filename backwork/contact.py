from backwork.direction import*

def hitbox(zone1, zone2):
    if zone1[0]=='rect':
        if zone2[0]=='rect':
            X1=zone1[1]
            Y1=zone1[2]
            Xx1=zone1[3]
            Yy1=zone1[4]
            X2=zone2[1]
            Y2=zone2[2]
            Xx2=zone2[3]
            Yy2=zone2[4]
            ret=False
            if X2<=X1<=Xx2 or X1<=X2<=Xx1:
                if Y2<=Y1<=Yy2 or Y1<=Y2<=Yy1:
                    ret=True
    if zone1[0]=='rect':
        if zone2[0]=='circle':
            X1=zone1[1]
            Y1=zone1[2]
            Xx1=zone1[3]
            Yy1=zone1[4]
            X2=zone2[1]
            Y2=zone2[2]
            R=zone2[3]
            ret= X1<X2<=Xx1 and Y1<Y2<=Yy1
            if X1<X2<Xx1:
                ret= ret or abs(Y2-Y1)<R or abs(Y2-Yy1)<R
            elif Y1<Y2<Yy1:
                ret= ret or abs(X2-X1)<R or abs(X2-Xx1)<R
            else:
                R=R**2
                ret= ret or disrap(X1, Y1, X2, Y2)<R or disrap(X1, Yy1, X2, Y2)<R or disrap(Xx1, Y1, X2, Y2)<R or disrap(Xx1, Yy1, X2, Y2)<R
    
    if zone1[0]=='rect':
        if zone2[0]=='point':
            X1=zone1[1]
            Y1=zone1[2]
            Xx1=zone1[3]
            Yy1=zone1[4]
            X2=zone2[1]
            Y2=zone2[2]
            ret= X1<X2<=Xx1 and Y1<Y2<=Yy1
    
    if zone2[0]=='rect':
        if zone1[0]=='point':
            X1=zone2[1]
            Y1=zone2[2]
            Xx1=zone2[3]
            Yy1=zone2[4]
            X2=zone1[1]
            Y2=zone1[2]
            ret= X1<X2<=Xx1 and Y1<Y2<=Yy1
        
    if zone1[0]=='circle':
        if zone2[0]=='rect':
            X1=zone2[1]
            Y1=zone2[2]
            Xx1=zone2[3]
            Yy1=zone2[4]
            X2=zone1[1]
            Y2=zone1[2]
            R=zone1[3]
            ret= X1<=X2<=Xx1 and Y1<=Y2<=Yy1
            if X1<=X2<=Xx1:
                ret= ret or abs(Y2-Y1)<R or abs(Y2-Yy1)<R
            elif Y1<=Y2<=Yy1:
                ret= ret or abs(X2-X1)<R or abs(X2-Xx1)<R
            else:
                R=R**2
                ret= ret or disrap(X1, Y1, X2, Y2)<=R or disrap(X1, Yy1, X2, Y2)<R or disrap(Xx1, Y1, X2, Y2)<=R or disrap(Xx1, Yy1, X2, Y2)<=R
    
    if zone1[0]=='circle':
        if zone2[0]=='circle':
            ret=disrap(zone1[1], zone1[2], zone2[1], zone2[2])<=(zone1[3]+zone2[3])**2

    return(ret)

def cross(A:tuple[float, float], B:tuple[float, float], C:tuple[float, float], D:tuple[float, float])->None|float:
    AB = vector(A, B);
    AC = vector(A, C);
    DC = vector(D, C);
    det = AB[0]*DC[1]-AB[1]*DC[0];

    if det==0:
        return None;
    t = (AC[0]*DC[1]-AC[1]*DC[0])/det

    if not(0<=t<1):
        return None;

    u = (AC[1]*AB[0]-AC[0]*AB[1])/det
    if 0<=u<1:
        return t;

def in_test_segment(P:tuple[float, float], A:tuple[float, float], B:tuple[float, float])->int|None:
    Ph = (0.,1.);
    PA = vector(P, A);
    BA = vector(B, A);
    det = Ph[0]*BA[1]-Ph[1]*BA[0];

    if det==0:
        return 0;
    t = (PA[0]*BA[1]-PA[1]*BA[0])/det

    if not(0<=t):
        return 0;

    u = (PA[1]*Ph[0]-PA[0]*Ph[1])/det
    if u == 0:
        print("so hi: ", end='');
        return None;
    if 0<u<1:
        return 1;
    return 0;

def seg_in_circle(circle:tuple[float, float, float], A:tuple[float, float], B:tuple[float, float])->None|float:
    r = circle[2]**2;
    center = (circle[0], circle[1]);

    AB = vector(A, B);
    BA = vector(B, A);
    scal = scalar(BA, vector(B, center));
    if scal > 0:
        scal = scalar(AB, vector(B, center));
        if scal > 0:
            fact = scal/norme2(AB)
            di = norme2(vector(center, (A[0]+(fact*AB[0]),A[1]+(fact*AB[1]))))
            if di<r:
                return fact;
        else:
            di = norme2(vector(center, A));
            if di<r:
                return 0.;
    else:
        di = norme2(vector(center, B))
        if di<r:
            return 1;

    return None;

def outBorderIn(circle:tuple[float, float, float], A:tuple[float, float], B:tuple[float, float])->int:
    """
        test si un segment AB est dans un cercle circle, renvoie 2 si il est entèrement dedant, 1 si partiellement et 0 sinon
    """
    r = circle[2]**2;
    center = (circle[0], circle[1]);
    ret = 0
    di = norme2(vector(center, A));
    if di<r:
        ret = 1
    di = norme2(vector(center, B))
    if di<r:
        ret += 1;
    if ret==2:
        return 2;
    if ret==1:
        return 1;

    AB = vector(A, B);
    BA = vector(B, A);
    scal = scalar(BA, vector(B, center));
    if scal > 0:
        scal = scalar(AB, vector(B, center));
        if scal > 0:
            fact = scal/norme2(AB)
            di = norme2(vector(center, (A[0]+(fact*AB[0]),A[1]+(fact*AB[1]))))
            if di<r:
                return 1;
    return 0;