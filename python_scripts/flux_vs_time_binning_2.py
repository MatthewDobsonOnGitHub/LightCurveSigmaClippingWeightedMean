#!/usr/bin/env python

# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab
import csv
import sys


##################### DATA IMPORT #########################

# Now, we read in the transient data.
# Data file has columns separated by commas.
# We can read in the data as a set of dictionaries; a dictionary contains a list of data pairs: a key and its associated value
# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).
# in case the filename needs to be changed, it's more accessible to define it here as a concatenated string variable, with the supernova name prefixed to the filename. 
# This prevents files being created for the same supernova with different supernova names.

supernova = "SN2018hmx"	

# file that contains the raw data (starts with SN designation)
filename = supernova + "_raw_data.csv" 

# each row in the datafile becomes its own dictionary; 'reader' contains many dictionaries.

reader = csv.DictReader(open(filename))


#################### DATA EXTRACTION #######################

# Now, we separate out all the 'rows' (dictionaries) by which type of filter was used, for later calculations.
# We can use the float() and str() functions (code will automatically read in as a string) to convert the data into the required format (numbers or strings)

mag_o = []
mag_c = []
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

# Some measurements contain values of 'None', that we do not want to be read into the arrays of the data. This creates our logical conditions for the arrays.

for dictionary in reader:
	
	if dictionary["filter"] == 'o':

		if dictionary["mjd"] != 'None' and dictionary["peakfit"] != 'None' and dictionary["major"] != 'None' and dictionary["minor"] != 'None' and dictionary["zp"] != 'None' and dictionary["apfit"] != 'None':

			mag_o.append(str(dictionary["mag"]))
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

			mag_c.append(str(dictionary["mag"]))
			time_c.append(float(dictionary["mjd"]))
			peakfit_c.append(float(dictionary["peakfit"]))
			dpeakfit_c.append(float(dictionary["dpeak"]))
			major_c.append(float(dictionary["major"]))
			minor_c.append(float(dictionary["minor"]))
			zeropoint_c.append(float(dictionary["zp"]))
			apfit_c.append(float(dictionary["apfit"]))

		else:

			continue


###### CALCULATION OF FLUX VALUES AND ASSOCIATED UNCERTAINTIES FOR BOTH FILTERS ######

#Define empty arrays for the flux values and uncertainties, one for each filter. Calculated values will be appended to these arrays.

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
print("FLUX CALCULATIONS")
print()
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

####################################### CALCULATION OF DATES ###########################################

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
print("length of orange dates")
print(len(dates_o))
print("length of cyan dates")
print(len(dates_c))
print()
print()


################################# BINNING #################################

# Now we bin the measurement times and fluxes by their date of measurement, by flooring a given time and comparing to a date in an array. If on the same day, they are appended to an array, which is itself appended to a new array as on of its elements.

# The loop proceeds to bin dates from a long list into sub-arrays, provided that their floored value of measurement time is equal to the integer date it is compared to.

# If this condition is no longer true, then the sub-arrays are appended to empty arrays as their elements, and the loop breaks and restarts anew for the element in the full time array where it left off. 

counter_o = 0
counter_c = 0

#### CYAN FILTER ####

time_binned_c = []
flux_binned_c = []
dflux_binned_c = []

for i in range(0, len(dates_c)):

	time_binned_element_array_c = []
	flux_binned_element_array_c = []
	dflux_binned_element_array_c = []

	for j in range(counter_c, len(time_c)):

		if math.floor(time_c[j]) == dates_c[i]:

			counter_c += 1
			time_binned_element_array_c.append(time_c[j])
			flux_binned_element_array_c.append(flux_c[j])
			dflux_binned_element_array_c.append(dflux_c[j])

		else:

			time_binned_c.append(time_binned_element_array_c)
			flux_binned_c.append(flux_binned_element_array_c)
			dflux_binned_c.append(dflux_binned_element_array_c)
			break

	


### ORANGE FILTER ###

time_binned_o = []
flux_binned_o = []
dflux_binned_o = []

for i in range(0, len(dates_o)):

	time_binned_element_array_o = []
	flux_binned_element_array_o = []
	dflux_binned_element_array_o = []

	for j in range(counter_o, len(time_o)):

		if math.floor(time_o[j]) == dates_o[i]:

			counter_o += 1
			time_binned_element_array_o.append(time_o[j])
			flux_binned_element_array_o.append(flux_o[j])
			dflux_binned_element_array_o.append(dflux_o[j])

		else:

			time_binned_o.append(time_binned_element_array_o)
			flux_binned_o.append(flux_binned_element_array_o)
			dflux_binned_o.append(dflux_binned_element_array_o)
			break


print("Binned Time Array (orange)")
print(time_binned_o)
print()
print("Binned Flux Array (orange)")
print(flux_binned_o)
print()
print("Binned Error Array (orange)")
print(dflux_binned_o)
print()
print("Binned Time Array (cyan)")
print(time_binned_c)
print()
print("Binned Flux Array (cyan)")
print(flux_binned_c)
print()
print("Binned Error Array (cyan)")
print(dflux_binned_c)
print()


########################## SIGMA CLIPPING ##########################

# Some of the data points will be outliers compared to the others in their binned set, and need to be excised from the total dataset wihout compromising accuracy. To do this, we perform 'SIGMA CLIPPING'.

# Sigma Clipping involves calculating the median and standard deviation of all the flux values in a day, and determining how far from the median the datapoints are, in units of standard deviation. 

# Data points that lie beyond a certain range - a given multiple of standard deviation - are removed.

# The standard deviation and median are then recalculated, until all datapoints lie within the required range (in units of the recalculated standard deviation).





