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


##################### DATA IMPORT #####################
# Now, we read in the transient data.
# Data file has columns separated by commas.
# We can read in the data as a set of dictionaries; a row contains a list of data pairs: a key and its associated value
# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).
# in case the filename needs to be changed, it's more accessible here.

supernova = "SN2019gwg"

filename = supernova + "_raw_data.csv"
filename_hawaii = supernova + ".csv"

# each row in the datafile becomes its own row; 'reader' contains many dictionaries. Each dictionary is an 'ordered dictionary'.

reader = csv.DictReader(open(filename))
reader_hawaii = csv.DictReader(open(filename_hawaii))

###################### DATA SORTING ######################

# Here, we create two empty dictionaries, that will contain as keys: the integer measurement times, and their associated values arrays, each element of which is a dictionary containing all the data about that measurement (float MJD, declination, RA, peakfit, etc.)

odict = {}
cdict = {}

odict_hawaii = {}
cdict_hawaii = {}

exposuretime = 30

# 'reader' is a massive array, with each element a dictionary. The following uses logical conditions to:
# 1. sort through which measurement have enough data to calculate flux
# 2. calculate the flux values for each measurement (and their associated uncertainties)
# 3. sort every measurement according to which wavelength filter was used (as these must be manipulated separately)
# The calculated flux values go into a new key, as do their associated uncertainties.
# The measurements are sorted into two dictionaries, one for each filter, which contain as keys the integer dates, and as values arrays, whose each element is a dictionary containing the data of a given measurement (the measurements are thus binned by day).
# For every dictionary (row) in the array 'reader' that contains all the observational data for a transient.

# Fo

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
                
			# The syntax here is: dictionary["new_key"].append(array)

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


# The Hawaii data from ATLAS is measured in a different way. We need to read in the data from a file, which contains the raw measured flux; we don't need to calculate the flux values from another 

for row in reader_hawaii:

	dflux_value_hawaii = float(row["duJy"])
	row["weight"] = dflux_value_hawaii**(-2)

	# If the data is measured with the orange filter:

	if row["F"] == 'o':

		try:
			odict_hawaii[int(float(row["###MJD"]))].append(dict(row))
		except KeyError as e:
			odict_hawaii[int(float(row["###MJD"]))] = []
			odict_hawaii[int(float(row["###MJD"]))].append(dict(row))

	# If the data is measured with the cyan filter:

	if row["F"] == 'c':

		try:
			cdict_hawaii[int(float(row["###MJD"]))].append(dict(row))
		except KeyError as e:
			cdict_hawaii[int(float(row["###MJD"]))] = []
			cdict_hawaii[int(float(row["###MJD"]))].append(dict(row))



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

	for row in value:

		print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
		time_sum_o = time_sum_o + float(row["mjd"])   
		flux_weight_product_sum_o = flux_weight_product_sum_o + (float(row["calc_flux"])*float(row["weight"]))
		weight_sum_o = weight_sum_o + float(row["weight"])         
		measurement_array_o.append(row["calc_flux"]) 
		uncertainty_array_o.append(row["calc_dflux"]) 
		time_array_o.append(row["mjd"]) 

		r_flux_o.append(float(row["calc_flux"])) 
		r_dev_o.append(float(row["calc_dflux"])) 
		r_time_o.append(float(row["mjd"])) 

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
print(raw_data_o["Time"])
print()
print("Flux Times - Orange")
print(raw_data_o["Flux"])
print()
print("Error Times - Orange")
print(raw_data_o["Error"])
print()
print("Raw Times - Cyan")
print(raw_data_c["Time"])
print()
print("Flux Times - Cyan")
print(raw_data_c["Flux"])
print()
print("Error Times - Cyan")
print(raw_data_c["Error"])
print()

##############################################################################################################

################################## HAWAII DATA - WEIGHTED MEAN CALCULATIONS ################################

mean_data_o_hawaii = {}
mean_data_c_hawaii = {}
raw_data_o_hawaii = {}
raw_data_c_hawaii = {}
print()
print("********** ORANGE ***********")
print()
r_time_o_hawaii = []
r_flux_o_hawaii = []
r_dev_o_hawaii = []
r_mag_o_hawaii = []
m_time_o_hawaii = []
w_flux_o_hawaii = []
s_dev_o_hawaii = []
num_o_hawaii = []
print()


for key, value in odict_hawaii.items():

	time_sum_o_hawaii = 0.0
	flux_weight_product_sum_o_hawaii = 0.0
	weight_sum_o_hawaii = 0.0
	stdv_o_hawaii = 0.0
	print()
	print("Day MJD")
	print(key)
	measurement_array_o_hawaii = []  
	uncertainty_array_o_hawaii = []
	time_array_o_hawaii = []

	for row in value:

		print(row["###MJD"], row["uJy"], row["duJy"])	
		time_sum_o_hawaii += float(row["###MJD"])
		flux_weight_product_sum_o_hawaii += (float(row["uJy"])*float(row["weight"]))
		weight_sum_o_hawaii += float(row["weight"])
		measurement_array_o_hawaii.append(float(row["uJy"])) 
		uncertainty_array_o_hawaii.append(float(row["duJy"])) 
		time_array_o_hawaii.append(row["###MJD"]) 

		r_flux_o_hawaii.append(float(row["uJy"])) 
		r_dev_o_hawaii.append(float(row["duJy"])) 
		r_time_o_hawaii.append(float(row["###MJD"])) 

	# The number of times summed is the length of the 'value' array.  
	print()	
	mean_time_o_hawaii = time_sum_o_hawaii / len(value)
	weighted_flux_o_hawaii = flux_weight_product_sum_o_hawaii / weight_sum_o_hawaii
	stdv_o_hawaii = standard_deviation(measurement_array_o_hawaii, uncertainty_array_o_hawaii)
	print("Mean Time Sum - Cyan")
	print(mean_time_o_hawaii)
	m_time_o_hawaii.append(mean_time_o_hawaii)
	print()
	print("Weighted Sum - Cyan")
	print(weighted_flux_o)
	w_flux_o_hawaii.append(weighted_flux_o_hawaii)
	print()
	print("Uncertainty Associated with Weighted Mean - Orange")
	print(stdv_o_hawaii)
	s_dev_o_hawaii.append(stdv_o_hawaii)
	print()
	print("Number of Data Points Averaged in this Day - Orange")
	print(len(value))
	number_o_hawaii = len(value)
	num_o_hawaii.append(number_o_hawaii)
	print()

mean_data_o_hawaii["Time"] = m_time_o_hawaii
mean_data_o_hawaii["Flux"] = w_flux_o_hawaii
mean_data_o_hawaii["Error"] = s_dev_o_hawaii
mean_data_o_hawaii["Number"] = num_o_hawaii

raw_data_o_hawaii["Time"] = r_time_o_hawaii
raw_data_o_hawaii["Flux"] = r_flux_o_hawaii
raw_data_o_hawaii["Error"] = r_dev_o_hawaii

print()
print("********** CYAN ***********")
print()
r_time_c_hawaii = []
r_flux_c_hawaii = []
r_dev_c_hawaii = []
r_mag_c_hawaii = []
m_time_c_hawaii = []
w_flux_c_hawaii = []
s_dev_c_hawaii = []
num_c_hawaii = []
print()


for key, value in cdict_hawaii.items():

	time_sum_c_hawaii = 0.0
	flux_weight_product_sum_c_hawaii = 0.0
	weight_sum_c_hawaii = 0.0
	stdv_c_hawaii = 0.0
	print()
	print("Day MJD")
	print(key)
	measurement_array_c_hawaii = []  
	uncertainty_array_c_hawaii = []
	time_array_c_hawaii = []

	for row in value:

		print(row["###MJD"], row["uJy"], row["duJy"])	
		time_sum_c_hawaii += float(row["###MJD"])
		flux_weight_product_sum_c_hawaii += (float(row["uJy"])*float(row["weight"]))
		weight_sum_c_hawaii += float(row["weight"])
		measurement_array_c_hawaii.append(float(row["uJy"])) 
		uncertainty_array_c_hawaii.append(float(row["duJy"])) 
		time_array_c_hawaii.append(row["###MJD"]) 

		r_flux_c_hawaii.append(float(row["uJy"])) 
		r_dev_c_hawaii.append(float(row["duJy"])) 
		r_time_c_hawaii.append(float(row["###MJD"])) 

	# The number of times summed is the length of the 'value' array.  
	print()	
	mean_time_c_hawaii = time_sum_c_hawaii / len(value)
	weighted_flux_c_hawaii = flux_weight_product_sum_c_hawaii / weight_sum_c_hawaii
	stdv_c_hawaii = standard_deviation(measurement_array_c_hawaii, uncertainty_array_c_hawaii)
	print("Mean Time Sum - Cyan")
	print(mean_time_c_hawaii)
	m_time_c_hawaii.append(mean_time_c_hawaii)
	print()
	print("Weighted Sum - Cyan")
	print(weighted_flux_c)
	w_flux_c_hawaii.append(weighted_flux_c_hawaii)
	print()
	print("Uncertainty Associated with Weighted Mean - Orange")
	print(stdv_c_hawaii)
	s_dev_c_hawaii.append(stdv_c_hawaii)
	print()
	print("Number of Data Points Averaged in this Day - Orange")
	print(len(value))
	number_c_hawaii = len(value)
	num_c_hawaii.append(number_c_hawaii)
	print()

mean_data_c_hawaii["Time"] = m_time_c_hawaii
mean_data_c_hawaii["Flux"] = w_flux_c_hawaii
mean_data_c_hawaii["Error"] = s_dev_c_hawaii
mean_data_c_hawaii["Number"] = num_c_hawaii

raw_data_c_hawaii["Time"] = r_time_c_hawaii
raw_data_c_hawaii["Flux"] = r_flux_c_hawaii
raw_data_c_hawaii["Error"] = r_dev_c_hawaii


for key, value in mean_data_o_hawaii.items():

	print(key)
	print(value)

print()

for key, value in mean_data_c_hawaii.items():

	print(key)
	print(value)

print()
print("Raw Times - Orange")
print(r_time_o_hawaii)
print()
print("Flux Times - Orange")
print(r_flux_o_hawaii)
print()
print("Error Times - Orange")
print(r_dev_o_hawaii)
print()
print("Raw Times - Cyan")
print(r_time_c_hawaii)
print()
print("Flux Times - Cyan")
print(r_flux_c_hawaii)
print()
print("Error Times - Cyan")
print(r_dev_c_hawaii)
print()
print()
print()
print()
print("Raw Times - Orange")
print(len(r_time_o_hawaii))
print()
print("Flux Times - Orange")
print(len(r_flux_o_hawaii))
print()
print("Error Times - Orange")
print(len(r_dev_o_hawaii))
print()
print("Raw Times - Cyan")
print(len(r_time_c_hawaii))
print()
print("Flux Times - Cyan")
print(len(r_flux_c_hawaii))
print()
print("Error Times - Cyan")
print(len(r_dev_c_hawaii))
print()








##################################### DATA WRITING #####################################

# Write the data plotted to a .txt file

filename_2 = '/home/mdobson/Archive/Objects/' + supernova + '/ATLAS/' + supernova + '_flux_weighted_mean_with_hawaii.txt'

data_raw_o = np.array([raw_data_o["Time"], raw_data_o["Flux"], raw_data_o["Error"]])
data_raw_c = np.array([raw_data_c["Time"], raw_data_c["Flux"], raw_data_c["Error"]])
data_wei_o = np.array([mean_data_o["Time"], mean_data_o["Flux"], mean_data_o["Error"], mean_data_o["Number"]])
data_wei_c = np.array([mean_data_c["Time"], mean_data_c["Flux"], mean_data_c["Error"], mean_data_c["Number"]])

data_raw_o_hawaii = np.array([raw_data_o_hawaii["Time"], raw_data_o_hawaii["Flux"], raw_data_o_hawaii["Error"]])
data_raw_c_hawaii = np.array([raw_data_c_hawaii["Time"], raw_data_c_hawaii["Flux"], raw_data_c_hawaii["Error"]])
data_wei_o_hawaii = np.array([mean_data_o_hawaii["Time"], mean_data_o_hawaii["Flux"], mean_data_o_hawaii["Error"], mean_data_o_hawaii["Number"]])
data_wei_c_hawaii = np.array([mean_data_c_hawaii["Time"], mean_data_c_hawaii["Flux"], mean_data_c_hawaii["Error"], mean_data_c_hawaii["Number"]])

# Transpose the data, to have it in multiple columns
data_raw_o = data_raw_o.T
data_raw_c = data_raw_c.T
data_wei_o = data_wei_o.T
data_wei_c = data_wei_c.T

data_raw_o_hawaii = data_raw_o_hawaii.T
data_raw_c_hawaii = data_raw_c_hawaii.T
data_wei_o_hawaii = data_wei_o_hawaii.T
data_wei_c_hawaii = data_wei_c_hawaii.T

with open(filename_2, 'w') as datafile_id:

# here, you open the ascii file
	
	np.savetxt(datafile_id, data_raw_o, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Orange Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_raw_c, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Cyan Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_o, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Orange Filter (Weighted Averages)', footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_c, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Cyan Filter (Weighted Averages)', footer='\n\n\n')

	np.savetxt(datafile_id, data_raw_o_hawaii, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Orange Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_raw_c_hawaii, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Cyan Filter (Raw data)',footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_o_hawaii, fmt=['%s','%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Orange Filter (Weighted Averages)', footer='\n\n\n')
	np.savetxt(datafile_id, data_wei_c_hawaii, fmt=['%s','%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Cyan Filter (Weighted Averages)', footer='\n\n\n')


##################################### DATA PLOTTING #####################################

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.
# Two graphs will be plotted on one figure: the data, and an analysis of the standard deviations

plt.figure("Flux vs Time")

plt.subplot(311)

plt.errorbar(mean_data_o["Time"], mean_data_o["Flux"], yerr=mean_data_o["Error"], fmt='o', color='red', capsize=5)
plt.errorbar(mean_data_c["Time"], mean_data_c["Flux"], yerr=mean_data_c["Error"], fmt='o', color='blue', capsize=5)
plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["Error"], fmt='o', color='orange', alpha = 0.2, capsize=5)
plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["Error"], fmt='o', color='cyan', alpha = 0.2, capsize=5)

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

plt.subplot(312)

plt.errorbar(mean_data_o_hawaii["Time"], mean_data_o_hawaii["Flux"], yerr=mean_data_o_hawaii["Error"], fmt='o', color='red', capsize=5)
plt.errorbar(mean_data_c_hawaii["Time"], mean_data_c_hawaii["Flux"], yerr=mean_data_c_hawaii["Error"], fmt='o', color='blue', capsize=5)
plt.errorbar(raw_data_o_hawaii["Time"], raw_data_o_hawaii["Flux"], yerr=raw_data_o_hawaii["Error"], fmt='o', color='orange', alpha = 0.2, capsize=5)
plt.errorbar(raw_data_c_hawaii["Time"], raw_data_c_hawaii["Flux"], yerr=raw_data_c_hawaii["Error"], fmt='o', color='cyan', alpha = 0.2, capsize=5)

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

plt.subplot(313)

plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["Error"], fmt='o', color='orange', alpha = 0.2, capsize=5)
plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["Error"], fmt='o', color='cyan', alpha = 0.2, capsize=5)
plt.errorbar(raw_data_o_hawaii["Time"], raw_data_o_hawaii["Flux"], yerr=raw_data_o_hawaii["Error"], fmt='o', color='red', alpha = 0.2, capsize=5)
plt.errorbar(raw_data_c_hawaii["Time"], raw_data_c_hawaii["Flux"], yerr=raw_data_c_hawaii["Error"], fmt='o', color='blue', alpha = 0.2, capsize=5)

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

fig_name = supernova + '_flux_vs_time_ATLAS_hawaii.pdf'

# And save it in the correct place
#my_path = os.path.abspath(/home/mdobson/Archive/Objects/SN2019muj)
plt.savefig('/home/mdobson/Archive/Objects/' + supernova + '/ATLAS/' + fig_name)

# Now we display the figure itself!
plt.show()



