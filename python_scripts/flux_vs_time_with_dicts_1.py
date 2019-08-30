import numpy as np
import matplotlib.pyplot as plt
import math
import pylab
import csv
import sys
import statistics as stat


##################### DATA IMPORT ########################

# Now, we read in the transient data.
# Data file has columns separated by commas.
# We can read in the data as a set of dictionaries; a row contains a list of data pairs: a key and its associated value
# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).
# in case the filename needs to be changed, it's more accessible here.

supernova = "SN2019nar"

filename = supernova + "_raw_data.csv"

# each row in the datafile becomes its own row; 'reader' contains many dictionaries. Each dictionary is an 'ordered dictionary'.

reader = csv.DictReader(open(filename))


##################### DATA SORTING ########################

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



###### CLIPPING ######

# Some of the data points will be outliers compared to the others in their binned set, and need to be excised from the total dataset wihout compromising accuracy. To do this, we perform 'SIGMA CLIPPING'.

# Sigma Clipping involves calculating the median and standard deviation of all the flux values in a day, and determining how far from the median the datapoints are, in units of standard deviation. 

# Data points that lie beyond a certain range - a given multiple of standard deviation - are removed.

# The standard deviation and median are then recalculated, and clipping proceeds again with these new values of median and standard deviation. This is repeated until all datapoints lie within the required acceptable range from the most recently calculated median.

print("********** ORANGE ***********")
print()
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

	for row in value:

		print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
		time_sum_o = time_sum_o + float(row["mjd"])   
		flux_weight_product_sum_o = flux_weight_product_sum_o + (float(row["calc_flux"])*float(row["weight"]))
		weight_sum_o = weight_sum_o + float(row["weight"])         
		measurement_array_o.append(row["calc_flux"]) 

	# The number of times summed is the length of the 'value' array.  
	mean_time_o = time_sum_o / len(value)
	weighted_flux_o = flux_weight_product_sum_o / weight_sum_o
	print()
	print("Mean Time Sum - Orange")
	print(mean_time_o)	
	print()
	print("Weighted Sum - Orange")
	print(weighted_flux_o)	
	print()

	#med_c = stat.median(measurement_array_c)
	stdv_o = np.std(measurement_array_o)
	print("Uncertainty Associated with Weighted Mean - Orange")
	print(stdv_o)
	print()
	#print("Array of Flux")
	#print(median_array_c)
	#print()
	#print("Median of Binned Day (Cyan)")
	#print(med_c)
	#print()
	#print("Standard Deviation of Binned Day (Cyan)")
	#print(stdv_c)
	#print()


print("********** CYAN ***********")
print()
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

	for row in value:

		print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
		time_sum_c = time_sum_c + float(row["mjd"])   
		flux_weight_product_sum_c = flux_weight_product_sum_c + (float(row["calc_flux"])*float(row["weight"]))
		weight_sum_c = weight_sum_c + float(row["weight"])         
		measurement_array_c.append(row["calc_flux"]) 

	# The number of times summed is the length of the 'value' array.  
	mean_time_c = time_sum_c / len(value)
	weighted_flux_c = flux_weight_product_sum_c / weight_sum_c
	print()
	print("Mean Time Sum - Cyan")
	print(mean_time_c)	
	print()
	print("Weighted Sum - Cyan")
	print(weighted_flux_c)	
	print()
	
	#med_c = stat.median(measurement_array_c)
	stdv_c = np.std(measurement_array_c)
	print("Uncertainty Associated with Weighted Mean - Orange")
	print(stdv_c)
	print()
	#print("Array of Flux")
	#print(median_array_c)
	#print()
	#print("Median of Binned Day (Cyan)")
	#print(med_c)
	#print()
	#print("Standard Deviation of Binned Day (Cyan)")
	#print(stdv_c)
	#print()






