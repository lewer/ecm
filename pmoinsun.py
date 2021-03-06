# -*- coding: utf-8 -*-
# pmoinsun.py
import utils
import math
import fractions


def un_facteur(n, b1=10**6, phase2=True, b2=5*10**8, k=3):
    """
    Renvoie un facteur de n avec la méthode p-1

    """

    if utils.AMR(n, k):
        # n probablement premier
        return n

    b = 2
    primes_up_to_bound = utils.primes_from_file(1, b1)
    for p in primes_up_to_bound:
        q = utils.valuation(b1, p)
        b = pow(b, q, n)
        g = fractions.gcd(b-1, n)
        if g > 1:
            break

    if g == 1:
        if not phase2:
            raise Exception('Aucun facteur calculé : il faut augmenter B1 ou faire la phase 2')

        # Phase 2, continuation standard
        # On tabule b^i mod n pour i <= log(b2)^2
        c = [pow(b, i, n) for i in range(int(math.log(b2)**2) + 1)]

        primes = utils.primes_from_file(b1, b2)  # nombres premiers entre b1 et b2
        s1 = primes.next()
        t = pow(b, s1, n)  # t va itérativement contenir b^s pour tous les s premiers, b1 <= s <= b2
        for s2 in primes:
            pgcd = fractions.gcd(t - 1, n)
            if pgcd > 1:
                return pgcd

            t = (t*c[s2 - s1]) % n  # s1, s2 = primes[i], primes[i+1]
            s1 = s2

        pgcd = fractions.gcd(t, n)
        if pgcd == 1:
            raise Exception('Aucun facteur trouvé après la phase 2')

    elif g == n:
        raise Exception('Aucun facteur calculé : Il faut réduire b1')
    else:
        return g


def factorise(N, k=3, b1=10**6):
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
        d = un_facteur(N, b1)
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
