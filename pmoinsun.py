# -*- coding: utf-8 -*-
import utils


def un_facteur(n):
    """
    Renvoie un facteur de n avec la méthode p-1

    """

    b = 2
    bound = 10**7
    primes_up_to_bound = utils.compute_prime_numbers_up_to(bound)
    for p in primes_up_to_bound:
        q = utils.valuation(bound, p)
        b = pow(b, q, n)
        g = utils.XGCD(b-1, n)[0]
        if g > 1:
            break

    if g == 1:
        print 'g=1'
        raise Exception('Aucun facteur calculé : B1 trop petit')
    elif g == n:
        print 'g=n'
        raise Exception('Aucun facteur calculé : B1 trop grand')
    else:
        return g


def factorise(N, k=3):
    """
    Factorise un entier avec la méthode un_facteur

    :Parameters:
        -`N`: L'entier à factoriser
        -`k`: le nombre de fois qu'on lance AMR pour déterminer si un entier est premier

    :return:
        La liste des facteurs de N

    """

    try:
        d = un_facteur(N)
    except:
        return [N]

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
