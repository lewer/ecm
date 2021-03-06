# -*- coding: utf-8 -*-
# utils.py

"""Fonctions arithmétiques utilisées pour la factorisation des entiers

"""

import random
import math


def AMR(n, k=3):
    """
    Test Miller-Rabin pour déterminer si un entier est premier

    :Parameters:
        -`n` : l'entier dont on veut savoir s'il est premier
        -`k` : le nombre de fois qu'on lance le test

    :return:
        False : n est un nombre composé
        True : n est probablement un nombre premier (mais n peut être composé)

    """

    if (n % 2 == 0):
        return False

    if (n == 3):
        return True

    d, s = n-1, 0
    while (d % 2 == 0):
        d, s = d/2, s+1

    def WitnessLoop():
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if (x == 1 or x == n-1):
            return True
        for j in range(s-1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n-1:
                return True
        return False

    for i in range(k):
        if not WitnessLoop():
            return False

    return True  # n est probablement premier


def eratho(n):
    """
    Renvoie les nombres premiers plus petits que n.

    Cette fonction stocke en mémoire une liste de taille n. Il faut donc n pas
    trop grand (n <= 10**7). Pour n > 10**7, on utilise big_eratho.
    """

    result = []
    eratho = (n+1)*range(1)
    for i in range(2, n+1):
        if eratho[i] == 0:
            result.append(i)
            for j in range(n/i):
                eratho[(j+1)*i] = 1

    return result


def segmented_eratho(l, r):
    """
    Renvoie les nombres premiers p tels que l <= p <= r

    http://programmingpraxis.com/2010/02/05/segmented-sieve-of-eratosthenes/

    Cette fonction stocke en mémoire une liste de taille (r-l)/2.
    Si (r-l)/2 > 10^7, on utilisera big_segmented_eratho.

    """

    # On se ramène au cas où l et r sont impairs
    if l % 2 == 0:
        l += 1

    if r % 2 == 0:
        r -= 1

    primes = eratho(int(math.sqrt(r)))[1:]  # on enlève 2
    q = [(-(l+p)/2) % p for p in primes]
    table = ((r-l)/2 + 1)*[True]
    for i, p in enumerate(primes):
        for j in range(q[i], ((r-l)/2 + 1), p):
            table[j] = False

    return [l+2*i for (i, b) in enumerate(table) if b]


def big_eratho(n):
    """
    Renvoie les nombres premiers inférieurs ou égaux à n.

    """

    chunksize = 10**7
    nb_chunks = (n-1)/chunksize + 1
    primes = eratho(chunksize)

    for i in range(nb_chunks):
        for j in range(len(primes)):
            yield primes[j]

        primes = segmented_eratho((i+1)*chunksize + 1, (i+2)*chunksize)


def big_segmented_eratho(l, r):
    """
    Renvoie les nombres premiers inférieurs ou égaux à n.

    """

    chunksize = 10**7
    nb_chunks = (r-l-1)/chunksize + 1
    primes = segmented_eratho(l, l+chunksize)

    for i in range(nb_chunks):
        for j, p in enumerate(primes):
            yield primes[j]

        primes = segmented_eratho((i+1)*chunksize + l + 1, (i+2)*chunksize + l)


def diviseurs_triviaux(n):
    """
    Renvoie la liste des petits diviseurs de n

    """

    nbrpremiers = eratho(10**6)
    result = []
    for p in nbrpremiers:
        if n % p == 0:
            g = n
            while g % p == 0:
                result.append(p)
                g = g/p
    return result


def XGCD(a, b):
    """
    L'algrithme d'Euclide étendu.
    Étant donné deux entiers a et b, calcule g = PGCD(a, b) et renvoie
    (g, x, y) tel que ax + by = g

    >>> XGCD(18,33)
    (3, 2, -1)
    >>> XGCD(15,7)
    (1, 1, -2)
    >>> XGCD(12388542345128376123,981723987132541230)
    (3, -23206105513321299L, 292841801346842686L)
    """

    x, y = a, b
    u1, v1 = 1, 0
    u2, v2 = 0, 1
    while y > 0:
        q = x/y
        x, y = y, x % y
        u2, u1 = u1 - q*u2, u2
        v2, v1 = v1 - q*v2, v2

    return (x, u1, v1)


def valuation(b, p):
    """"
    Renvoie p^k tel que p^k <= b < p^(k+1)

    """

    assert(p > 0)
    assert(b > 0)
    result = p
    while (result*p < b):
        result *= p

    return result


def decimales_pi(n, offset=0):
    """
    Renvoie n décimales de pi en partant de la offset-ième

    """

    with open('pi.txt') as f:
        f.seek(offset)
        return int(f.read(n))


def naive_factoring(n):
    """
    Factorise n en le divisant par les nombres premiers inférieurs à sqrt(n)

    """

    result = []
    for p in eratho(n/2):
        if n % p == 0:
            q = p
            while (n % q == 0):
                result.append(p)
                q *= p

    return result


def write_primes_up_to(n):
    """
    Enregistre dans le fichiers nbrpremiers.txt les nombres premiers
    inférieurs à n

    """

    with open('nbrpremiers.txt', 'w') as f:
        for p in big_eratho(n):
            f.write(str(p) + '\n')


def primes_from_file(l, r):
    """
    Renvoie les nombres premiers p tels que l <= p <= r lus depuis un fichier

    """

    with open('nbrpremiers.txt', 'r') as f:
        p = int(f.readline())
        while p < l:
            p = int(f.readline())

        while p <= r:
            yield p
            p = int(f.readline())
