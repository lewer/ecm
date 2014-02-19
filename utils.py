# -*- coding: utf-8 -*-

"""Fonctions arithmétiques utilisées pour la factorisation des entiers

"""

import os.path
import random

def AMR(n, k = 3) :
    """
    Test Miller-Rabin pour déterminer si un entier est premier
    
    :Parameters:
        -`n` : l'entier dont on veut savoir s'il est premier
        -`k` : le nombre de fois qu'on lance le test
        
    :return:
        False : n est un nombre composé
        True : n est probablement un nombre premier (mais n peut être composé)
    
    """
    
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

def compute_prime_numbers_up_to (n): 
    """
    Écrit dans le fichier nbrpremiers.txt les n premiers nombres premiers
    
    """
    
    with open('nbrpremiers.txt','w') as nbrpremiers:
        eratho = (n+1)*range(1)
        for i in range(2,n+1) :
            if eratho[i] == 0 : 
                if(i==2):nbrpremiers.write("2") #disjonction de cas pour le saut de ligne
                if(i!=2):nbrpremiers.write("\n%i" %i)             
                for j in range(n/i) :
                    eratho[(j+1)*i]=1

def diviseurs_triviaux (n) :
    """
    Renvoie la liste des petits diviseurs de n
    
    """
    
    if not os.path.isfile('nbrpremiers.txt'):
        #Si le fichier n'existe pas, on le créé
        compute_prime_numbers_up_to(10**6)
        
    nbrpremiers = open('nbrpremiers.txt','r')
    lignes = nbrpremiers.readlines()
    reponse=[]
    for ligne in lignes :
        i = int(ligne)
        if n%i == 0 :
            g = n
            while g %i ==0:
                reponse = reponse +[i]
                g = g/i
    return reponse

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

if __name__ == "__main__":
    print "Running doctest..."
    import doctest
    doctest.testmod( )

