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






######################################## DATA EXTRACTION ###############################################


# Now, we separate out all the 'rows' (dictionaries) by which type of filter was used, for later calculations.
# We can use the float() and str() functions (code will automatically read in as a string) to convert the data into the required format (numbers or strings)

time_o_raw = []
time_c_raw = []
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
exposuretime = 40	

# To calculate the flux values of the supernova ATLAS19nar in units of micro-Janskys, values in the data must be called.
# However, they must be separated out by filter.

# Some measurements contain values of 'None', that we do not want to be read into the arrays of the data. This creates our logical conditions for the arrays.


for dictionary in reader:
	
	if dictionary["filter"] == 'o':

		if dictionary["mjd"] != 'None' and dictionary["peakfit"] != 'None' and dictionary["major"] != 'None' and dictionary["minor"] != 'None' and dictionary["zp"] != 'None' and dictionary["apfit"] != 'None':

			time_o_raw.append(float(dictionary["mjd"]))
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

			time_c_raw.append(float(dictionary["mjd"]))
			peakfit_c.append(float(dictionary["peakfit"]))
			dpeakfit_c.append(float(dictionary["dpeak"]))
			major_c.append(float(dictionary["major"]))
			minor_c.append(float(dictionary["minor"]))
			zeropoint_c.append(float(dictionary["zp"]))
			apfit_c.append(float(dictionary["apfit"]))

		else:

			continue






############## CALCULATION OF FLUX VALUES AND ASSOCIATED UNCERTAINTIES FOR BOTH FILTERS ###############

#Define empty arrays for the flux values and uncertainties, one for each filter. calculated values will be appended to these arrays.
flux_o_raw = []
flux_c_raw = []
dflux_o_raw = []
dflux_c_raw = []


for i in range(0, len(peakfit_o)):

	index_o = (zeropoint_o[i] + apfit_o[i])/(-2.5) + 9.56
	flux_numerator_o = peakfit_o[i]*major_o[i]*minor_o[i]
	flux_value_o = (flux_numerator_o/exposuretime)*10**index_o
	flux_o_raw.append(flux_value_o)

for i in range(0, len(peakfit_c)):

	index_c = (zeropoint_c[i] + apfit_c[i])/(-2.5) + 9.56
	flux_numerator_c = peakfit_c[i]*major_c[i]*minor_c[i]
	flux_value_c = (flux_numerator_c/exposuretime)*10**index_c
	flux_c_raw.append(flux_value_c)


for i in range(0, len(dpeakfit_o)):
	index_o = (zeropoint_o[i] + apfit_o[i])/(-2.5) + 9.56
	dflux_numerator_o = dpeakfit_o[i]*major_o[i]*minor_o[i]
	dflux_value_o = (dflux_numerator_o/exposuretime)*10**index_o
	dflux_o_raw.append(dflux_value_o)


for i in range(0, len(dpeakfit_c)):
	index_c = (zeropoint_c[i] + apfit_c[i])/(-2.5) + 9.56
	dflux_numerator_c = dpeakfit_c[i]*major_c[i]*minor_c[i]
	dflux_value_c = (dflux_numerator_c/exposuretime)*10**index_c
	dflux_c_raw.append(dflux_value_c)

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
print(len(flux_o_raw))
print("Length of orange flux uncertainties array:")
print(len(dflux_o_raw))
print("Length of orange time measurements:")
print(len(time_o_raw))
print("Length of cyan flux array:")
print(len(flux_c_raw))
print("Length of cyan flux uncertainties array:")
print(len(dflux_c_raw))
print("Length of orange time measurements:")
print(len(time_c_raw))
print()
print()
print()




######################################## CLIPPING ####################################################

# Many of the data points we want to plot have very large associated errors. We want to find a way of eliminating these points from the final plot, in the hopes of making any given trend more salient without compromising accuracy.

# To do this, we cycle through all of the arrays defined above, and if the errors for a given dataset are less than a manually defined threshold value, they are appended to new 

flux_o = []
flux_c = []
dflux_o = []
dflux_c = []
time_o = []
time_c = []

max_error = 30

# ORANGE FILTER

for i in range(0, len(flux_o_raw)):

	if dflux_o_raw[i] < max_error:

		flux_o.append(flux_o_raw[i])
		dflux_o.append(dflux_o_raw[i])
		time_o.append(time_o_raw[i])

	else:

		continue
		



# CYAN FILTER

for i in range(0, len(flux_c_raw)):

	if dflux_c_raw[i] < max_error:

		flux_c.append(flux_c_raw[i])
		dflux_c.append(dflux_c_raw[i])
		time_c.append(time_c_raw[i])

	else:

		continue




################################# BINNING AND WEIGHTED AVERAGING ########################################


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



################################## CALCULATING WEIGHTED AVERAGES ########################################


# This code will calculate a weighted average fo all the flux measurements for a given day of observation. 
# These values will be weighted by the inverse of their variance, i.e. the inverse square of their standard deviation.
# We calculate the weights of each flux value, where a weight is equal to the inverse square of its uncertainty.

# These weights will also serve a further purpose, in being the uncertainties of the weighted mean flux values

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


# FOR ORANGE LENS:

# The following arrays are for use in the loop

summed_time_o = np.zeros(len(dates_o))

summed_flux_o = np.zeros(len(dates_o))

time_divisor_o = np.zeros(len(dates_o))

flux_divisor_o = np.zeros(len(dates_o))

summed_weighted_flux_o = np.zeros(len(dates_o))

summed_weights_o = np.zeros(len(dates_o))


# The following arrays are for the final calculation of the weighted means

time_mean_o = np.zeros(len(dates_o))

flux_mean_o = np.zeros(len(dates_o))

flux_mean_err_o = np.zeros(len(dates_o))

flux_weighted_mean_o = np.zeros(len(dates_o))

flux_weighted_mean_err_o = np.zeros(len(dates_o))


# Used in calculations

time_counter_o = 0

flux_counter_o = 0

for i in range(0, len(dates_o)):

	time_counter_o = 0

	flux_counter_o = 0

	for j in range(counter_o, len(time_o)):

		time_counter_o = 0

		flux_counter_o = 0

		if math.floor(time_o[j]) == dates_o[i]:

			
			time_counter_o += 1

			flux_counter_o += 1

			summed_time_o[i] += time_o[j]

			summed_flux_o[i] += flux_o[j]

			time_divisor_o[i] += time_counter_o 

			flux_divisor_o[i] += flux_counter_o

			summed_weighted_flux_o[i] += flux_o[j]*weights_o[j]

			summed_weights_o[i] += weights_o[j]

			counter_o += 1


print()
print()
print("Summed Weights - Orange:")
print(summed_weights_o)
print()
print()


weighted_var_o = np.zeros(len(summed_weights_o))

# Now to calculate the standard deviation of the weighted mean values

for i in range(0, len(summed_weights_o)):

	weighted_var_o[i] = 1/summed_weights_o[i]
	flux_weighted_mean_err_o[i] = weighted_var_o[i]**(1/2)


# Now to calculate the weighted mean values of the flux and time

for i in range(0, len(time_mean_o)):

	time_mean_o[i] = summed_time_o[i]/time_divisor_o[i]
	flux_mean_o[i] = summed_flux_o[i]/flux_divisor_o[i]
	flux_weighted_mean_o[i] = summed_weighted_flux_o[i]/summed_weights_o[i]


print("Summed time----------->", summed_time_o)
print()
print("Summed flux----------->", summed_flux_o)
print()
print("Summed weighted flux-->", summed_weighted_flux_o)
print()
print("No. times  summed----->", time_divisor_o)
print()
print("No. fluxes summed----->", flux_divisor_o)
print()
print("Mean Time------------->", time_mean_o)
print()
print("Mean Flux------------->", flux_mean_o)
print()
print("Weighted Mean Flux---->", flux_weighted_mean_o)
print()




# FOR CYAN LENS:

# The following arrays are for use in the loop

summed_time_c = np.zeros(len(dates_c))

summed_flux_c = np.zeros(len(dates_c))

time_divisor_c = np.zeros(len(dates_c))

flux_divisor_c = np.zeros(len(dates_c))

summed_weighted_flux_c = np.zeros(len(dates_c))

summed_weights_c = np.zeros(len(dates_c))


# The following arrays are for the final calculation of the weighted means

time_mean_c = np.zeros(len(dates_c))

flux_mean_c = np.zeros(len(dates_c))

flux_weighted_mean_c = np.zeros(len(dates_c))

flux_mean_err_c = np.zeros(len(dates_c))

flux_weighted_mean_err_c = np.zeros(len(dates_c))


# Used in calculations

time_counter_c = 0

flux_counter_c = 0

for i in range(0, len(dates_c)):

	time_counter_c = 0

	flux_counter_c = 0

	for j in range(counter_c, len(time_c)):

		time_counter_c = 0

		flux_counter_c = 0

		if math.floor(time_c[j]) == dates_c[i]:

			
			time_counter_c += 1

			flux_counter_c += 1

			summed_time_c[i] += time_c[j]

			summed_flux_c[i] += flux_c[j]

			time_divisor_c[i] += time_counter_c 

			flux_divisor_c[i] += flux_counter_c

			summed_weighted_flux_c[i] += flux_c[j]*weights_c[j]

			summed_weights_c[i] += weights_c[j]

			counter_c += 1

print()
print()
print("Summed Weights - Cyan:")
print(summed_weights_c)
print()
print()

weighted_var_c = np.zeros(len(summed_weights_c))

# Now to calculate the weighted error bars of the weighted mean values. According to the Least Mean Square method, this is equal to the square root of the inverse of the summed weights for a given day.

for i in range(0, len(summed_weights_c)):

	weighted_var_c[i] = 1/summed_weights_c[i]
	flux_weighted_mean_err_c[i] = weighted_var_c[i]**(1/2)


# Now to calculate the mean values of flux and time (weighted and unweighted, respectively)

for i in range(0, len(time_mean_c)):

	time_mean_c[i] = summed_time_c[i]/time_divisor_c[i]
	flux_mean_c[i] = summed_flux_c[i]/flux_divisor_c[i]
	flux_weighted_mean_c[i] = summed_weighted_flux_c[i]/summed_weights_c[i]

print()
print("Summed time----------->", summed_time_c)
print()
print("Summed flux----------->", summed_flux_c)
print()
print("Summed weighted flux-->", summed_weighted_flux_c)
print()
print("No. times  summed----->", time_divisor_c)
print()
print("No. fluxes summed----->", flux_divisor_c)
print()
print("Mean Time------------->", time_mean_c)
print()
print("Mean Flux------------->", flux_mean_c)
print()
print("Weighted Mean Flux---->", flux_weighted_mean_c)
print()
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








print()
print("Weighted Orange Flux")
print(flux_weighted_mean_o)
print()
print("Weighted Cyan Flux")
print(flux_weighted_mean_c)
print()
print("Orange Error Bars")
print(flux_weighted_mean_err_o)
print()
print("Cyan Error Bars")
print(flux_weighted_mean_err_c)
print()



############################ STANDARD DEVIATION OF WEIGHTED MEAN FLUXES #################################


# The standard deviation is equal to the square root of the ratio of the sum of the square of the differences of each data point in a day compared to the mean, to the number of data points in a day minus one.

# FOR ORANGE FILTER


sq_diff_sum_o = np.zeros(len(dates_o))
denom_o = np.zeros(len(dates_o))

counter_o = 0

for i in range(0, len(dates_o)):

	flux_counter_sd_o = 0

	for j in range(counter_o, len(time_o)):

		flux_counter_sd_o = 0

		if math.floor(time_o[j]) == dates_o[i]:

			diff_from_mean = 0
			
			diff_from_mean = flux_o[j] - flux_weighted_mean_o[i]

			squared_diff_from_mean = diff_from_mean**2

			sq_diff_sum_o[i] += squared_diff_from_mean

			flux_counter_sd_o += 1
			
			denom_o[i] += flux_counter_sd_o

			counter_o += 1

print()
print("orange square difference sum")
print(sq_diff_sum_o)
print()
print("orange denominators")
print(denom_o)
print()

# Calculating the n-1 of the standard deviation denominator

denominators_o = np.zeros(len(dates_o))

for i in range(0, len(denom_o)):

	denominators_o[i] = denom_o[i]-1

print("orange denominators minus one")
print(denominators_o)
print()

var_o = np.zeros(len(dates_o))
stdev_o = np.zeros(len(dates_o))

for i in range(0, len(dates_o)):

	if denominators_o[i] != 0:	# If more than one data point in a day have been averaged

		var_o[i] = sq_diff_sum_o[i] / denominators_o[i]
	
		stdev_o[i] = var_o[i]**(1/2)

	elif denominators_o ==0:	# if only one data point in a day has been averaged

		denominators_o[i] = 1

		var_o[i] = sq_diff_sum_o[i] / denominators_o[i]

		stdev_o[i] = var_o[i]**(1/2)

print("orange flux standard deviations")
print(stdev_o)
print()



# FOR CYAN FILTER


sq_diff_sum_c = np.zeros(len(dates_c))
denom_c = np.zeros(len(dates_c))

counter_c = 0

for i in range(0, len(dates_c)):

	flux_counter_sd_c = 0

	for j in range(counter_c, len(time_c)):

		flux_counter_sd_c = 0

		if math.floor(time_c[j]) == dates_c[i]:

			diff_from_mean = 0
			
			diff_from_mean = flux_c[j] - flux_weighted_mean_c[i]

			squared_diff_from_mean = diff_from_mean**2

			sq_diff_sum_c[i] += squared_diff_from_mean

			flux_counter_sd_c += 1
			
			denom_c[i] += flux_counter_sd_c

			counter_c += 1

print()
print("cyan square difference sum")
print(sq_diff_sum_c)
print("cyan denominators")
print(denom_c)
print()


# Calculating the n-1 of the standard deviation denominator

denominators_c = np.zeros(len(dates_c))

for i in range(0, len(denom_c)):

	denominators_c[i] = denom_c[i]-1

print("cyan denominators minus one")
print(denominators_c)
print()

var_c = np.zeros(len(dates_c))
stdev_c = np.zeros(len(dates_c))

for i in range(0, len(dates_c)):

	if denominators_c[i] != 0:	# If more than one data point in a day have been averaged

		var_c[i] = sq_diff_sum_c[i] / denominators_c[i]
	
		stdev_c[i] = var_c[i]**(1/2)

	elif denominators_c ==0:	# If only one data point in a day has been averaged

		denominators_c[i] = 1

		var_c[i] = sq_diff_sum_c[i] / denominators_c[i]

		stdev_c[i] = var_c[i]**(1/2)


print("cyan flux standard deviations")
print(stdev_c)
print()










#used to stop program at this point in the code.
#sys.exit(0) 











#USED TO CHECK THE DIFFERENCE BETWEEN WEIGHTED ERROR AND STANDARD DEVIATION 

stdev_diff_o = stdev_o - flux_weighted_mean_err_o

stdev_diff_c = stdev_c - flux_weighted_mean_err_c





####################################### DATA PLOTTING ################################################


# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.


# Two graphs will be plotted on one figure: the data, and an analysis of the standard deviations

plt.figure(1)
plt.subplot(211)

plt.errorbar(time_mean_o, flux_weighted_mean_o, yerr=stdev_o, fmt='o', color='red', capsize=5)
plt.errorbar(time_mean_c, flux_weighted_mean_c, yerr=stdev_c, fmt='o', color='blue', capsize=5)

#plt.errorbar(time_mean_o, flux_weighted_mean_o, yerr=flux_weighted_mean_err_o, fmt='o', color='yellow', capsize=5)
#plt.errorbar(time_mean_c, flux_weighted_mean_c, yerr=flux_weighted_mean_err_c, fmt='o', color='purple', capsize=5)

plt.errorbar(time_o, flux_o, yerr = dflux_o, fmt='o', color='orange', alpha = 0.2, capsize=5)
plt.errorbar(time_c, flux_c, yerr = dflux_c, fmt='o', color='cyan', alpha = 0.2, capsize=5)



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



plt.subplot(212)

plt.plot(flux_weighted_mean_err_o, stdev_diff_o, 'o', color='magenta')
plt.plot(flux_weighted_mean_err_c, stdev_diff_c, 'o', color='green')

#plt.xlim([0,200])
#plt.ylim([-20,40])

# Before plotting the figure, we save it
plt.savefig('flux_vs_time_mean_plot_stdev_and_errors_clipped_2.pdf')



# Now we display the figure itself!
plt.show()


















