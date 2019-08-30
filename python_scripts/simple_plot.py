#!/usr/bin/env python		->>>>>>>>	THIS LINE OF CODE MUST BE INCLUDED
#										FOR THIS SCRIPT TO BE READ TO THE 
#										COMMAND LINE!										
#	loading in necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import math

#	loading in data
data = np.loadtxt('textfile.txt')

#	setting size of output graph
fig = plt.figure(figsize=(12, 6), dpi=100)

#	plotting the data

#plt.plot(data[:,0], data[:,1], color = 'red', label = 'NIR', alpha =0.8)
# in data[x,y] tells it to plot the xth row and yth column of data
#plt.plot(data[:,0], data[:,2], color = 'blue', label = 'NIR', linestyle = '--', marker = '.', alpha =0.8)

#to plot markers, do marker = 'x' for x's, marker = '.' for dots, etc.

plt.errorbar(data[:,0], data[:,1], yerr = data[:,2], fmt = 'ob', capsize = 5, linestyle = '')
#fmt determines the style (1st letter) and colour (2nd letter) of the data points.


#	plotting legend
plt.legend(loc='best')

#	setting gridlines and tick marks on x and y axes
plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')

#	setting titles for x and y axes
plt.xlabel('Rest Wavelength / $\mathrm{\AA}$')
plt.ylabel('Flux / erg $\mathrm{s^{-1}}$ $\mathrm{cm^{-2}}$ $\mathrm{\AA^{-1}}$')

#	adjusting x and y axis limits
plt.xlim([0,11])
plt.ylim([-20,120])

#	adjusting the border
plt.subplots_adjust(left=0.06)
plt.subplots_adjust(right=0.95)
plt.subplots_adjust(bottom=0.09)
plt.subplots_adjust(top=0.96)

plt.savefig('dry_run.pdf')

#	plotting graph
plt.show()

