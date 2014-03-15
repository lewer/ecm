# -*- coding: utf-8 -*-
# arith.py
# author: Gabriel Lewertowski, Stephane Horte
# -*- coding: utf-8 -*-

import random
import utils

def etapeunECM (n,B1) :
    if(n%2==0) : return 2
    delta = n
    while (delta == n) :
        x0 = random.randint(0,n-1)  
        y0 = random.randint(0,n-1)
        a = random.randint(0,n-1)
        b = (pow(y0,2,n) - pow(x0,3,n) - a * x0)%n
        delta = utils.XGCD(4*pow(a,3,n)+27*pow(b,2,n),n)[0]
    if(delta !=1) : return delta
    P = (x0,y0)
    d = (utils.XGCD(4,n)[1])%n
    d = (d * (a+2))%n
    primes_up_to_bound = utils.big_eratho(B1)
    for k in utils.primes_up_bound(B1) :
        u = k
        while(u <= B1) :
            u= u *k
            P= ECM_mult(P,k,d,n)
            if(utils.XGCD(n,P[1])[0]!= 1) : return utils.XGCD(n,P[1])[0]
    raise Exception ('Pas de factorisation pour les méchantes courbes, il faut passer a l étape 2 ou recommence avec une autre courbe ou/et un nouveau point de depart') 



def ECM_mult((x,z),k,d,n) :
    
    xp = 0
    xq = x
    zp = 1
    zq = z
    
    i = k.bit_length()
    for l in range(i):
        f = (k>>(i-1-l))-((k>>(i-l))<<1) # regarde si le i-l eme bit de k est un 0 ou un 1
        if(f==0) :
         #  u = pow((xp+zp),2,n)
         #   v = pow((xp-zp),2,n)
         #   t = (d*(u-v)+v)%n
         #   xv = (u*v)%n
         #   zv = ((u-v)*t)%n
         #   u = ((xq+zq)*(xp-zp))%n
         #   v = ((xq-zq)*(xp+zp))%n
         #   w = pow(u+v,2,n)
         #   t = pow(u-v,2,n)
         #   xw = (z*w)%n
         #   zw = (x*t)%n
            xv = (pow((xp+zp),2,n)*pow((xp-zp),2,n))%n
            zv = ((4*xp*zp)*(pow((xp-zp),2,n)+d*4*xp*zp))%n
            xw = (z*pow((xq-zq)*(xp+zp)+(xq+zq)*(xp-zp),2,n))%n
            zw = (x*pow((xq-zq)*(xp+zp)-(xq+zq)*(xp-zp),2,n))%n

        if(f==1) :
         #   u = pow((xq+zq),2,n)
         #   v = pow((xq-zq),2,n)
         #   t = (d*(u-v)+v)%n
         #   xw = (u*v)%n
         #   zw = ((u-v)*t)%n
         #   u = ((xq+zq)*(xp-zp))%n
         #   v = ((xq-zq)*(xp+zp))%n
         #   w = pow(u+v,2,n)
         #   t = pow (u-v,2,n)
         #   xv = (z*w)%n
         #   zv = (x*t)%n
            xv = (z*pow((xq-zq)*(xp+zp)+(xq+zq)*(xp-zp),2,n))%n
            zv = (x*pow((xq-zq)*(xp+zp)-(xq+zq)*(xp-zp),2,n))%n
            xw = (pow((xp+zp),2,n)*pow((xp-zp),2,n))%n
            zw = ((4*xq*zq)*(pow((xq-zq),2,n)+d*4*xq*z))%n

        xp = xv
        zp = zv        
        xq = xw
        zq = zw 
    return ((xp,zp))
        
    
    
