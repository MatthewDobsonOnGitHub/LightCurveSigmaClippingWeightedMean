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

######### MEDIAN AND STANDARD DEVIATION FUNCTIOM ###########

def median_and_stdev(value):	

	# To calculate the standard deviation of the daily flux measurements, we append them to an 		empty array, and so the same for their uncertainties and measurement times (to separate arrays, of 		course). The standard deviation function we defined at the start requires two inputs: values and raw 		errors, in order to compute the error for a lone measurement in a day.
	measurement_clipping_array_o = []  
	uncertainty_clipping_array_o = []
	time_clipping_array_o = []
	# Resetting the values of sigma and median to zero, for every iteration.
	sigma = 0
	med = 0

	for row in value:

		measurement_clipping_array_o.append(row["calc_flux"]) 
		uncertainty_clipping_array_o.append(row["calc_dflux"]) 
		time_clipping_array_o.append(row["mjd"]) 
			
	# Calculates the standard deviation of all flux values in a day
	sigma = standard_deviation(measurement_clipping_array_o, uncertainty_clipping_array_o)

	# Calculates the median of all flux values in a day
	med = stat.median(measurement_clipping_array_o)

	return sigma, med



####### REMOVE ROW FUNCTION #######

def remove_row(value, sigma, median):

	empty_list = []

	for row in value:	

		# If a measurement lies outside the 1 sigma range from the median (i.e. it is an outlier)...
		if row["calc_flux"] < (sigma + median) and row["calc_flux"] > (sigma - median):
			
			# ... then we delete the entire measurement from the dictionary
			empty_list.append(row)
		else:

			print("Doing some clipping")


	return empty_list


##################### DATA IMPORT #####################
# Firstly, we read in the transient data.
# Data file has columns of physical quantities, separated by commas.
# We can read in the data as a set of dictionaries; a row in the original data file contains a list of data pairs: a key and its associated value
# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).
# in case the filename needs to be changed, it's more accessible here.

supernova = "SN2019muj"

filename = supernova + "_raw_data_reduced.csv"

# each row in the datafile becomes its own row; 'reader' contains many dictionaries. Each dictionary is an 'ordered dictionary'.
# In short, 'reader' is an array, with each element a dictionary, whose key:value pairs are the physical quantites and their values.

reader = csv.DictReader(open(filename))


###################### DATA SORTING ######################
# Here, we create two empty dictionaries, one for each filter used, that will contain as keys: the integer measurement times; and their associated values: arrays, each element of which is a dictionary containing all the data about that measurement (float MJD, declination, RA, peakfit, etc.)
# This will help to bin the data by day; a key of the dictionary is the integer day on which its measurement occur - its value an array; each element a dictionary containing all the data about a given measurement.

odict = {}
cdict = {}

exposuretime = 30	# Necessary for manual calculations of flux.

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
        
        	# Here, we calculated the flux and its uncertainty for every measurement, and append the values as new key:value pairs to that measurement's dictionary.
        
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
			# What this does is append the data of a single measurement to the dictionary appropriate to its filter; the key becomes the integer date it was measured on, and its value the dictionary of data for that measurement. Since it's very likely that more than one measurement will occur on a given day, the data of further measurements on the same day are APPENDED to the same key.
# Thus, each key is an integer day, and the value an array, each element of which is a dictionary of the data for a given measurement.

				odict[int(float(row["mjd"]))].append(dict(row))
        
			# However, if this key does not exist, we need to create this key:value pair to begin with, creating it as an empty list. However, the following code must be kept separate, and run only once per measurement day analysed, as repeating this will erase all rows of data apart from the last one in the day.
            
			except KeyError as e:
                
				odict[int(float(row["mjd"]))] = []
				odict[int(float(row["mjd"]))].append(dict(row))

		# If the measurement was made with the cyan filter

		elif row["filter"] == 'c':
        
			try:
            
				cdict[int(float(row["mjd"]))].append(dict(row))
            
			except KeyError as e:
                
				cdict[int(float(row["mjd"]))] = []
				cdict[int(float(row["mjd"]))].append(dict(row))



###### CLIPPING ######
# Within a given day, some of the measurements will have outlying flux values. We want to clip the data - removing the outlying points in a given day, without affecting the accuracy of the data.
# There is a known method of doing this: we calculate the standard deviation and the median of every measurement for a given day, and check to see whether every data point lies within one s.d. from the median. If not, any outlying points (beyond 1 s.d. of the median) are discarded.
# The process is repeated; a new s.d. and median calculated for the remaining points - and continues until every point for a day lies within 1 s.d. from the median.

# We create new copies of the dictionaries that contain the data.

clipping_data_o = odict.copy()
clipping_data_c = cdict.copy()

# We loop through all the days of measurements, and loop through all the measurements taken on each day (nested loops).

for key, value in clipping_data_o.items():

	list_length = len(value)

	print()
	print("test message")

	list_length_new = len(value)
        difference = 0

	# create an array of list lengths , starting with original list length

	length_array = [list_length]

	# while....	

	# condition: if list_length != 1:

		# do stuff
		
		sigma, med = median_and_stdev(value)

		new_list = remove_row(value, sigma, med)
                #if len(new_list) < list_length:

		#print("new list length")
		#print(len(new_list))
		list_length_new = len(new_list)

		length_array.append(list_length_new)

		#print("Something's going on here")
		value = new_list

		# condition: if length_array[i] - length_array[i-1] != 0

		print()

print()
print("FULL")
print()
for key, value in odict.items():

	print(key)
	print()
	for row in value:
		print(row["calc_flux"])
print()

for key, value in cdict.items():

	print(key)
	print()
	for row in value:

		print(row["calc_flux"])
print()	


print("CLIPPED")
print()
for key, value in clipping_data_o.items():

	print(key)
	print()
	for row in value:

		print(row["calc_flux"])
print()

for key, value in clipping_data_c.items():

	print(key)
	print()
	for row in value:

		print(row["calc_flux"])
print()	

###### WEIGHTED MEAN CALCULATIONS ######
# Here, we make the calculations of the weighted mean of the flux values in a given day.
# Here, we define two empty dictionaries, one for each filter, which will contain, for a given weighted mean measurement, the measurement time, flux value, flux uncertainty, and number of points used to make the weighted mean.
# Their keys will be time, flux, error and number, and their values the arrays of these values, whose equivalent nth elements correspond to a given nth measurement. 

mean_data_o = {}
mean_data_c = {}
raw_data_o = {}
raw_data_c = {}
#print()
#print("********** ORANGE ***********")
#print()
r_time_o = []
r_flux_o = []
r_dev_o = []
r_mag_o = []
m_time_o = []
w_flux_o = []
s_dev_o = []
num_o = []
#print()

for key, value in clipping_data_o.items():
    
	time_sum_o = 0.0
	flux_weight_product_sum_o = 0.0
	weight_sum_o = 0.0
	stdv_o = 0.0
	#print()
	#print("Day MJD")
	#print(key)
	measurement_array_o = []  
	uncertainty_array_o = []
	time_array_o = []

	for row in value:

		#print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
		time_sum_o += float(row["mjd"])   
		flux_weight_product_sum_o += (float(row["calc_flux"])*float(row["weight"]))
		weight_sum_o += float(row["weight"])         
		measurement_array_o.append(row["calc_flux"]) 
		uncertainty_array_o.append(row["calc_dflux"]) 
		time_array_o.append(row["mjd"]) 

		r_flux_o.append(float(row["calc_flux"])) 
		r_dev_o.append(float(row["calc_dflux"])) 
		r_time_o.append(float(row["mjd"])) 

	# The number of times summed is the length of the 'value' array.  
	#print()	
	mean_time_o = time_sum_o / len(value)
	weighted_flux_o = flux_weight_product_sum_o / weight_sum_o
	stdv_o = standard_deviation(measurement_array_o, uncertainty_array_o)
	#print("Mean Time Sum - Cyan")
	#print(mean_time_o)
	m_time_o.append(mean_time_o)
	#print()
	#print("Weighted Sum - Cyan")
	#print(weighted_flux_o)
	w_flux_o.append(weighted_flux_o)
	#print()
	#print("Uncertainty Associated with Weighted Mean - Orange")
	#print(stdv_o)
	s_dev_o.append(stdv_o)
	#print()
	#print("Number of Data Points Averaged in this Day - Orange")
	#print(len(value))
	number_o = len(value)
	num_o.append(number_o)
	#print()
	
mean_data_o["Time"] = m_time_o
mean_data_o["Flux"] = w_flux_o
mean_data_o["Error"] = s_dev_o
mean_data_o["Number"] = num_o

raw_data_o["Time"] = r_time_o
raw_data_o["Flux"] = r_flux_o
raw_data_o["Error"] = r_dev_o

#print()
#print()
#print("********** CYAN ***********")
#print()

r_time_c = []
r_flux_c = []
r_dev_c = []

m_time_c = []
w_flux_c = []
s_dev_c = []
num_c = []

#print()
for key, value in clipping_data_c.items():
    
	time_sum_c = 0.0
	flux_weight_product_sum_c = 0.0
	weight_sum_c = 0.0
	stdv_c = 0.0
	#print()
	#print("Day MJD")
	#print(key)
	measurement_array_c = []  
	uncertainty_array_c = []
	time_array_c = [] 

	for row in value:

		#print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
		time_sum_c += float(row["mjd"])   
		flux_weight_product_sum_c += (float(row["calc_flux"])*float(row["weight"]))
		weight_sum_c += float(row["weight"])         
		measurement_array_c.append(row["calc_flux"]) 
		uncertainty_array_c.append(row["calc_dflux"]) 
		time_array_c.append(row["mjd"]) 

		r_flux_c.append(float(row["calc_flux"])) 
		r_dev_c.append(float(row["calc_dflux"])) 
		r_time_c.append(float(row["mjd"])) 


	# The number of times summed is the length of the 'value' array.  
	#print()	
	mean_time_c = time_sum_c / len(value)
	weighted_flux_c = flux_weight_product_sum_c / weight_sum_c
	stdv_c = standard_deviation(measurement_array_c, uncertainty_array_c)
	#print("Mean Time Sum - Cyan")
	#print(mean_time_c)
	m_time_c.append(mean_time_c)
	#print()
	#print("Weighted Sum - Cyan")
	#print(weighted_flux_c)
	w_flux_c.append(weighted_flux_c)
	#print()
	#print("Uncertainty Associated with Weighted Mean - Cyan")
	#print(stdv_c)
	s_dev_c.append(stdv_c)
	#print()
	#print("Number of Data Points Averaged in this Day - Cyan")
	#print(len(value))
	number_c = len(value)
	num_c.append(number_c)
	#print()

mean_data_c["Time"] = m_time_c
mean_data_c["Flux"] = w_flux_c
mean_data_c["Error"] = s_dev_c
mean_data_c["Number"] = num_c

raw_data_c["Time"] = r_time_c
raw_data_c["Flux"] = r_flux_c
raw_data_c["Error"] = r_dev_c

#for key, value in mean_data_o.items():

#	print(key)
#	print(value)
#print()

#for key, value in mean_data_c.items():

#	print(key)
#	print(value)
#print()

#print("Raw Times - Orange")
#print(r_time_o)
#print()
#print("Flux Times - Orange")
#print(r_flux_o)
#print()
#print("Error Times - Orange")
#print(r_dev_o)
#print()
#print("Raw Times - Cyan")
#print(r_time_c)
#print()
#print("Flux Times - Cyan")
#print(r_flux_c)
#print()
#print("Error Times - Cyan")
#print(r_dev_c)
#print()


##################################### DATA WRITING #####################################

# Write the data plotted to a .txt file

filename_2 = supernova + '_flux_weighted_mean.txt'

data_raw_o = np.array([raw_data_o["Time"], raw_data_o["Flux"], raw_data_o["Error"]])
data_raw_c = np.array([raw_data_c["Time"], raw_data_c["Flux"], raw_data_c["Error"]])
data_wei_o = np.array([mean_data_o["Time"], mean_data_o["Flux"], mean_data_o["Error"], mean_data_o["Number"]])
data_wei_c = np.array([mean_data_c["Time"], mean_data_c["Flux"], mean_data_c["Error"], mean_data_c["Number"]])

# Transpose the data, to have it in multiple columns
data_raw_o = data_raw_o.T
data_raw_c = data_raw_c.T
data_wei_o = data_wei_o.T
data_wei_c = data_wei_c.T

with open(filename_2, 'w') as datafile_id:
# here, you open the ascii file
	
	np.savetxt(datafile_id, data_raw_o, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Orange Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_raw_c, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Cyan Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_o, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Orange Filter (Weighted Averages)', footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_c, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Cyan Filter (Weighted Averages)', footer='\n\n\n')


##################################### DATA PLOTTING #####################################

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.
# Two graphs will be plotted on one figure: the data, and an analysis of the standard deviations

plt.figure("Flux vs Time")

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
#plt.xlim([xmin,xmax])
#plt.ylim([ymin,ymax])

fig_name = supernova + '_flux_vs_time_plot_using_dictionaries.pdf'

# Before plotting the figure, we save it
plt.savefig(fig_name)

# Now we display the figure itself!
plt.show()


