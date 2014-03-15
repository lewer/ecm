# -*- coding: utf-8 -*-
# author: Gabriel Lewertowski, Stephane Horte

import random
import utils
import fractions


def un_facteur(n, B1=10**6, k=1, phase2=True, B2=5*10**8):
    """
    Calcule un facteur de n avec la méthode ECM.
    k est le nombre d'essais.

    """
    for i in range(k):
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


def factorise(N, k=3):
    """
    Factorise un entier avec la méthode un_facteur

    :Parame)ers:
        -`N`: L'entier à factoriser
        -`k`: le nombre de fois qu'on lance AMR pour déterminer si un entier est premier

    :return:
        La liste des facteurs de N

    """

    # On factorise les entiers <= 1000 avec une méthode naïve
    if N <= 1000:
        return utils.naive_factoring(N)

    try:
        d = un_facteur(N)
    except:  # Pollard_rho lance une exception s'il n'a pas pu calculer de facteur de N
        raise Exception("Impossible de factorier l'entier")

    if d == N:
        return [d]

    facteurs = []
    if utils.AMR(d, k):
        facteurs += [d]
    else:
        facteurs += factorise(d)

    if utils.AMR(N/d, k):
        facteurs += [N/d]
    else:
        facteurs += factorise(N/d)

    return facteurs
