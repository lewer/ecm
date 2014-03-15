# -*- coding: utf-8 -*-
# arith.py
# author: Gabriel Lewertowski, Stephane Horte
# -*- coding: utf-8 -*-
import fractions
import utils


def un_facteur(N, f=lambda x, m: (x*x + 1) % m, k=3):
    """
    Computes a non-trivial factor of the integer N
    (presumed composite) using the Pollard rho algorithm.
    The second argument, f, is a pseudo-random function modulo N.
    """

    if utils.AMR(N, k):
        # N est probablement premier
        return N

    x, y, g = 1, 1, 1
    while (g == 1):
        x, y = f(x, N), f(f(y, N), N)
        g = fractions.gcd(x - y, N)

    if (g == N):
        # if the algorithm fails:
        raise Exception("could not compute factor")
    else:
        return g


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
