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


############## CALCULATION OF FLUX VALUES AND ASSOCIATED UNCERTAINTIES FOR BOTH FILTERS ###############

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


####################### BINNING AND WEIGHTED AVERAGING ##############################

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


################################ CLIPPING #####################################

# For a given day fo measurement, some of the data points may be outliers, and lie a large distance from the median of all the measurements for a given day.
# We want to find a way of 'clipping' these points, eliminating them based on their distance from neighbouring points (along the y-axis) and thus improving the accuracy of the subsequent weighted mean calculations.




####################### CALCULATING WEIGHTED AVERAGES #########################


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



# Now to calculate the weighted mean values of the flux and time

weighted_var_o = np.zeros(len(summed_weights_o))

for i in range(0, len(time_mean_o)):

	time_mean_o[i] = summed_time_o[i]/time_divisor_o[i]
	flux_mean_o[i] = summed_flux_o[i]/flux_divisor_o[i]
	flux_weighted_mean_o[i] = summed_weighted_flux_o[i]/summed_weights_o[i]


print("Summed times - orange") 
print(summed_time_o)
print()
print("Summed weighted flux orange")
print(summed_weighted_flux_o)
print()
print("No. times summed - orange")
print(time_divisor_o)
print()
print("No. fluxes summed - orange")
print(flux_divisor_o)
print()
print("Weighted Mean Flux - orange")
print(flux_weighted_mean_o)
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


# Now to calculate the mean values of flux and time (weighted and unweighted, respectively)

for i in range(0, len(time_mean_c)):

	time_mean_c[i] = summed_time_c[i]/time_divisor_c[i]
	flux_mean_c[i] = summed_flux_c[i]/flux_divisor_c[i]
	flux_weighted_mean_c[i] = summed_weighted_flux_c[i]/summed_weights_c[i]

print()
print("Summed times - cyan") 
print(summed_time_c)
print()
print("Summed weighted flux - cyan")
print(summed_weighted_flux_c)
print()
print("No. times summed - cyan")
print(time_divisor_c)
print()
print("No. fluxes summed - cyan")
print(flux_divisor_c)
print()
print("Weighted Mean Flux - cyan")
print(flux_weighted_mean_c)
print()



################### STANDARD DEVIATION OF WEIGHTED MEAN FLUXES #####################


# The standard deviation is equal to the square root of the ratio of the sum of the square of the differences of each data point in a day compared to the mean, to the number of data points in a day minus one.

# FOR ORANGE FILTER


denom_o = np.zeros(len(dates_o))

counter_o = 0

for i in range(0, len(dates_o)):

	flux_counter_sd_o = 0

	for j in range(counter_o, len(time_o)):

		flux_counter_sd_o = 0

		if math.floor(time_o[j]) == dates_o[i]:

			flux_counter_sd_o += 1			
			denom_o[i] += flux_counter_sd_o
			counter_o += 1


counter_o = 0

print("orange denominators")
print(denom_o)
print()

# Calculating the n-1 of the standard deviation denominator

denominators_o = np.zeros(len(dates_o))

for i in range(0, len(denom_o)):

	denominators_o[i] = denom_o[i] - 1


# Now, to start calculating the numerator

sq_diff_sum_o = np.zeros(len(dates_o))

for i in range(0, len(dates_o)):

	flux_counter_sd_o = 0

	for j in range(counter_o, len(time_o)):

		flux_counter_sd_o = 0

		if math.floor(time_o[j]) == dates_o[i] and denominators_o[i] != 0:

			diff_from_mean = 0			
			diff_from_mean = flux_o[j] - flux_weighted_mean_o[i]
			squared_diff_from_mean = diff_from_mean**2
			sq_diff_sum_o[i] += squared_diff_from_mean

		if math.floor(time_o[j]) == dates_o[i] and denominators_o[i] == 0:

			sq_diff_sum_o[i] = dflux_o[j]




var_o = np.zeros(len(dates_o))
stdev_o = np.zeros(len(dates_o))

for i in range(0, len(dates_o)):

	if denominators_o[i] != 0:	# If more than one data point in a day have been averaged

		var_o[i] = sq_diff_sum_o[i] / denominators_o[i]	
		stdev_o[i] = var_o[i]**(1/2)

	elif denominators_o[i] == 0:	# if only one data point in a day has been averaged

		denominators_o[i] = 1
		stdev_o[i] = sq_diff_sum_o[i] / denominators_o[i]


print("orange flux standard deviations")
print(stdev_o)
print()




# FOR CYAN FILTER


denom_c = np.zeros(len(dates_c))

counter_c = 0

for i in range(0, len(dates_c)):

	flux_counter_sd_c = 0

	for j in range(counter_c, len(time_c)):

		flux_counter_sd_c = 0

		if math.floor(time_c[j]) == dates_c[i]:

			flux_counter_sd_c += 1			
			denom_c[i] += flux_counter_sd_c
			counter_c += 1


counter_c = 0

print("cyan denominators")
print(denom_c)
print()

# Calculating the n-1 of the standard deviation denominator

denominators_c = np.zeros(len(dates_c))

for i in range(0, len(denom_c)):

	denominators_c[i] = denom_c[i] - 1


# Now, to start calculating the numerator

sq_diff_sum_c = np.zeros(len(dates_c))

for i in range(0, len(dates_c)):

	flux_counter_sd_c = 0

	for j in range(counter_c, len(time_c)):

		flux_counter_sd_c = 0

		if math.floor(time_c[j]) == dates_c[i] and denominators_c[i] != 0:

			diff_from_mean = 0			
			diff_from_mean = flux_c[j] - flux_weighted_mean_c[i]
			squared_diff_from_mean = diff_from_mean**2
			sq_diff_sum_c[i] += squared_diff_from_mean

		if math.floor(time_c[j]) == dates_c[i] and denominators_c[i] == 0:

			sq_diff_sum_c[i] = dflux_c[j]




var_c = np.zeros(len(dates_c))
stdev_c = np.zeros(len(dates_c))

for i in range(0, len(dates_c)):

	if denominators_c[i] != 0:	# If more than one data point in a day have been averaged

		var_c[i] = sq_diff_sum_c[i] / denominators_c[i]	
		stdev_c[i] = var_c[i]**(1/2)

	elif denominators_c[i] == 0:	# if only one data point in a day has been averaged

		denominators_c[i] = 1
		stdev_c[i] = sq_diff_sum_c[i] / denominators_c[i]


print("cyan flux standard deviations")
print(stdev_c)
print()

#used to stop program at this point in the code.
#sys.exit(0)  

print()
print()
print()
print()
print()
print()
print("Length of weighted orange flux array:")
print(len(flux_weighted_mean_o))
print("Length of orange flux uncertainties array:")
print(len(stdev_o))
print("Length of orange mean time measurements:")
print(len(time_mean_o))
print("Length of time measurements counter (orange):")
print(len(time_divisor_o))
print("Length of weighted cyan flux array:")
print(len(flux_weighted_mean_c))
print("Length of cyan flux uncertainties array:")
print(len(stdev_c))
print("Length of cyan mean time measurements:")
print(len(time_mean_c))
print("Length of time measurements counter (cyan):")
print(len(time_divisor_c))
print()
print()
print()



####################################### DATA PLOTTING ###################################################

# Write the data plotted to a .txt file

no_of_measurements_o = np.ones(len(flux_o))
no_of_measurements_c = np.ones(len(flux_c))


filename_2 = supernova + '_flux_raw_weighted.txt'

data_raw_o = np.array([time_o, flux_o, dflux_o, no_of_measurements_o])
data_raw_c = np.array([time_c, flux_c, dflux_c, no_of_measurements_c])
data_wei_o = np.array([time_mean_o, flux_weighted_mean_o, stdev_o, time_divisor_o])
data_wei_c = np.array([time_mean_c, flux_weighted_mean_c, stdev_c, time_divisor_c])


# Transpose the data, to have it in multiple columns
data_raw_o = data_raw_o.T
data_raw_c = data_raw_c.T
data_wei_o = data_wei_o.T
data_wei_c = data_wei_c.T


with open(filename_2, 'w') as datafile_id:
# here, you open the ascii file
	
	np.savetxt(datafile_id, data_raw_o, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time, Flux and Flux Error for Orange Filter (Raw data)',footer='\n')
	np.savetxt(datafile_id, data_raw_c, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time, Flux and Flux Error for Cyan Filter (Raw data)',footer='\n')
	np.savetxt(datafile_id, data_wei_o, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time, Flux, Flux Error and No. Measurements per Weighted Mean for Orange Filter (Weighted Averages)', footer='\n')
	np.savetxt(datafile_id, data_wei_c, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time, Flux, Flux Error and No. Measurements per Weighted Mean for Cyan Filter (Weighted Averages)', footer='\n')


# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

# Two graphs will be plotted on one figure: the data, and an analysis of the standard deviations

plt.figure(1)

plt.errorbar(time_mean_o, flux_weighted_mean_o, yerr=stdev_o, fmt='o', color='red', capsize=5)
plt.errorbar(time_mean_c, flux_weighted_mean_c, yerr=stdev_c, fmt='o', color='blue', capsize=5)

plt.errorbar(time_o, flux_o, yerr = dflux_o, fmt='o', color='orange', alpha = 0.2, capsize=5)
plt.errorbar(time_c, flux_c, yerr = dflux_c, fmt='o', color='cyan', alpha = 0.2, capsize=5)

# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.
plt.xlabel('MJD')
plt.ylabel('Transient Flux (Micro-Janskys)')

# We can also set gridlines and tick marks on the graph.
plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')

# Setting x- and y-axis limits

#plt.xlim([0,200])
plt.ylim([-1000,1000])

# Before plotting the figure, we save it
plt.savefig('SN2019ehk_flux_vs_time_raw_and_weighted_mean.pdf')

# Now we display the figure itself!
plt.show()

