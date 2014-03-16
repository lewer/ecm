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

    :Parameters:
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
        d = un_facteur(N)
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
