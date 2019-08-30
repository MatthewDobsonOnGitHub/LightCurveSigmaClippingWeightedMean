#!/usr/bin/env python
#
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab
import csv
import sys






# DATA IMPORT

# Now, we read in the transient data.
# Data file has columns separated by commas.
# We can read in the data as a set of dictionaries; a dictionary contains a list of data pairs: a key and its associated value

# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).


# in case the filename needs to be changed, it's more accessible here.	
filename = "PK8fUD7n.csv" 

# each row in the datafile becomes its own dictionary; 'reader' contains many dictionaries.
reader = csv.DictReader(open(filename))

# Now, we separate out all the 'rows' (dictionaries) by which type of filter was used, for later calculations.
# We can use the float() and str() functions (code will automatically read in as a string) to convert the data into the required format (numbers or strings)

time_o = []
time_c = []
peakfit_o = []
peakfit_c = []
dpeakfit_o = []
dpeakfit_c = []
major_o = []
major_c = []
minor_o = []
minor_c = []
zeropoint_o = []
zeropoint_c = []
apfit_o = []
apfit_c = []


# Exposure time for all the measurements was 30 SECONDS
exposuretime = 30	

# To calculate the flux values of the supernova ATLAS19nar in units of micro-Janskys, values in the data must be called.
# However, they must be separated out by filter.


for dictionary in reader:
	
	if dictionary["filter"] == 'o':

		if dictionary["mjd"] != 'None' and dictionary["peakfit"] != 'None' and dictionary["major"] != 'None' and dictionary["minor"] != 'None' and dictionary["zp"] != 'None' and dictionary["apfit"] != 'None':

			time_o.append(float(dictionary["mjd"]))
			peakfit_o.append(float(dictionary["peakfit"]))
			dpeakfit_o.append(float(dictionary["dpeak"]))
			major_o.append(float(dictionary["major"]))
			minor_o.append(float(dictionary["minor"]))
			zeropoint_o.append(float(dictionary["zp"]))
			apfit_o.append(float(dictionary["apfit"]))

		else:

			continue

	elif dictionary["filter"] == 'c':

		if dictionary["mjd"] != 'None' and dictionary["peakfit"] != 'None' and dictionary["major"] != 'None' and dictionary["minor"] != 'None' and dictionary["zp"] != 'None' and dictionary["apfit"] != 'None':

			time_c.append(float(dictionary["mjd"]))
			peakfit_c.append(float(dictionary["peakfit"]))
			dpeakfit_c.append(float(dictionary["dpeak"]))
			major_c.append(float(dictionary["major"]))
			minor_c.append(float(dictionary["minor"]))
			zeropoint_c.append(float(dictionary["zp"]))
			apfit_c.append(float(dictionary["apfit"]))

		else:

			continue

print("Times for o-filter")	
print(time_o)
print()
print()
print("Times for c-filter")
print(time_c)	



#used to stop program at this point in the code.
#sys.exit(0) 



#Define empty arrays for the flux values and uncertainties, one for each filter. calculated values will be appended to these arrays.
flux_o = []
flux_c = []
dflux_o = []
dflux_c = []


for i in range(0, len(peakfit_o)):

	index_o = (zeropoint_o[i] + apfit_o[i])/(-2.5) + 9.56
	flux_numerator_o = peakfit_o[i]*major_o[i]*minor_o[i]
	flux_value_o = (flux_numerator_o/exposuretime)*10**index_o
	flux_o.append(flux_value_o)

for i in range(0, len(peakfit_c)):

	index_c = (zeropoint_c[i] + apfit_c[i])/(-2.5) + 9.56
	flux_numerator_c = peakfit_c[i]*major_c[i]*minor_c[i]
	flux_value_c = (flux_numerator_c/exposuretime)*10**index_c
	flux_c.append(flux_value_c)


for i in range(0, len(dpeakfit_o)):
	index_o = (zeropoint_o[i] + apfit_o[i])/(-2.5) + 9.56
	dflux_numerator_o = dpeakfit_o[i]*major_o[i]*minor_o[i]
	dflux_value_o = (dflux_numerator_o/exposuretime)*10**index_o
	dflux_o.append(dflux_value_o)


for i in range(0, len(dpeakfit_c)):
	index_c = (zeropoint_c[i] + apfit_c[i])/(-2.5) + 9.56
	dflux_numerator_c = dpeakfit_c[i]*major_c[i]*minor_c[i]
	dflux_value_c = (dflux_numerator_c/exposuretime)*10**index_c
	dflux_c.append(dflux_value_c)


print(flux_o)
print(flux_c)
print(dflux_o)
print(dflux_c)	
print(time_o)
print(time_c)
print()
print()
print(len(flux_o))
print(len(dflux_o))
print(len(time_o))
print(len(flux_c))
print(len(dflux_c))
print(len(time_c))







# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.errorbar(time_o, flux_o, yerr = dflux_o, fmt = 'or', ecolor = 'r', capsize = 5)
plt.errorbar(time_c, flux_c, yerr = dflux_c, fmt = 'ob', ecolor = 'b', capsize = 5)


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

plt.savefig('flux_vs_time_plot_2.pdf')



# Now we display the figure itself!

plt.show()


















