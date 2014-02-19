# -*- coding: utf-8 -*-
# arith.py
# author: Gabriel Lewertowski, Stephane Horte
# date: 07/02/14
#
# A range of number-theoretic algorithms.
# Compatible with the doctest module.

import fractions
from utils import *

def un_facteur(N,f = lambda x, m : (x*x +1) % m):
    """
    Computes a non-trivial factor of the integer N
    (presumed composite) using the Pollard rho algorithm.
    The second argument, f, is a pseudo-random function modulo N.
    """
    
    x, y, g = 1, 1 ,1
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
        La liste des facteurs de N
        
    """
    
    try:
        d = un_facteur(N) 
    except: #Pollard_rho lance une exception s'il n'a pas pu calculer de facteur de N
        return [N]

    facteurs = []
    if AMR(d, k):
        facteurs += [d]
    else:
        facteurs += factorise(d)

    if AMR(N/d, k):
        facteurs += [N/d]
    else:
        facteurs += factorise(N/d)
        
    return facteurs
