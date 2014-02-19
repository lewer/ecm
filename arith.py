# arith.py
# author: Gabriel Lewertowski, Stéphane Horte
# date: 07/02/14
#
# A range of number-theoretic algorithms.
# Compatible with the doctest module.

import random
import fractions

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
        d = Pollard_rho(N) # utilise methode de Monte Carlo
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

def primes_up_to(bound):
    """
    Lists the primes p less than or equal to the bound.
    
    >>> primes_up_to(50) 
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    """
    
    marked = set()
    primes = []
    lowest_unmarked = 2

    while bound not in marked:
        primes.append(lowest_unmarked)
        for k in xrange(1, bound/lowest_unmarked):
            marked.add(k*lowest_unmarked)
        print marked
        while lowest_unmarked in marked:
            lowest_unmarked += 1
        
    return primes

def ecrirenombrepremier (n): 
    
    nbrpremiers = open('nbrpremiers.txt','w')    
    eratho = (n+1)*range(1)
    for i in range(2,n+1) :
        if eratho[i] == 0 : 
            if(i==2):nbrpremiers.write("2") #disjonction de cas pour le saut de ligne
            if(i!=2):nbrpremiers.write("\n%i" %i)             
            for j in range(n/i) :
                eratho[(j+1)*i]=1

def trial_division(N,bound):
    """
    Given an integer N, returns a list S of tuples in the form (p,e),
    where each p is a prime less than bound and e is an exponent such that
    p**e divides N.  Also returns the (unfactored) cofactor M
    such that N is the product of M with the prime powers specified by S.

    >>> N = 29145271819831067830349386007355751792690423602074265137925000
    >>> trial_division(N,100)
    ([(2, 3), (3, 6), (5, 5), (17, 3), (31, 2), (41, 6)], 71306198031317215975086685276791653621L)
    >>> trial_division(1,100)
    ([], 1)
    """
    # your code goes here...

    pass  # remove this line when done


def XGCD(a,b):
    """
    The extended Euclidean algorithm:
    Given integers a and b, returns x, y, and g = GCD(a,b)
    such that ax + by = g .

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
        q=x/y
        x, y = y, x%y 
        u2, u1 = u1 - q*u2, u2 
        v2, v1 = v1 - q*v2, v2
    
    return (x, u1, v1)

def CRT(S):
    """
    Given a list S of pairs (r,m), returns an integer n such that
    n mod m = r for each (r,m) in S.  If no such n exists, then this
    function returns -1.  The moduli m must all be positive.

    >>> CRT([(1,7),(2,11),(3,13),(4,15),(5,17)])
    18229
    >>> CRT([(1,3),(2,6)]) 
    -1
    """
    # your code goes here...

    pass # remove this line when done


def Jacobi_symbol(a,b):
    """
    Computes the Jacobi Symbol (a/b) of integers a and b,
    where b is positive and odd.

    >>> Jacobi_symbol(129837123,98732498234134187123)
    -1
    >>> Jacobi_symbol(1231928323,98732498234134187123)
    1
    """
    if (b < 0) or ((b % 2) == 0):
        raise RuntimeError("Second argument of Jacobi_symbol must be positive and odd")

    # your code goes here...

    pass # remove this line when done



def is_probable_prime(N,nbases=20):
    """
    True if N is a strong pseudoprime for nbases random bases b < N.
    Uses the Miller--Rabin primality test.

    >>> is_probable_prime(13)
    True
    >>> is_probable_prime(1293871928371928739182731111)
    False
    >>> is_probable_prime(1267650600228229401496703205653)
    True
    """
    # Use the Miller-Rabin primality test
    # your code goes here...

    pass # remove this line when done



def random_probable_prime(bits):
    """
    Returns a probable prime number with the given number of bits.
    """
    # your code goes here...

    pass # remove this line when done


# If this module is run as a script, then the following code will
# check the examples given in the docstrings for each function.
if __name__ == "__main__":
    print "Running doctest..."
    import doctest
    doctest.testmod( )
