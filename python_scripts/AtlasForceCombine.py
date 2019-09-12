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
import sys

#########################################################################
#######################	ATLASFORCECOMBINE CODE ##########################
##########################################################################



############### WEIGHTED MEAN AND SIGMA CLIPPING OF SUPERNOVA FLUX DATA ###############	

######### STANDARD DEVIATION FUNCTION #########
# The standard deviation is equal to the square root of the ratio of the sum of the square of the differences of each data point in a day compared to the mean, to the number of data points in a day minus one. We would normally use the built-in Python standard deviation function, but for some days we have only a single measurement, and wish to keep its intrinsic uncertainty as the 'standard deviation' of that day's weighted mean flux value.

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

		sigma = max(error) #Using max function to extract the value inside the one-element array
		return sigma


######### MEDIAN AND STANDARD DEVIATION FUNCTION ###########
def median_and_stdev(value, determiner):	

# To calculate the standard deviation of the daily flux measurements, we append them to an 	empty array, and so the same for their uncertainties and measurement times (to separate arrays, of course). The standard deviation function we defined at the start requires two inputs: values and  errors of the individual 30-second exposure measurements, in order to compute the error for a lone measurement in a day.

	measurement_clipping_array_o = []  
	uncertainty_clipping_array_o = []

# Resetting the values of sigma and median to zero, for every iteration.
	sigma = 0
	med = 0
	
	if determiner == 1:

		for row in value:

			measurement_clipping_array_o.append(row["calc_flux"]) 
			uncertainty_clipping_array_o.append(row["calc_dflux"]) 

	elif determiner == 2:

		for row in value:

			measurement_clipping_array_o.append(row["uJy"]) 
			uncertainty_clipping_array_o.append(row["duJy"]) 		
				
	# Calculates the standard deviation of all flux values in a day
	sigma = standard_deviation(measurement_clipping_array_o, uncertainty_clipping_array_o)

	# Calculates the median of all flux values in a day
	med = stat.median(measurement_clipping_array_o)

	return sigma, med


####### REMOVE ROW FUNCTION #######
def remove_row(value, sigma, median, determiner, number_sigma):

	empty_list = []

	if determiner == 1:

		for row in value:

			print()
			print("Median")
			print(median)
			print("Sigma")
			print(sigma)
			print(row["calc_flux"], row["mjd"], median+number_sigma*sigma, median-number_sigma*sigma)

			# If a measurement lies outside the n-sigma range from the median (i.e. it is an outlier)...
			if row["calc_flux"] < (median + (number_sigma*sigma)) and row["calc_flux"] > (median - (number_sigma*sigma)):
				print("ACCEPTABLE DATA POINT")
				empty_list.append(row)
			else:
				print("Doing some clipping")

	elif determiner == 2:

		for row in value:

			print()
			print("Median")
			print(median)
			print("Sigma")
			print(sigma)
			print(row["uJy"], row["###MJD"], median+number_sigma*sigma, median-number_sigma*sigma)

			# If a measurement lies outside the n-sigma range from the median (i.e. it is an outlier)...
			if row["uJy"] < (median + (number_sigma*sigma)) and row["uJy"] > (median - (number_sigma*sigma)):
				print("ACCEPTABLE DATA POINT")
				empty_list.append(row)
			else:
				print("Doing some clipping")

	return empty_list


####### WEIGHTED MEAN FUNCTION #######
def weighted_mean_function(dictionary, determiner):	

	raw_time = []
	raw_flux = []
	raw_dev = []
	mean_time = []
	weighted_flux = []
	standard_dev = []
	number = []
	new_error = []

	for key, value in dictionary.items():
	    
		time_sum_o = 0.0
		flux_weight_product_sum_o = 0.0
		weight_sum_o = 0.0
		stdv_o = 0.0
		sqdiff_o = 0.0
		print()
		print("Day MJD")
		print(key)
		measurement_array_o = []  
		uncertainty_array_o = []
		time_array_o = []

		if determiner == 1:

			for row in value:

				print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
				time_sum_o += float(row["mjd"])   
				flux_weight_product_sum_o += (float(row["calc_flux"])*float(row["weight"]))
				weight_sum_o += float(row["weight"])  
	       
				measurement_array_o.append(row["calc_flux"]) 
				uncertainty_array_o.append(row["calc_dflux"]) 
				time_array_o.append(row["mjd"]) 

				raw_flux.append(float(row["calc_flux"])) 
				raw_dev.append(float(row["calc_dflux"])) 
				raw_time.append(float(row["mjd"])) 

		elif determiner == 2:

			for row in value:

				print(row["###MJD"], row["uJy"], row["duJy"], row["weight"])   
				time_sum_o += float(row["###MJD"])   
				flux_weight_product_sum_o += (float(row["uJy"])*float(row["weight"]))
				weight_sum_o += float(row["weight"])  
	       
				measurement_array_o.append(row["uJy"]) 
				uncertainty_array_o.append(row["duJy"]) 
				time_array_o.append(row["###MJD"]) 

				raw_flux.append(float(row["uJy"])) 
				raw_dev.append(float(row["duJy"])) 
				raw_time.append(float(row["###MJD"])) 

	  
		print()	
		mean_time_o = time_sum_o / len(value)
		weighted_flux_o = flux_weight_product_sum_o / weight_sum_o
		stdv_o = standard_deviation(measurement_array_o, uncertainty_array_o)

		mean_time.append(mean_time_o)
		weighted_flux.append(weighted_flux_o)
		standard_dev.append(stdv_o)
		number.append(len(value))

		if len(value) > 1:

			if determiner == 1:

				for row in value:

					sqdiff_o += float(row["weight"])*((weighted_flux_o - float(row["calc_flux"]))**2)

			elif determiner == 2:

				for row in value:

					sqdiff_o += float(row["weight"])*((weighted_flux_o - float(row["uJy"]))**2)

			ratio_o = (len(value)-1)/ len(value)
			weighted_variance_o = sqdiff_o/(ratio_o*weight_sum_o)
			weighted_standard_deviation_o = weighted_variance_o**(1/2) 
			new_error.append(weighted_standard_deviation_o)


# Sometimes, we will have a single data point for a day. The weighted standard deviation equation cannot cope with this, as it causes division by zero. For such cases, the intrinsic error for that lone datapoint is used for the 'weighted error', and its value appended to the latter's appropriate array.


		elif len(value) == 1:

			stdv_o = standard_deviation(measurement_array_o, uncertainty_array_o)
			new_error.append(stdv_o)

	return raw_time, raw_flux, raw_dev, mean_time, weighted_flux, standard_dev, number, new_error


####### CLIPPING FUNCTION ########	
	
def clipping_function(input_dictionary, output_dictionary, determiner, number_sigma):

	# We loop through all the days of measurements, and loop through all the measurements taken on each day (nested loops).

	for key, value in input_dictionary.items():

		# Define the number of points per day in the initial, unclipped data.
		list_length = len(value)

		# Define the number of points per day in the clipped data - this will be subject to change of value with each iteration
		list_length_new = len(value)

		# Create an array of list lengths, starting with original list length
		length_array = [list_length]

		# Finding the standard deviation and median values for each day; the function returns two variables, and assigns the values in a specific order, so be careful!
		sigma, med = median_and_stdev(value, determiner)

		# Performs the clipping an initial first time, calling the function 'remove_row' to remove an outlying data point (if one exists).
		new_list = remove_row(value, sigma, med, determiner, number_sigma)

		# Appends the length of the new, clipped list to the array.
		length_array.append(len(new_list))

		print(length_array)

		while(True): # Infinite loop, until the last two elements in the array are of equal length

			# calculate new s.d. and median for every clipping iteration

			sigma, med = median_and_stdev(new_list, determiner)

			# If no more points have been clipped (i.e. the number of unclipped points in a day after passing the data through the clipping function is the same), we want the algorithm to stop for a given day.
			if length_array[-1] == length_array[-2]:

				# The newest list is appended to the empty dictionary for clipped data, with the same key as the original, unclipped data.

				output_dictionary[key] = new_list
				print("Break Out")			
				print(length_array)
				output_dictionary[key] = new_list
				break

			# If clipping has been performed (i.e. if the new clipped list is shorter than before), we want this to continue.

			else:
				# perform clipping again
				new_list = remove_row(value, sigma, med, determiner, number_sigma)
				# newest list added to the clipped data dictionary (it seemingly overwrites the original array)
				# number of remaining data points calculated, and appended to the appropriate array
				length_array.append(len(new_list))
				print(length_array)
				sigma, med = median_and_stdev(new_list, determiner)
				output_dictionary[key] = new_list

	return output_dictionary

def general_code(filename, determiner, supernova):


	##################### DATA IMPORT #####################

	# Firstly, we read in the transient data.
	# Data file has columns of physical quantities, separated by commas.
	# We can read in the data as a set of dictionaries; a row in the original data file contains a list of data pairs: a key and its associated value
	# We define the name of the supernova under study as a string, to be concatenated to the files this code produces, and to identify which data files to read in.

	# However, there are two formats fo data which can be used: 1) the Forced Photometry data taken from the ATLAS website; or 2) the Forced Photometry data that is output from the forced.sh file. The file contents are different; the first requires calculation of flux from other quantities in the file, the second already has accurate flux values in the file which only need to be read.

	# each row in the datafile becomes its own row; 'reader' contains many dictionaries. Each dictionary is an 'ordered dictionary'.
	# In short, 'reader' is an array, with each element a dictionary, whose key:value pairs are the physical quantites and their values.

	if determiner == 1:

		reader = csv.DictReader(open(filename))

	elif determiner == 2:

		reader = csv.DictReader(open(filename), delimiter=',', skipinitialspace=True)



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

	if determiner == 1:

		for row in reader:
		    
		    	# Ensures that a given observation has enough data from which the observed flux can be calculated.
		    
			if row["mjd"] != 'None' and row["peakfit"] != 'None' and row["major"] != 'None' and row["minor"] != 'None' and row["zp"] != 'None' and row["apfit"] != 'None':
			
				# Here, we calculated the flux and its uncertainty for every measurement, and append the values as new key:value pairs to that measurement's dictionary.
			
				index = (float(row["zp"]) + float(row["apfit"]))/(-2.5) + 9.56

				flux_numerator = float(row["peakfit"])*float(row["major"])*float(row["minor"])
				flux_value = (flux_numerator/exposuretime)*10**index
				row["calc_flux"] = flux_value
			
				dflux_numerator = float(row["dpeak"])*float(row["major"])*float(row["minor"])
				dflux_value = (dflux_numerator/exposuretime)*10**index
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

	elif determiner == 2:

		for row in reader:

			row["###MJD"] = float(row["###MJD"])
			row["uJy"] = float(row["uJy"])
			row["duJy"] = float(row["duJy"])

			dflux_value = float(row["duJy"])
			row["weight"] = dflux_value**(-2)

			if row["F"] == 'o':

				try:
					odict[int(float(row["###MJD"]))].append(dict(row))
				except KeyError as e:
					odict[int(float(row["###MJD"]))] = []
					odict[int(float(row["###MJD"]))].append(dict(row))

			if row["F"] == 'c':

				try:
					cdict[int(float(row["###MJD"]))].append(dict(row))
				except KeyError as e:
					cdict[int(float(row["###MJD"]))] = []
					cdict[int(float(row["###MJD"]))].append(dict(row))


	###################### CLIPPING #######################

	# Within a given day, some of the measurements will have outlying flux values. We want to clip the data - removing the outlying points in a given day, without affecting the accuracy of the data.
	# There is a known method of doing this: we calculate the standard deviation and the median of every measurement for a given day, and check to see whether every data point lies within one s.d. from the median. If not, any outlying points (beyond 3 s.d. of the median) are discarded.
	# The process is repeated; a new s.d. and median calculated for the remaining points - and continues until every point for a day lies within 1 s.d. from the median.
	# Ideally, we would use a do...while loop, but that is not possible with the Python language. Instead, we write the code to be run first, then duplicate it in a while loop that follows the initial instance of code. In a sense, the loop performs an initial round of clipping and then checks whether or not to proceed.
	# Just in case, a good thing to do would be to define the number of standard deviations beyond which data points should be clipped. Normally, it is three sigma, but sometimes it could be more.

	number_sigma = 3

	# We create new copies of the dictionaries that contain the data, in order to preserve the read-in data, should something happen in the code that causes it to be edited.
	clipping_data_o = odict.copy()
	clipping_data_c = cdict.copy()

	# We define two empty dictionaries (one for each filter), where the remaining data points will be stored
	clipped_data_o = {}
	clipped_data_c = {}

	clipped_data_o = clipping_function(clipping_data_o, clipped_data_o, determiner, number_sigma)
	clipped_data_c = clipping_function(clipping_data_c, clipped_data_c, determiner, number_sigma)


	###### WEIGHTED MEAN CALCULATIONS ######
	# Here, we make the calculations of the weighted mean of the flux values in a given day.
	# Here, we define two empty dictionaries, one for each filter, which will contain, for a given weighted mean measurement, the measurement time, flux value, flux uncertainty, and number of points used to make the weighted mean.
	# Their keys will be time, flux, error and number, and their values the arrays of these values, whose equivalent nth elements correspond to a given nth measurement. 

	mean_data_o = {}
	mean_data_c = {}
	raw_data_o = {}
	raw_data_c = {}

	clipped_mean_data_o = {}
	clipped_mean_data_c = {}
	clipped_raw_data_o = {}
	clipped_raw_data_c = {}


	# ORANGE #
	raw_data_o["Time"], raw_data_o["Flux"], raw_data_o["STDEV"], mean_data_o["Time"], mean_data_o["Flux"], mean_data_o["STDEV"],  mean_data_o["Number"], mean_data_o["Error"] = weighted_mean_function(clipping_data_o, determiner)

	clipped_raw_data_o["Time"], clipped_raw_data_o["Flux"], clipped_raw_data_o["STDEV"], clipped_mean_data_o["Time"], clipped_mean_data_o["Flux"], clipped_mean_data_o["STDEV"],  clipped_mean_data_o["Number"], clipped_mean_data_o["Error"] = weighted_mean_function(clipped_data_o, determiner)

	# CYAN #
	raw_data_c["Time"], raw_data_c["Flux"], raw_data_c["STDEV"], mean_data_c["Time"], mean_data_c["Flux"], mean_data_c["STDEV"],  mean_data_c["Number"], mean_data_c["Error"] = weighted_mean_function(clipping_data_c, determiner)

	clipped_raw_data_c["Time"], clipped_raw_data_c["Flux"], clipped_raw_data_c["STDEV"], clipped_mean_data_c["Time"], clipped_mean_data_c["Flux"], clipped_mean_data_c["STDEV"],  clipped_mean_data_c["Number"], clipped_mean_data_c["Error"] = weighted_mean_function(clipped_data_c, determiner)



	##################################### DATA WRITING #####################################
	# Write the data plotted to a .txt file

	filename_2 = supernova + '_flux_weighted_mean_clipped.txt'

	data_raw_o = np.array([raw_data_o["Time"], raw_data_o["Flux"], raw_data_o["STDEV"]])
	data_raw_c = np.array([raw_data_c["Time"], raw_data_c["Flux"], raw_data_c["STDEV"]])
	data_wei_o = np.array([mean_data_o["Time"], mean_data_o["Flux"], mean_data_o["Error"], mean_data_o["Number"]])
	data_wei_c = np.array([mean_data_c["Time"], mean_data_c["Flux"], mean_data_c["Error"], mean_data_c["Number"]])
	data_clp_o = np.array([clipped_mean_data_o["Time"], clipped_mean_data_o["Flux"], clipped_mean_data_o["Error"], clipped_mean_data_o["Number"]])
	data_clp_c = np.array([clipped_mean_data_c["Time"], clipped_mean_data_c["Flux"], clipped_mean_data_c["Error"], clipped_mean_data_c["Number"]])


	# Transpose the data, to have it in multiple columns
	data_raw_o = data_raw_o.T
	data_raw_c = data_raw_c.T
	data_wei_o = data_wei_o.T
	data_wei_c = data_wei_c.T
	data_clp_o = data_clp_o.T
	data_clp_c = data_clp_c.T


	note = 'Forced photometry from ATLAS\n=============================================\nForced photometry values for individual 30s exposures in orange (o) and cyan (c) are provided in the two former (long) tables. The measurements are are in a flux unit, not magnitudes. But conversion is simple. \nThe flux unit used is microJanskys, so AB mags are just\n\n\tm_AB  = -2.5*log(Flux * 10^-6) + 8.9\n\nThe error in m_AB can be calculated as above. Of course, will not be meangingful when the significance is < 3 sigma.\nIn those cases, the n-sigma upper limit (you can chose n) can be estimated from \n\n\tm_AB (n-sigma upper limit) > -2.5*log(n * Flux_error * 10^-6) + 8.9 \n\nIn the middle two tables, the multiple measurements per night have been combined into a nightly mean. It is a weighted mean, with the points weighted by the inverse variance. \n\n In the latter two tables, the multiple measurements per night have been sigma-clipped, with points lying beyond 3 sigma from the nightly mean removed. The remaining points have been combined into a weighted mean, with points weighted by inverse variance (as before). \n\n For the latter four tables, the number of 30s exposures which were combined together for each night is given in the last column. There are a small number of outliers which remain after 3-sigma clipping, which you will see.'

	with open(filename_2, 'w') as datafile_id:
	# here, you open the ascii file
		
		np.savetxt(datafile_id, data_raw_o, fmt=['%.5f','%f','%f'], delimiter='\t\t', header=note + '\n\n\n\nTime (MJD), Flux and Flux Error (microjanskys) for Orange Filter (Individual 30-second exposure data)',footer='\n\n\n')
		np.savetxt(datafile_id, data_raw_c, fmt=['%.5f','%f','%f'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Cyan Filter (Individual 30-second exposure data)',footer='\n\n\n')
		np.savetxt(datafile_id, data_wei_o, fmt=['%.5f','%f','%f','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Orange Filter (Weighted Averages)', footer='\n\n\n')
		np.savetxt(datafile_id, data_wei_c, fmt=['%.5f','%f','%f','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Cyan Filter (Weighted Averages)', footer='\n\n\n')
		np.savetxt(datafile_id, data_clp_o, fmt=['%.5f','%f','%f','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Orange Filter (Clipped Weighted Averages)', footer='\n\n\n')
		np.savetxt(datafile_id, data_clp_c, fmt=['%.5f','%f','%f','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Cyan Filter (Clipped Weighted Averages)', footer='\n\n\n')



	##################################### DATA PLOTTING #####################################
	# Now, we plot the data on the graph. 
	# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
	# capsize determines the size of the error bar caps.
	# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.
	# Two graphs will be plotted on one figure: the data, and an analysis of the standard deviations

	plt.figure("Flux vs Time - " + supernova, figsize = [7,7])

	plt.subplots_adjust(hspace=0.7, wspace=0)

	plt.subplot(311)
	plt.subplot(311).set_title("Individual 30s Exposure Flux")

	plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["STDEV"], fmt='o', color='orange', alpha = 0.4, capsize=5)
	plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["STDEV"], fmt='o', color='c', alpha = 0.4, capsize=5)

	plt.xlabel('MJD')
	plt.ylabel('Transient Flux ($\mu$Jy)')

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	plt.subplot(312)
	plt.subplot(312).set_title("Weighted Mean Flux")

	plt.errorbar(mean_data_o["Time"], mean_data_o["Flux"], yerr=mean_data_o["Error"], fmt='o', color='red', capsize=5)
	plt.errorbar(mean_data_c["Time"], mean_data_c["Flux"], yerr=mean_data_c["Error"], fmt='o', color='blue', capsize=5)
	plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["STDEV"], fmt='o', color='orange', alpha = 0.2, capsize=5)
	plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["STDEV"], fmt='o', color='c', alpha = 0.2, capsize=5)

	plt.xlabel('MJD')
	plt.ylabel('Transient Flux ($\mu$Jy)')

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	plt.subplot(313)
	plt.subplot(313).set_title("Weighted Mean Flux with 3-Sigma Clipping")

	plt.errorbar(clipped_mean_data_o["Time"], clipped_mean_data_o["Flux"], yerr=clipped_mean_data_o["Error"], fmt='o', color='red', capsize=5)
	plt.errorbar(clipped_mean_data_c["Time"], clipped_mean_data_c["Flux"], yerr=clipped_mean_data_c["Error"], fmt='o', color='blue', capsize=5)
	plt.errorbar(clipped_raw_data_o["Time"], clipped_raw_data_o["Flux"], yerr=clipped_raw_data_o["STDEV"], fmt='o', color='orange', alpha = 0.2, capsize=5)
	plt.errorbar(clipped_raw_data_c["Time"], clipped_raw_data_c["Flux"], yerr=clipped_raw_data_c["STDEV"], fmt='o', color='c', alpha = 0.2, capsize=5)

	# Setting the titles for the x- and y-axes.
	plt.xlabel('MJD')
	plt.ylabel('Transient Flux ($\mu$Jy)')
	# We can also set gridlines and tick marks on the graph.
	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	#plt.xlim([,])
	#plt.ylim([-100,325])

	fig_name = supernova + '_flux_vs_time_weighted_clipped.pdf'

	# Before plotting the figure, we save it
	plt.savefig(fig_name)

	# Now we display the figure itself!
	# The block=False is to enable the following; we print the plot to the screen, hold for 2 seonds, then close. This allows the code to run for many data files without the user needing to manually perform running the code for each file -- enough time to glimpse each plot, but brief enough to ensure the code can run for many files within a reasonable timeframe.
	plt.show()	
	#plt.show(block=False)
	#plt.pause(1)
	#plt.close()


#####################################################################################

# To call this code for multiple files of a given 'format', use the following code in a bash terminal:

#	for file in `ls *.format`; do python AtlasForceCombine.py $file; done

# Note the backquote ` -- it means take the result of the command to list all the .format files (the asterisk), and iterate through each one line by line. 'file' is the result of the `ls *.csv` and the 'do' loop is the oject which performs the iteration. (syntax: for "files" do "everything in the do loop" done (done closes the loop). A variable inside bash is represented by the dollar $ sign.

# Defining the code this way allows it to run on multiple files in one sitting; one need type into the command line

#	python codename datafile

# to run the code of name 'codename' on a file called 'datafile'	
	

def main(argv=None):
	if argv is None:
		argv = sys.argv

# The number of arguments to the code can be set to any given number; we set it to 1, as only one file need be entered at a time.
	usage = "Usage: %s <SN filename>" % argv[0]
	if len(argv) != 2:
		sys.exit(usage)

	filename = str(argv[1])

# The data file can be one of either two formats:
#	1. Forced photometry downloaded from the ATLAS website
#	2. Forced photometry output from the forced.sh bash script code
# Both these formats contain different data, in a different format, and so the code must be able to run for both these formats.
# To determine what format the data files are, we make use of the .readlines() function: this turns the file into an array of strings, with every line in a file being itself a string. We select the first element in this array -- the first line in the file -- and search for certain headers that indicate the file format. A determining variable takes a value depending on the format, and the code will run in accordance with that given format.

	f = open(filename)
	firstLine = f.readlines()[0]
    
	if "###MJD" in firstLine:

		determiner = 2

	elif "mjd" in firstLine:

		determiner = 1

	else:

		determiner = 0
		print("File not in correct format")


	dot = filename.index('.')

	supernova = str(filename[0:dot])

	print()
	print("SUPERNOVA NAME:")
	print(supernova)
	print()

	general_code(filename, determiner, supernova)

	return


# The double underscore is a python-ism, and has special meaning.
if __name__ == '__main__':

	main()

