#!/usr/bin/env python
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab
import csv
import sys
import statistics as stat

######### STANDARD DEVIATION FUNCTION (WILL BE USEFUL LATER) #########

# The standard deviation is equal to the square root of the ratio of the sum of the square of the differences of each data point in a day compared to the mean, to the number of data points in a day minus one.

def standard_deviation(array, error):

	if len(array) > 1:

		mu = stat.mean(array)
		summ = 0
		denominator = len(array)-1

		for i in range(0, len(array)):

			diff = 0
			diff = mu - array[i]
			sq_diff = diff**2
			summ = summ + sq_diff

		variance = summ / denominator
		sigma = variance**(1/2)

		return sigma

	elif len(array) == 1:

		sigma = max(error)

		return sigma

##################### DATA IMPORT #####################
# Now, we read in the transient data.
# Data file has columns separated by commas.
# We can read in the data as a set of dictionaries; a row contains a list of data pairs: a key and its associated value
# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).
# in case the filename needs to be changed, it's more accessible here.

supernova = "SN2018kzr"

filename = supernova + "_raw_data.csv"

# each row in the datafile becomes its own row; 'reader' contains many dictionaries. Each dictionary is an 'ordered dictionary'.

reader = csv.DictReader(open(filename))

###################### DATA SORTING ######################
# Here, we create two empty dictionaries, that will contain as keys: the integer measurement times, and their associated values arrays, each element of which is a dictionary containing all the data about that measurement (float MJD, declination, RA, peakfit, etc.)

odict = {}
cdict = {}

exposuretime = 30

# 'reader' is a massive array, with each element a dictionary. The following uses logical conditions to:
# 1. sort through which measurement have enough data to calculate flux
# 2. calculate the flux values for each measurement (and their associated uncertainties)
# 3. sort every measurement according to which wavelength filter was used (as these must be manipulated separately)
# The calculated flux values go into a new key, as do their associated uncertainties.
# The measurements are sorted into two dictionaries, one for each filter, which contain as keys the integer dates, and as values arrays, whose each element is a dictionary containing the data of a given measurement (the measurements are thus binned by day).
# For every dictionary (row) in the array 'reader' that contains all the observational data for a transient.

for row in reader:
    
    # Ensures that a given observation has enough data from which the observed flux can be calculated.
    
	if row["mjd"] != 'None' and row["peakfit"] != 'None' and row["major"] != 'None' and row["minor"] != 'None' and row["zp"] != 'None' and row["apfit"] != 'None':
        
        	# Here, we calculated the flux and its uncertainty
        
		index = (float(row["zp"]) + float(row["apfit"]))/(-2.5) + 9.56
		flux_numerator = float(row["peakfit"])*float(row["major"])*float(row["minor"])
		flux_value = (flux_numerator/exposuretime)*10**index
		row["calc_flux"] = flux_value
        
		dindex = (float(row["zp"]) + float(row["apfit"]))/(-2.5) + 9.56
		dflux_numerator = float(row["dpeak"])*float(row["major"])*float(row["minor"])
		dflux_value = (dflux_numerator/exposuretime)*10**dindex
		row["calc_dflux"] = dflux_value
        
		row["weight"] = dflux_value**(-2)
        
        # If the measurement was made with the orange filter
        
		if row["filter"] == 'o':
            
			# Firstly, we append the row to the appropriate key in the orange filter data dictionary 'odict'
            
			try:
                
			# The syntax here is: dictionary["(new)key"].append(array)

				odict[int(float(row["mjd"]))].append(dict(row))
        
			# However, if this key does not exist, we need to create this key:value pair to begin with, creating it as an empty list. However, the following code must be kept separate, and run only once per measurement day analysed, as repeating this will erase all rows of data apart from the last one in the day.
            
			except KeyError as e:
                
				odict[int(float(row["mjd"]))] = []
				odict[int(float(row["mjd"]))].append(dict(row))

		# If the measurement was made with the cyan filter

		elif row["filter"] == 'c':
        
			# Firstly, we append the row to the appropriate key in the orange filter data dictionary 'odict'
        
			try:
            
				cdict[int(float(row["mjd"]))].append(dict(row))
            
			# However, if this key does not exist, we need to create this key:value pair to begin with, creating it as an empty list. However, the following code must be kept separate, and run only once per measurement day analysed, as repeating this will erase all rows of data apart from the last one in the day.
            
			except KeyError as e:
                
				cdict[int(float(row["mjd"]))] = []
				cdict[int(float(row["mjd"]))].append(dict(row))


###### WEIGHTED MEAN CALCULATIONS ######
# Here, we make the calculations of the weighted mean of the flux values in a given day.
# Here, we define two empty dictionaries, one for each filter, which will contain, for a given weighted mean measurement, the measurement time, flux value, flux uncertainty, and number of points used to make the weighted mean.
# Their keys will be time, flux, error and number, and their values the arrays of these values, whose equivalent nth elements correspond to a given nth measurement. 

mean_data_o = {}
mean_data_c = {}
raw_data_o = {}
raw_data_c = {}
print()
print("********** ORANGE ***********")
print()
r_time_o = []
r_flux_o = []
r_dev_o = []
r_mag_o = []
m_time_o = []
w_flux_o = []
s_dev_o = []
num_o = []
print()

for key, value in odict.items():
    
	time_sum_o = 0.0
	flux_weight_product_sum_o = 0.0
	weight_sum_o = 0.0
	stdv_o = 0.0
	print()
	print("Day MJD")
	print(key)
	measurement_array_o = []  
	uncertainty_array_o = []
	time_array_o = []
	mag_array_o = []

	for row in value:

		print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
		time_sum_o = time_sum_o + float(row["mjd"])   
		flux_weight_product_sum_o = flux_weight_product_sum_o + (float(row["calc_flux"])*float(row["weight"]))
		weight_sum_o = weight_sum_o + float(row["weight"])         
		measurement_array_o.append(row["calc_flux"]) 
		uncertainty_array_o.append(row["calc_dflux"]) 
		time_array_o.append(row["mjd"]) 
		mag_array_o.append(row["mag"])

		r_flux_o.append(float(row["calc_flux"])) 
		r_dev_o.append(float(row["calc_dflux"])) 
		r_time_o.append(float(row["mjd"])) 
		r_mag_o.append(row["mag"])		# Raw magnitude values to compare to our calculated ones, which are found from flux values.

	# The number of times summed is the length of the 'value' array.  
	print()	
	mean_time_o = time_sum_o / len(value)
	weighted_flux_o = flux_weight_product_sum_o / weight_sum_o
	stdv_o = standard_deviation(measurement_array_o, uncertainty_array_o)
	print("Mean Time Sum - Cyan")
	print(mean_time_o)
	m_time_o.append(mean_time_o)
	print()
	print("Weighted Sum - Cyan")
	print(weighted_flux_o)
	w_flux_o.append(weighted_flux_o)
	print()
	print("Uncertainty Associated with Weighted Mean - Orange")
	print(stdv_o)
	s_dev_o.append(stdv_o)
	print()
	print("Number of Data Points Averaged in this Day - Orange")
	print(len(value))
	number_o = len(value)
	num_o.append(number_o)
	print()
	
mean_data_o["Time"] = m_time_o
mean_data_o["Flux"] = w_flux_o
mean_data_o["Error"] = s_dev_o
mean_data_o["Number"] = num_o

raw_data_o["Time"] = r_time_o
raw_data_o["Flux"] = r_flux_o
raw_data_o["Error"] = r_dev_o

print()
print()
print("********** CYAN ***********")
print()

r_time_c = []
r_flux_c = []
r_dev_c = []
r_mag_c = []

m_time_c = []
w_flux_c = []
s_dev_c = []
num_c = []

print()
for key, value in cdict.items():
    
	time_sum_c = 0.0
	flux_weight_product_sum_c = 0.0
	weight_sum_c = 0.0
	stdv_c = 0.0
	print()
	print("Day MJD")
	print(key)
	measurement_array_c = []  
	uncertainty_array_c = []
	time_array_c = [] 

	for row in value:

		print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
		time_sum_c = time_sum_c + float(row["mjd"])   
		flux_weight_product_sum_c = flux_weight_product_sum_c + (float(row["calc_flux"])*float(row["weight"]))
		weight_sum_c = weight_sum_c + float(row["weight"])         
		measurement_array_c.append(row["calc_flux"]) 
		uncertainty_array_c.append(row["calc_dflux"]) 
		time_array_c.append(row["mjd"]) 

		r_flux_c.append(float(row["calc_flux"])) 
		r_dev_c.append(float(row["calc_dflux"])) 
		r_time_c.append(float(row["mjd"])) 
		r_mag_c.append(row["mag"])		# Raw magnitude values to compare to our calculated ones, which are found from flux values.


	# The number of times summed is the length of the 'value' array.  
	print()	
	mean_time_c = time_sum_c / len(value)
	weighted_flux_c = flux_weight_product_sum_c / weight_sum_c
	stdv_c = standard_deviation(measurement_array_c, uncertainty_array_c)
	print("Mean Time Sum - Cyan")
	print(mean_time_c)
	m_time_c.append(mean_time_c)
	print()
	print("Weighted Sum - Cyan")
	print(weighted_flux_c)
	w_flux_c.append(weighted_flux_c)
	print()
	print("Uncertainty Associated with Weighted Mean - Cyan")
	print(stdv_c)
	s_dev_c.append(stdv_c)
	print()
	print("Number of Data Points Averaged in this Day - Cyan")
	print(len(value))
	number_c = len(value)
	num_c.append(number_c)
	print()

mean_data_c["Time"] = m_time_c
mean_data_c["Flux"] = w_flux_c
mean_data_c["Error"] = s_dev_c
mean_data_c["Number"] = num_c

raw_data_c["Time"] = r_time_c
raw_data_c["Flux"] = r_flux_c
raw_data_c["Error"] = r_dev_c

for key, value in mean_data_o.items():

	print(key)
	print(value)

print()

for key, value in mean_data_c.items():

	print(key)
	print(value)

print()
print("Raw Times - Orange")
print(r_time_o)
print()
print("Flux Times - Orange")
print(r_flux_o)
print()
print("Error Times - Orange")
print(r_dev_o)
print()
print("Raw Times - Cyan")
print(r_time_c)
print()
print("Flux Times - Cyan")
print(r_flux_c)
print()
print("Error Times - Cyan")
print(r_dev_c)
print()

############################ CROSS-CHECKING FLUX CALCULATIONS ############################

# This is a method to cross-check the flux calculations. We convert the calculated flux values into janskys, then into magnitudes, and then plot them against the raw magnitude values in the original datafile.
# The magnitude values read into the arrays contain minimum mag values, with the '>' symbol. This prevents the values from being read in as floats, and therefore, these values require removal.
# Since we don't know exactly how many magnitude values will be sorted and calculated without looking at the raw data file beforehand, we must define arrays that will contain the indermediate calculated quantities as empty, and append values to them.

magnitude_calc_o = []	# non-upperlimit measured magnitudes (orange - all)
magnitude_calc_c = []	# non-upperlimit measured magnitudes (cyan - all)
magnitude_recalc_o = []	# recalculated magnitude values (orange - all)
magnitude_recalc_c = []	# recalculated magnitude values (cyan - all)
flux_corresponding_o = [] 	# Flux values corresponding to every recalculated magnitude value (orange)
flux_corresponding_c = [] 	# Flux values corresponding to every recalculated magnitude value (cyan)
dmagnitude_recalc_o = []	# recalculated magnitude uncertainties (orange - all)
dmagnitude_recalc_c = []	# recalculated magnitude uncertainties (cyan - all)
three_dmagnitude_recalc_o = []	# 3 sigma magnitude uncertainty for all measurements (orange)
three_dmagnitude_recalc_c = []	# 3 sigma magnitude uncertainty for all measurements (cyan)
dflux_corresponding_o = [] 	# Flux uncertainty values (orange - all)
dflux_corresponding_c = []	# Flux uncertainty values (cyan - all)
time_corresponding_o = []	# Time values corresponding to every recalculated magnitude value (orange)
time_corresponding_c = []	# Time values corresponding to every recalculated magnitude value (cyan)


for i in range(0, len(r_mag_o)):
	if '>' not in r_mag_o[i] and r_flux_o[i] >= 0 and r_dev_o[i] >= 0:
		mag_float_o = float(r_mag_o[i])
		magnitude_calc_o.append(mag_float_o)
		flux_corresponding_o.append(r_flux_o[i])
		dflux_corresponding_o.append(r_dev_o[i])
		time_corresponding_o.append(r_time_o[i])

for i in range(0, len(r_mag_c)):
	if '>' not in r_mag_c[i] and r_flux_c[i] >= 0 and r_dev_c[i] >= 0:
		mag_float_c = float(r_mag_c[i])
		magnitude_calc_c.append(mag_float_c)
		flux_corresponding_c.append(r_flux_c[i])
		dflux_corresponding_c.append(r_dev_c[i])
		time_corresponding_c.append(r_time_c[i])

# Converting microjansky flux values and uncertainties from microjanskys to janskys
flux_jan_o = np.zeros(len(flux_corresponding_o))
dflux_jan_o = np.zeros(len(dflux_corresponding_o))
three_dflux_jan_o = np.zeros(len(dflux_corresponding_o))

for i in range(0, len(flux_jan_o)):
	flux_jan_o[i] = flux_corresponding_o[i]*10**(-6)
	dflux_jan_o[i] = dflux_corresponding_o[i]*10**(-6)
	three_dflux_jan_o[i] = 3*dflux_jan_o[i]

flux_jan_c = np.zeros(len(flux_corresponding_c))
dflux_jan_c = np.zeros(len(dflux_corresponding_c))
three_dflux_jan_c = np.zeros(len(dflux_corresponding_o))

for i in range(0, len(flux_jan_c)):
	flux_jan_c[i] = flux_corresponding_c[i]*10**(-6)
	dflux_jan_c[i] = dflux_corresponding_o[i]*10**(-6)
	three_dflux_jan_c[i] = 3*dflux_jan_c[i]

# Now we must calculate the magnitudes:
for i in range(0, len(flux_jan_o)):
	if flux_jan_o[i] >= 0 and dflux_jan_o[i] >= 0:
		mag_o = (-2.5) * math.log(flux_jan_o[i], 10) + 8.9
		magnitude_recalc_o.append(mag_o)
		dmag_o = (-2.5) * math.log(dflux_jan_o[i], 10) + 8.9
		dmagnitude_recalc_o.append(dmag_o)
		three_dmag_o = (-2.5) * math.log(three_dflux_jan_o[i], 10) + 8.9
		three_dmagnitude_recalc_o.append(three_dmag_o)
	else:
		continue

for i in range(0, len(flux_jan_c)):
	if flux_jan_c[i] >= 0 and dflux_jan_c[i] >= 0:
		mag_c = (-2.5) * math.log(flux_jan_c[i], 10) + 8.9
		magnitude_recalc_c.append(mag_c)
		dmag_c = (-2.5) * math.log(dflux_jan_c[i], 10) + 8.9
		dmagnitude_recalc_c.append(dmag_c)
		three_dmag_c = (-2.5) * math.log(three_dflux_jan_c[i], 10) + 8.9
		three_dmagnitude_recalc_c.append(three_dmag_c)
	else:
		continue

print()
print("Re-calculated magnitudes - orange")
print(magnitude_recalc_o)
print("Re-calculated magnitudes - cyan")
print(magnitude_recalc_c)
print("Re-calculated magnitude uncertainties - orange")
print(dmagnitude_recalc_o)
print("Re-calculated magnitude uncertainties - cyan")
print(dmagnitude_recalc_c)
print("3 sigma magnitude uncertainties - orange")
print(three_dmagnitude_recalc_o)
print("3 sigma magnitude uncertainties - cyan")
print(three_dmagnitude_recalc_c)
print()
print("Re-calculated magnitudes length - orange")
print(len(magnitude_recalc_o))
print("Re-calculated magnitudes length - orange")
print(len(dmagnitude_recalc_o))
print("Re-calculated magnitudes length - cyan")
print(len(magnitude_recalc_c))
print("Re-calculated magnitudes length - cyan")
print(len(dmagnitude_recalc_c))
print("3 sigma magnitude uncertainties length - orange")
print(len(three_dmagnitude_recalc_o))
print("3 sigma magnitude uncertainties length - cyan")
print(len(three_dmagnitude_recalc_c))
print()		

# Now to calculate the difference between the measured and the recalculated magnitudes

mag_diff_o = []
mag_diff_c = []

for i in range(0, len(magnitude_recalc_o)):
	mag_diff_for_o = magnitude_recalc_o[i] - magnitude_calc_o[i]
	mag_diff_o.append(mag_diff_for_o)

for i in range(0, len(magnitude_recalc_c)):
	mag_diff_for_c = magnitude_recalc_c[i] - magnitude_calc_c[i]
	mag_diff_c.append(mag_diff_for_c)

mag_rel_diff_o = np.zeros(len(mag_diff_o))
mag_rel_diff_c = np.zeros(len(mag_diff_c))

for i in range(0, len(mag_diff_o)):
	mag_rel_diff_o[i] = (mag_diff_o[i] / magnitude_calc_o[i])*100
for i in range(0, len(mag_diff_c)):
	mag_rel_diff_c[i] = (mag_diff_c[i] / magnitude_calc_c[i])*100

print("Magnitude Difference for Orange Filter")
print(mag_diff_o)
print()
print("Magnitude Difference for Cyan Filter")
print(mag_diff_c)
print()
print("Raw Cyan Data Dictionary")
print(raw_data_c)
print()

##################################### DATA WRITING #####################################

# Write the data plotted to a .txt file

filename_2 = supernova + '_flux_weighted_mean_and_mag.txt'

data_raw_o = np.array([raw_data_o["Time"], raw_data_o["Flux"], raw_data_o["Error"]])
data_raw_c = np.array([raw_data_c["Time"], raw_data_c["Flux"], raw_data_c["Error"]])
data_wei_o = np.array([mean_data_o["Time"], mean_data_o["Flux"], mean_data_o["Error"], mean_data_o["Number"]])
data_wei_c = np.array([mean_data_c["Time"], mean_data_c["Flux"], mean_data_c["Error"], mean_data_c["Number"]])
data_mag_o = np.array([time_corresponding_o, flux_corresponding_o, magnitude_recalc_o, dmagnitude_recalc_o, three_dmagnitude_recalc_o])
data_mag_c = np.array([time_corresponding_c, flux_corresponding_c, magnitude_recalc_c, dmagnitude_recalc_c, three_dmagnitude_recalc_c])

# Transpose the data, to have it in multiple columns
data_raw_o = data_raw_o.T
data_raw_c = data_raw_c.T
data_wei_o = data_wei_o.T
data_wei_c = data_wei_c.T
data_mag_o = data_mag_o.T
data_mag_c = data_mag_c.T

with open(filename_2, 'w') as datafile_id:
# here, you open the ascii file
	
	np.savetxt(datafile_id, data_raw_o, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Orange Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_raw_c, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Cyan Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_o, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Orange Filter (Weighted Averages)', footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_c, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Cyan Filter (Weighted Averages)', footer='\n\n\n')
	np.savetxt(datafile_id, data_mag_o, fmt=['%s','%s','%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux (microjanskys) and Calculated Magnitude Value, Magnitude Uncertainty and 3-sigma Error for Orange Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_mag_c, fmt=['%s','%s','%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux (microjanskys) and Calculated Magnitude Value, Magnitude Uncertainty and 3-sigma Error for Cyan Filter (Raw data)',footer='\n\n\n')


##################################### DATA PLOTTING #####################################

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.
# Two graphs will be plotted on one figure: the data, and an analysis of the standard deviations

plt.figure("Flux vs Time and Magnitude Recalculation")

plt.subplot(311)

plt.errorbar(mean_data_o["Time"], mean_data_o["Flux"], yerr=mean_data_o["Error"], fmt='o', color='red', capsize=5)
plt.errorbar(mean_data_c["Time"], mean_data_c["Flux"], yerr=mean_data_c["Error"], fmt='o', color='blue', capsize=5)
plt.errorbar(r_time_o, r_flux_o, yerr=r_dev_o, fmt='o', color='orange', alpha = 0.2, capsize=5)
plt.errorbar(r_time_c, r_flux_c, yerr=r_dev_c, fmt='o', color='cyan', alpha = 0.2, capsize=5)
# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.
plt.xlabel('MJD')
plt.ylabel('Transient Flux (microjanskys)')
# We can also set gridlines and tick marks on the graph.
plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')
# Setting x- and y-axis limits
#plt.xlim([0,200])
#plt.ylim([-400,600])

plt.subplot(312)

plt.plot(time_corresponding_o, magnitude_calc_o, 'o', color='orange')
plt.plot(time_corresponding_c, magnitude_calc_c, 'o', color='cyan')
plt.plot(time_corresponding_o, magnitude_recalc_o, 'o', color='red')
plt.plot(time_corresponding_c, magnitude_recalc_c, 'o', color='blue')
plt.xlabel('MJD')
plt.ylabel('Magnitudes (measured and recalculated)')
# Remembering that the more negative the magnitude the brighter the transient
# we reverse the direction of the y-axis.
plt.gca().invert_yaxis()

plt.subplot(313)

plt.plot(magnitude_calc_o, mag_rel_diff_o, 'o', color='magenta')
plt.plot(magnitude_calc_c, mag_rel_diff_c, 'o', color='magenta')
plt.xlabel('Measured Magnitudes')
plt.ylabel('Magnitude Percentage Difference')
plt.ylim([-0.1,0.1])
plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')

#plt.subplot(414)

#plt.errorbar(time_corresponding_o, magnitude_recalc_o, yerr=three_dmagnitude_recalc_o, fmt='o', color='orange', alpha = 0.2, capsize=5)
#plt.errorbar(time_corresponding_c, magnitude_recalc_c, yerr=three_dmagnitude_recalc_c, fmt='o', color='cyan', alpha = 0.2, capsize=5)
#plt.gca().invert_yaxis()
fig_name = supernova + '_flux_vs_time_plot_using_dictionaries.pdf'

# Before plotting the figure, we save it
plt.savefig(fig_name)

# Now we display the figure itself!
plt.show()



