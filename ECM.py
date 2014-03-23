# -*- coding: utf-8 -*-
# ECM.py

import random
import utils
import fractions


def un_facteur(n, B1=10**6, nb_essais=1, phase2=True, B2=5*10**8):
    """
    Calcule un facteur de n avec la méthode ECM.
    k est le nombre d'essais.

    """
    for i in range(nb_essais):
        if(n % 2 == 0):
            return 2
        delta = n
        while (delta == n):
            x0 = random.randint(0, n-1)
            y0 = random.randint(0, n-1)
            a = random.randint(0, n-1)
            b = ((y0**2) - (x0**3) - a * x0) % n
            delta = fractions.gcd(4*a**3 + 27*b**2, n)
        if(delta != 1):
            return delta
        P = (x0, y0)
        d = (utils.XGCD(4, n)[1]) % n
        d = (d * (a+2)) % n
        for k in utils.primes_from_file(1, B1):
            u = k
            while(u <= B1):
                u = u*k
                P = ECM_mult(P, k, d, n)
                g = fractions.gcd(n, P[1])
                if(g != 1):
                    return g

        if phase2:
            for p in utils.primes_from_file(B1, B2):
                P = ECM_mult(P, p, d, n)
                g = fractions.gcd(P[1], n)
                if g > 1:
                    return g

    raise Exception('Aucun facteur trouvé')


def ECM_mult((x, z), k, d, n):
    """
    Multiplication rapide sur une courbe elliptique

    :Parameters:
     -`(x, z)`: un point de la courbe
     -`k`: un entier
     -`d`: l'inverse de 4 mod n
     -`n`: la caractéristique de l'anneau sur lequel la courbe est définie
    :return:
     - k.P

     """

    xp = 1
    xq = x
    zp = 0
    zq = z

    i = k.bit_length()
    for l in range(i):

        # regarde si le i-l eme bit de k est un 0 ou un 1
        f = (k >> (i-1-l))-((k >> (i-l)) << 1)
        if(f == 0):
            xv = (pow((xp+zp), 2, n)*pow((xp-zp), 2, n)) % n
            zv = ((4*xp*zp)*(pow((xp-zp), 2, n)+d*4*xp*zp)) % n
            xw = (z*pow((xq-zq)*(xp+zp)+(xq+zq)*(xp-zp), 2, n)) % n
            zw = (x*pow((xq-zq)*(xp+zp)-(xq+zq)*(xp-zp), 2, n)) % n

        if(f == 1):
            xv = (z*pow((xq-zq)*(xp+zp)+(xq+zq)*(xp-zp), 2, n)) % n
            zv = (x*pow((xq-zq)*(xp+zp)-(xq+zq)*(xp-zp), 2, n)) % n
            xw = (pow((xq+zq), 2, n)*pow((xq-zq), 2, n)) % n
            zw = ((4*xq*zq)*(pow((xq-zq), 2, n)+d*4*xq*zq)) % n

        xp = xv
        zp = zv
        xq = xw
        zq = zw
    return (xp, zp)


def factorise(N, k=3, nb_essais=1, B1=10**6, B2=10**8, phase2=True):
    """
    Factorise un entier avec la méthode un_facteur

    :Parame)ers:
        -`N`: L'entier à factoriser
        -`k`: le nombre de fois qu'on lance AMR pour déterminer si un entier est premier

    :return:
        un couple de listes l, m, où:
            l sont des facteurs premiers de N
            m sont des facteurs de N que l'algorithme n'a pas su factoriser

    """

    # On factorise les entiers <= avec la méthode naïve
    if N <= 1000:
        return utils.naive_factoring(N), []

    try:
        d = un_facteur(N, B1, nb_essais, phase2, B2)
    except:
        return [], [N]

    if d == N:
        return [d], []

    facteurs, non_factorise = [], []
    if utils.AMR(d, k):
        facteurs.append(d)
    else:
        a, b = factorise(d)
        facteurs += a
        non_factorise += b

    if utils.AMR(N/d, k):
        facteurs.append(N/d)
    else:
        a, b = factorise(N/d)
        facteurs += a
        non_factorise += b

    return facteurs, non_factorise
