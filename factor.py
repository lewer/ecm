#!/usr/bin/python
# factor.py
# Basic factorization algorithms
#  * Pollard's Rho algorithm (for factoring)
#  * Pollard's p-1 algorithm
#
# author: Gabriel Lewertowski
# date: 14/02/14

import fractions
import random

def AMR(n, k = 3) :
    if n % 2 == 0 :
        return False
    
    d, s = n-1, 0
    while (d % 2 == 0):
        d, s = d/2, s+1

    def WitnessLoop():
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if (x == 1 or x == n - 1):
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
    
    return True #n est probablement premier
        
                
    
def Pollard_rho(N,f = lambda x, m : (x*x +1) % m):
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

def FactorPollard(N, k=3):
    try:
        d = Pollard_rho(N)
    except:
        return [N]

    facteurs = []
    if AMR(d, k):
        facteurs += [d]
    else:
        facteurs += FactorPollard(d)

    if AMR(N/d, k):
        facteurs += [N/d]
    else:
        facteurs += FactorPollard(N/d)
        
    return facteurs

def Pollard_pminusone(N,B1=None,B2=None):
    """
    Computes a non-trivial factor of the integer N
    (presumed composite) using Pollard's p-1 algorithm.
    B1 and B2 (optional) are the bounds for phase one and two.
    """
    # your code goes here...

    # if the algorithm fails:
    raise Exception("could not compute factor")


