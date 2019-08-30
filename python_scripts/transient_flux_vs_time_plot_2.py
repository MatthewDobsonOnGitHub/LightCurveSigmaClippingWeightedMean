#!/usr/bin/env python
#
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab






# DATA IMPORT

# Now, we read in the transient data.
# Data file has columns separated by commas.
# To prevent it reading an entire row as a string, we use a function np.genfromtxt to generate an array from the data, recognising that the columns are separated by commas using delimiter=','
# Enter data file name inside brackets.
# This will store the data from the file as an array called 'data'.

data = np.genfromtxt("k9B7deoy.txt", delimiter=',')	






# DATA EXTRACTION

# Firstly, we store the desired data to be plotted in arrays, one for each axis.
# To do this, we select a given column, denoted by a number, and select all rows in the column (:).
# Note: the 1st row/column is denoted '0', the 2nd row/column denoted '1', etc.
# The time values of the transient measurements will be plotted on the x-axis, units of Mean Julian Date

time = data[:,8]		# Time (MJD)

# To calculate the flux values of the supernova ATLAS19nar in units of micro-Janskys, values in the data array must be called.

peakfit = data[:,13]
dpeakfit = data[:,14]
major = data[:,19]
minor = data[:,20] 
zeropoint = data[:,7]
apfit = data[:,23]
exposuretime = 30	# Exposure time for all the measurements was 30 SECONDS


# to see what's going on -- whether we've picked the correct column.
#for i in range(0, len(peakfit)):
#	print(peakfit[i])
#	print()


#Define empty arrays for the flux values and uncertainties. calculated values will be appended to these arrays.
flux = []
dflux = []

for i in range(0, len(peakfit)):
	index = (zeropoint[i] + apfit[i])/(-2.5) + 9.56
	flux_numerator = peakfit[i]*major[i]*minor[i]
	flux_value = (flux_numerator/exposuretime)*10**index
	flux.append(flux_value)

for i in range(0, len(dpeakfit)):
	index = (zeropoint[i] + apfit[i])/(-2.5) + 9.56
	dflux_numerator = dpeakfit[i]*major[i]*minor[i]
	dflux_value = (dflux_numerator/exposuretime)*10**index
	dflux.append(dflux_value)

print(flux)
print(dflux)	


print(len(zeropoint))
print(len(peakfit))
print(len(dpeakfit))
print(len(major))
print(len(minor))
print(len(time))


# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.errorbar(time, flux, yerr = dflux, fmt = 'ob', ecolor = 'b', capsize = 5)



# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.

plt.xlabel('MJD')
plt.ylabel('Transient Flux (Micro-Janskys)')



# We can also set gridlines and tick marks on the graph.

plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')




# Before plotting the figure, we save it

plt.savefig('flux_vs_time_plot_1.pdf')



# Now we display the figure itself!

plt.show()


















