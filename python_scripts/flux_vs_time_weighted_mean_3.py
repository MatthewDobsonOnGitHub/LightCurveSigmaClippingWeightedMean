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






# DATA EXTRACTION

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







# FLUX CALCULATION FOR BOTH FILTERS

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

print()
print()
print()
print()
print()
print("FLUX CALCULATIONS")
#print("Fluxes of orange filter")
#print(flux_o)
#print()
#print("Fluxes of cyan filter")
#print(flux_c)
#print()
#print("Uncertainties of fluxes of orange filter")
#print(dflux_o)
#print()
#print("Uncertainties of fluxes of cyan filter")
#print(dflux_c)	
#print()
#print("Times of orange filter")
#print(time_o)
#print()
#print("Times of cyan filter")
#print(time_c)
#print()
#print()
#print()
#print()
print("Length of orange flux array:")
print(len(flux_o))
print("Length of orange flux uncertainties array:")
print(len(dflux_o))
print("Length of orange time measurements:")
print(len(time_o))
print("Length of cyan flux array:")
print(len(flux_c))
print("Length of cyan flux uncertainties array:")
print(len(dflux_c))
print("Length of orange time measurements:")
print(len(time_c))
print()
print()
print()






# BINNING AND WEIGHTED AVERAGING

# The transient flux values are all taken over separate days.
# Some are taken on the same day, but not at the same time.
# Thus, to find the mean value of the transient magnitude for each day, we must sort the results by the day on which they were measured by binning them.

# To do this, let us consider a pair of data points: the flux measurement and the time at which it was taken.
# We want to calculate both the mean flux value (weighted by the uncertainties) and the mean time value (no uncertainties to weigh by).
# To bin the times by the day on which they were measured, we can round down the time values using the floor function.
# For a given date value, we can then sum all the magnitudes that correspond to that date and then take the average.


# Firstly, we need date values to compare the measurement times to, to determine how they are supposed to be binned.
# We make use of the floor function, to go through the times of every measurement.

floored_o = []
floored_c = []

for i in range(0, len(time_o)):
	floored_o.append(math.floor(time_o[i]))
for i in range(0, len(time_c)):
	floored_c.append(math.floor(time_c[i]))

print("FLOORING THE TIMES")
print()
#print("Raw Time Values (orange)")
#print(time_o)
#print()
#print("Floored Time Values (orange)")
#print(floored_o)
#print()
#print("Raw Time Values (cyan)")
#print(time_c)
#print()
#print("Floored Time Values (cyan)")
#print(floored_c)
#print()
#print()
print("length of orange time array")
print(len(time_o))
print("length of cyan time array")
print(len(time_c))
print("length of orange floored time array")
print(len(floored_o))
print("length of cyan floored time array")
print(len(floored_c))
print()
print()
print()
print()

# Now to remove the redundancy in the array of floored time values.
# This will provide a list of dates with which the floor values of the raw dates can be compared

dates_o = []
dates_c = []

for i in range(0, len(floored_o)):
	
	if floored_o[i] not in dates_o:
	
		dates_o.append(floored_o[i])

	else:

		continue


for i in range(0, len(floored_c)):
	
	if floored_c[i] not in dates_c:
	
		dates_c.append(floored_c[i])

	else:

		continue

# To see what's going on, we print the arrays
print("ELIMINATING REDUNDANCY IN FLOORED TIMES")
print()
#print("orange dates")
#print(dates_o)
#print()
print("length of orange dates")
print(len(dates_o))
#print("cyan dates")
#print(dates_c)
#print()
print("length of cyan dates")
print(len(dates_c))
print()
print()


# This code will calculate a weighted average fo all the flux measurements for a given day of observation. 
# These values will be weighted by the inverse of their variance, i.e. the inverse square of their standard deviation.
# We calculate the weights of each flux value, where a weight is equal to the inverse square of its uncertainty.

#print("Length of dflux_o:")
#print(len(dflux_o))
#print()
#print("Length of dflux_c:") 
#print(len(dflux_o))
#print()

variance_o = np.zeros(len(dflux_o))
variance_c = np.zeros(len(dflux_c))

weights_o = np.zeros(len(dflux_o))
weights_c = np.zeros(len(dflux_c))

for i in range(0, len(dflux_o)):
	variance_o[i] = dflux_o[i]**2
	weights_o[i] = 1/variance_o[i]

for i in range(0, len(dflux_c)):
	variance_c[i] = dflux_c[i]**2
	weights_c[i] = 1/variance_c[i]

print()
print("Weights for the orange filter")
print(weights_o)
print()
print("Weights for the cyan filter")
print(weights_c)
print()
print()

# As of this point, we have an array of the time measurement values (in MJD) and the date on which the measurement occured. 
# However, we still need to calculate the average time value for a given day of measuring.
# To do this, we must cycle through the raw time values (separately for each filter!!) and check if the floor of each time value id equal to the nth value in the date array.
# If this is the case, the time value is summed to a cumulative sum value, and a counter is increased by 1. 
# If not, that summed value is divided by said counter, and the result appended to an empty array. 
# The cycle will continue, but this time comparing the raw time values to the next (n+1th) date value in the date array.
# However, we do not want the inner nested loop to restart; we want it to continue along the list fo raw time values; we just want the index of the outer loop (for the date values) to increase by 1.

counter_o = 0
counter_c = 0


# for orange lens:

summed_time_o = np.zeros(len(dates_o))

summed_flux_o = np.zeros(len(dates_o))

summed_weights_o = np.seros(len(dates_o))

time_divisor_o = np.zeros(len(dates_o))

flux_divisor_o = np.zeros(len(dates_o))

time_mean_o = np.zeros(len(dates_o))

flux_mean_o = np.zeros(len(dates_o))

time_counter_o = 0

flux_counter_o = 0

for i in range(0, len(dates_o)):

	time_counter_o = 0

	flux_counter_o = 0

	for j in range(counter_o, len(time_o)):

		time_counter_o = 0

		flux_counter_o = 0

		if math.floor(time_o[j]) == dates_o[i]:

			summed_time_o[i] += time_o[j]

			summed_flux_o[i] += flux_o[j]

			summed_weights_o[i] += weights_o[j]

			time_counter_o += 1

			flux_counter_o += 1

			time_divisor_o[i] += time_counter_o 

			flux_divisor_o[i] += flux_counter_o

			counter_o += 1

for i in range(0, len(time_mean_o)):

	time_mean_o[i] = summed_time_o[i]/time_divisor_o[i]
	flux_mean_o[i] = summed_flux_o[i]/flux_divisor_o[i]


print("Summed time----------->", summed_time_o)
print("Summed flux----------->", summed_flux_o)
print("No. times  summed----->", time_divisor_o)
print("No. fluxes summed----->", flux_divisor_o)
print("Mean Time------------->", time_mean_o)
print("Mean Flux------------->", flux_mean_o)




# for cyan lens:

summed_time_c = np.zeros(len(dates_c))

summed_flux_c = np.zeros(len(dates_c))

time_divisor_c = np.zeros(len(dates_c))

flux_divisor_c = np.zeros(len(dates_c))

time_mean_c = np.zeros(len(dates_c))

flux_mean_c = np.zeros(len(dates_c))

time_counter_c = 0

flux_counter_c = 0

for i in range(0, len(dates_c)):

	time_counter_c = 0

	flux_counter_c = 0

	for j in range(counter_c, len(time_c)):

		time_counter_c = 0

		flux_counter_c = 0

		if math.floor(time_c[j]) == dates_c[i]:

			summed_time_c[i] += time_c[j]

			summed_flux_c[i] += flux_c[j]

			time_counter_c += 1

			flux_counter_c += 1

			time_divisor_c[i] += time_counter_c 

			flux_divisor_c[i] += flux_counter_c

			counter_c += 1

for i in range(0, len(time_mean_c)):

	time_mean_c[i] = summed_time_c[i]/time_divisor_c[i]
	flux_mean_c[i] = summed_flux_c[i]/flux_divisor_c[i]


print("Summed time----------->", summed_time_c)
print("Summed flux----------->", summed_flux_c)
print("No. times  summed----->", time_divisor_c)
print("No. fluxes summed----->", flux_divisor_c)
print("Mean Time------------->", time_mean_c)
print("Mean Flux------------->", flux_mean_c)
		
#print()
#print()
#print()
#print("Orange Times Length")
#print(len(time_o))
#print("Orange Dates Length")
#print(len(dates_o))
#print("Orange Mean Times Length")
#print(len(time_mean_o))
#print("Orange Fluxes Length")
#print(len(flux_o))
#print("Orange Mean Length")
#print(len(flux_mean_o))
#print()
#print("Cyan Times Length")
#print(len(time_c))
#print("Cyan Dates Length")
#print(len(dates_c))
#print("Cyan Mean Times Length")
#print(len(time_mean_c))
#print("Cyan Fluxes Length")
#print(len(flux_c))
#print("Cyan Mean Fluxes Length")
#print(len(flux_mean_c))













#used to stop program at this point in the code.
#sys.exit(0) 









# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.plot(time_mean_o, flux_mean_o, 'o', color='orange')
plt.plot(time_mean_c, flux_mean_c, 'oc')


plt.errorbar(time_o, flux_o, yerr = dflux_o, fmt='o', color='red', alpha = 0.2, capsize=5)
plt.errorbar(time_c, flux_c, yerr = dflux_c, fmt='o', color='blue', alpha = 0.2, capsize=5)



# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.
plt.xlabel('MJD')
plt.ylabel('Transient Flux (Micro-Janskys)')



# We can set the axis limits
#plt.xlim([58630,58646])
#plt.ylim([-200,300])




# We can also set gridlines and tick marks on the graph.
plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')




# Before plotting the figure, we save it
plt.savefig('flux_vs_time_mean_plot.pdf')



# Now we display the figure itself!
plt.show()


















