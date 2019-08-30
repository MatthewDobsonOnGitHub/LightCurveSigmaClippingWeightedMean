#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import pylab as p
import math

Lsun = 3.86e26       # solar luminosity Watts
msun = 1.99e30       # solar mass kg 
sb_sigma = 5.67E-08  # Stefan Boltzmann Constant W m^-2 K^-4
G = 6.67E-11         # N m^2 kg^-2 
c = 3e8              # speed of light m/s 

# Velocity required to reach a luminosity L, at Temperature T
time  =  2     # day
Lum   = 1e43   #erg/s
T     = 17000  # Temperature, K

time_sec = time * 24 * 3600 # sec
Lum_W = Lum * 1e-7          # Watts 
V  = math.pow(time_sec,-1) * math.pow(Lum_W, 0.5) * math.pow(T, -2) * math.pow(4*sb_sigma*math.pi, -0.5)  # Velocity in m/s
V_kms  = V/1000  # Velocity in km/s

# KE of the ejecta at that velocity 
mass = 0.1 # ejecta mass in solar masses
mass_kg = mass * msun
KE = 0.3 * mass_kg * math.pow(V, 2)
KE_ergs = KE * 1e7 

# Ni mass required to produce that luminosity 
t = 5 # days since 56Ni created 
tau_56Ni = 8.7 
m56Ni = Lum/(7.8e43) * math.pow(math.e, t/tau_56Ni)

# Arnett ejecta mass 
tau_m = 5     # rise time in days
kappa = 0.1
beta = 13.7
E_kergs = 2e51    # KE of explosion in ergs
#
E_k = E_kergs/1e7    # KE of explosion in Joules
tau_ms =  tau_m * 24 * 3600 # rise time in sec
#
MArnett_kg = math.pow((tau_ms/1.05 * math.pow(beta*c,0.5) * math.pow(kappa, -0.5) * math.pow(E_k, 0.25)),1.3333333)
MArnett = MArnett_kg/msun
VArnett = math.pow((10/3)*E_k/MArnett_kg,0.5)  # m/s
VArnett_kms =  VArnett/1000 # m/s


# Co Mass to produce tail phase
tau_56Co = 111  
t_tail = 16.8    # example epoch in tail phase 
L_tail = 6e40  # Luminosity at this point erg/s 
m56Ni_tail = L_tail/(1.4e43) * (math.pow(math.e, -1*t_tail/tau_56Co) - math.pow(math.e, -1*t_tail/tau_56Ni) / (1 - (tau_56Ni/tau_56Co)))


#print time_sec
#print Lum_W
#print math.pi 
#print math.sqrt(4*sb_sigma*math.pi)
print ("Velocity to reach peak L in %d days             = %.0f km/s" % (time, V_kms))
print ("KE for mass of %f Msun at this velocity         = %.3e ergs" % (mass, KE_ergs))
print ("56Ni mass to produce luminosity at time %d days = %.3f Msol" % (t, m56Ni))
print ("56Ni mass to produce 56Co tail luminosity at time %d days = %.3f Msol" % (t_tail, m56Ni_tail))
print (" ")
print ("Arnett ejecta mass for rise of %d days with explosion energy %.2e = %.3f Msun" % (tau_m ,E_kergs, MArnett))
print ("Velocity for this mass and energy                                 = %d km/s" % (VArnett_kms))



