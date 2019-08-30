#!/usr/bin/env python
#
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab
import csv






# DATA IMPORT

# Now, we read in the transient data.
# Data file has columns separated by commas.
# We can read in the data as a set of dictionaries; a dictionary contains a list of data pairs: a 

# csv.reader is better than the np.genfromtxt


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
major_o = []
major_c = []
minor_o = []
minor_c = []
zeropoint_o = []
zeropoint_c = []
apfit_o = []
apfit_c = []

exposuretime = 30	# Exposure time for all the measurements was 30 SECONDS

# To calculate the flux values of the supernova ATLAS19nar in units of micro-Janskys, values in the data must be called.
# However, they must be separated out by filter.


for dictionary in reader:
	
	if dictionary["filter"] == 'o':

	    	time_o.append(float(dictionary["mjd"]))
		peakfit_o.append(float(dictionary["peakfit"]))
		major_o.append(float(dictionary["major"]))
		minor_o.append(float(dictionary["minor"]))
		zeropoint_o.append(float(dictionary["zp"]))
		apfit_o.append(float(dictionary["apfit"]))

	elif dictionary["filter"] == 'c':

		time_c.append(float(dictionary["mjd"]))
		peakfit_c.append(float(dictionary["peakfit"]))
		major_c.append(float(dictionary["major"]))
		minor_c.append(float(dictionary["minor"]))
		zeropoint_c.append(float(dictionary["zp"]))
		apfit_c.append(float(dictionary["apfit"]))
	
	

#print(ra_o)


sys.exit(0) #used to stop program at this point in the code.



# to see what's going on -- whether we've picked the correct column.
#for i in range(0, len(peakfit)):
#	print(peakfit[i])
#	print()


#Define empty arrays for the flux values and uncertainties, one for each filter. calculated values will be appended to these arrays.
flux_o = []
flux_c = []
dflux_o = []
dflux_c = []
time_o = []
time_c = []

for i in range(0, len(peakfit)):
	index = (zeropoint[i] + apfit[i])/(-2.5) + 9.56
	flux_numerator = peakfit[i]*major[i]*minor[i]
	flux_value = (flux_numerator/exposuretime)*10**index
	if telescope_filter[i] == 'o':
		flux_o.append(flux_value)
		time_o.append(time[i])
	if telescope_filter[i] == 'c':
		flux_c.append(flux_value)
		time_o.append(time[i])

for i in range(0, len(dpeakfit)):
	index = (zeropoint[i] + apfit[i])/(-2.5) + 9.56
	dflux_numerator = dpeakfit[i]*major[i]*minor[i]
	dflux_value = (dflux_numerator/exposuretime)*10**index
	if telescope_filter[i] == 'o':
		dflux_o.append(dflux_value)
	if telescope_filter[i] == 'c':
		dflux_c.append(dflux_value)

print(flux_o)
print(flux_c)
print(dflux_o)
print(dflux_c)	
print(time_o)
print(time_c)
print(telescope_filter)

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

plt.errorbar(time_o, flux_o, yerr = dflux_o, fmt = 'ob', ecolor = 'b', capsize = 5)



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


















