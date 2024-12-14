import backwork.direction as direct


def leftPoint(points: tuple[tuple[float, float]])-> tuple[float, float]:
    n = points[0];
    for i in points:
        if i[0]<n[0]:
            n = i
    return n;


def jarvis(points: tuple[tuple[float, float]])-> tuple[tuple[float, float]]:
    ret:list[tuple[float, float]] = [None for _ in points];
    n = 0
    L = leftPoint(points);
    P = L;
    while (P!=L) | (n==0):
        ret[n] = P;
        Q = points[(n+1)%len(points)];
        Vq = direct.vector(P,Q);
        for i in points:
            Vi = direct.vector(P, i)
            if direct.side(Vq, Vi)<0:
                Vq = Vi;
                Q = i;
        P = Q;
        n+=1;
    return tuple(ret[:n])