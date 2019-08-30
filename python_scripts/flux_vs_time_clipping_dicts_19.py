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
import os

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

	# To calculate the standard deviation of the daily flux measurements, we append them to an 		empty array, and so the same for their uncertainties and measurement times (to separate arrays, 	of course). The standard deviation function we defined at the start requires two inputs: values 	and raw errors, in order to compute the error for a lone measurement in a day.
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

		print()
		print("Median")
		print(median)
		print("Sigma")
		print(sigma)
		print(row["calc_flux"], row["mjd"], median+sigma, median-sigma)

		# If a measurement lies outside the 1 sigma range from the median (i.e. it is an outlier)...
		if row["calc_flux"] < (median + (number_sigma*sigma)) and row["calc_flux"] > (median - (number_sigma*sigma)):
			print("ACCEPTABLE DATA POINT")
			empty_list.append(row)
		else:
			print("Doing some clipping")

	return empty_list



##################### DATA IMPORT #####################

# Firstly, we read in the transient data.
# Data file has columns of physical quantities, separated by commas.
# We can read in the data as a set of dictionaries; a row in the original data file contains a list of data pairs: a key and its associated value
# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).

# We define the name of the supernova under study as a string, to be concatenated to the files this code produces, and to identify which data files to read in.

supernova = input("Enter Supernova to Analyse: ")

# This code will produce a plot of flux vs time, and a text file of calculated data; both of these will be stored in a directory, which we define here. 

directory = '/home/mdobson/Archive/Objects/' + supernova + '/ATLAS/'

# If this directory (file) does not already exist, we can created it using the code here.
if not os.path.exists(directory):
	os.makedirs(directory)

filename = supernova + "_raw_data.csv"

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



###################### CLIPPING #######################

# Within a given day, some of the measurements will have outlying flux values. We want to clip the data - removing the outlying points in a given day, without affecting the accuracy of the data.
# There is a known method of doing this: we calculate the standard deviation and the median of every measurement for a given day, and check to see whether every data point lies within one s.d. from the median. If not, any outlying points (beyond 1 s.d. of the median) are discarded.
# The process is repeated; a new s.d. and median calculated for the remaining points - and continues until every point for a day lies within 1 s.d. from the median.

# Ideally, we would use a do...while loop, but that is not possible with the Python language. Instead, we write the code to be run first, then duplicate it in a while loop that follows the initial instance of code. In a sense, the loop performs an initial round of clipping and then checks whether or not to proceed.

# Just in case, a good thing to do would be to define the number of standard deviations beyond which data points should be clipped. Normally, it is one sigma, but sometimes it could be more.

number_sigma = float(input("Enter number of standard deviations for clipping: "))

# We create new copies of the dictionaries that contain the data, in order to preserve the read-in data, should something happen in the code that causes it to be edited.
clipping_data_o = odict.copy()
clipping_data_c = cdict.copy()

# We define two empty dictionaries (one for each filter), where 
clipped_data_o = {}
clipped_data_c = {}

# We loop through all the days of measurements, and loop through all the measurements taken on each day (nested loops).

for key, value in clipping_data_o.items():

	# Define the number of points per day in the initial, unclipped data.
	list_length = len(value)

	# Define the number of points per day in the clipped data - this will be subject to change of value with each iteration
	list_length_new = len(value)

	# Create an array of list lengths, starting with original list length
	length_array = [list_length]

	# Finding the standard deviation and median values for each day; the function returns two variables, and assigns the values in a specific order, so be careful!
	sigma, med = median_and_stdev(value)

	# Performs the clipping an initial first time.
	new_list = remove_row(value, sigma, med)

	# Appends the length of the new, clipped list to the array.
	length_array.append(len(new_list))

	print(length_array)

	while(True): # Infinite loop, until the last two elements in the array are of equal length

		# calculate new s.d. and median for every clipping iteration

		sigma, med = median_and_stdev(new_list)

		# If no more points have been clipped (i.e. the number of unclipped points in a day after passing the data through the clipping function is the same), we want the algorithm to stop for a given day.
		if length_array[-1] == length_array[-2]:

			# The newest list is appended to the empty dictionary for clipped data, with the same key as the original, unclipped data.

			clipped_data_o[key] = new_list
			print("Break Out")			
			print(length_array)
			break

		# If clipping has been performed (i.e. if the new clipped list is shorter than before), we want this to continue.

		else:
			# perform clipping again
			new_list = remove_row(value, sigma, med)
			# newest list added to the clipped data dictionary (it seemingly overwrites the original array)
			clipped_data_o[key] = new_list
			# number of remaining data points calculated, and appended to the appropriate array
			length_array.append(len(new_list))
			print(length_array)
			sigma, med = median_and_stdev(new_list)
	

for key, value in clipping_data_c.items():

	list_length = len(value)

	list_length_new = len(value)

	length_array = [list_length]

	sigma, med = median_and_stdev(value)

	new_list = remove_row(value, sigma, med)

	length_array.append(len(new_list))

	print(length_array)

	while(True):

		sigma, med = median_and_stdev(new_list)

		if length_array[-1] != length_array[-2]:

			new_list = remove_row(value, sigma, med)
			clipped_data_c[key] = new_list
			length_array.append(len(new_list))
			print(length_array)
			sigma, med = median_and_stdev(new_list)

		else:

			clipped_data_c[key] = new_list
			print("Break Out")			
			print(length_array)
			break

print()
print()
print("FULL")
for key, value in odict.items():
	print()
	print(key)
	print()
	for row in value:
		print(row["calc_flux"])
print()

for key, value in cdict.items():
	print()
	print(key)
	print()
	for row in value:

		print(row["calc_flux"])
print()	
print()
print("CLIPPED")
for key, value in clipped_data_o.items():
	print()
	print(key)
	print()
	for row in value:

		print(row["calc_flux"])
print()

for key, value in clipped_data_c.items():
	print()
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

# ORANGE #

r_time_o = []
r_flux_o = []
r_dev_o = []
r_mag_o = []
m_time_o = []
w_flux_o = []
s_dev_o = []
num_o = []
new_error_o = []

for key, value in clipped_data_o.items():
    
	time_sum_o = 0.0
	flux_weight_product_sum_o = 0.0
	weight_sum_o = 0.0
	stdv_o = 0.0
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

	# The number of measurements summed is the length of the 'value' array. 
	if len(value) > 0:
 	
		mean_time_o = time_sum_o / len(value)
		weighted_flux_o = flux_weight_product_sum_o / weight_sum_o
		stdv_o = standard_deviation(measurement_array_o, uncertainty_array_o)
		err_o = (weight_sum_o)**(-1/2)
		m_time_o.append(mean_time_o)
		w_flux_o.append(weighted_flux_o)
		s_dev_o.append(stdv_o)
		new_error_o.append(err_o)
		number_o = len(value)
		num_o.append(number_o)
	
mean_data_o["Time"] = m_time_o
mean_data_o["Flux"] = w_flux_o
mean_data_o["STDEV"] = s_dev_o
mean_data_o["Number"] = num_o
mean_data_o["Error"] = new_error_o

raw_data_o["Time"] = r_time_o
raw_data_o["Flux"] = r_flux_o
raw_data_o["STDEV"] = r_dev_o

# CYAN #

r_time_c = []
r_flux_c = []
r_dev_c = []
m_time_c = []
w_flux_c = []
s_dev_c = []
num_c = []
new_error_c = []

for key, value in clipped_data_c.items():
    
	time_sum_c = 0.0
	flux_weight_product_sum_c = 0.0
	weight_sum_c = 0.0
	stdv_c = 0.0
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
	if len(value) > 0:
		mean_time_c = time_sum_c / len(value)
		weighted_flux_c = flux_weight_product_sum_c / weight_sum_c
		stdv_c = standard_deviation(measurement_array_c, uncertainty_array_c)
		err_c = (weight_sum_c)**(-1/2)
		m_time_c.append(mean_time_c)
		w_flux_c.append(weighted_flux_c)
		s_dev_c.append(stdv_c)
		new_error_c.append(err_c)
		number_c = len(value)
		num_c.append(number_c)

mean_data_c["Time"] = m_time_c
mean_data_c["Flux"] = w_flux_c
mean_data_c["STDEV"] = s_dev_c
mean_data_c["Number"] = num_c
mean_data_c["Error"] = new_error_c

raw_data_c["Time"] = r_time_c
raw_data_c["Flux"] = r_flux_c
raw_data_c["STDEV"] = r_dev_c


##################################### DATA WRITING #####################################

# Write the data plotted to a .txt file

filename_2 = directory + supernova + '_flux_weighted_mean_clipped.txt'

data_raw_o = np.array([raw_data_o["Time"], raw_data_o["Flux"], raw_data_o["STDEV"]])
data_raw_c = np.array([raw_data_c["Time"], raw_data_c["Flux"], raw_data_c["STDEV"]])
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

plt.figure("Flux vs Time - " + supernova)

plt.errorbar(mean_data_o["Time"], mean_data_o["Flux"], yerr=mean_data_o["Error"], fmt='o', color='red', capsize=5)
plt.errorbar(mean_data_c["Time"], mean_data_c["Flux"], yerr=mean_data_c["Error"], fmt='o', color='blue', capsize=5)
plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["STDEV"], fmt='o', color='orange', alpha = 0.2, capsize=5)
plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["STDEV"], fmt='o', color='cyan', alpha = 0.2, capsize=5)

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

fig_name = directory + supernova + '_flux_vs_time_clipped.pdf'

# Before plotting the figure, we save it
plt.savefig(fig_name)

# Now we display the figure itself!
plt.show()


