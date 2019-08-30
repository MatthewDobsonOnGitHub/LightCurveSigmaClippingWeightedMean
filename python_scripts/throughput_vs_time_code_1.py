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


def general_code(filename, determiner, telescope):


	##################### DATA IMPORT #####################

	# Firstly, we read in the transient data.
	# Data file has columns of physical quantities, separated by commas.
	# We can read in the data as a set of dictionaries; a row in the original data file contains a list of data pairs: a key and its associated value
	# We define the name of the supernova under study as a string, to be concatenated to the files this code produces, and to identify which data files to read in.


	# This code will produce a plot of flux vs time, and a text file of calculated data; both of these will be stored in a directory, which we define here. 
	directory = '/home/mdobson/Archive/ObservationData/' + telescope + '/ATLAS/'

	# If this directory (file) does not already exist, we can created it using the code here.
	if not os.path.exists(directory):
		os.makedirs(directory)

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
	# Just in case, a good thing to do would be to define the number of standard deviations beyond which data points should be clipped. Normally, it is one sigma, but sometimes it could be more.

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

	note = 'SN2019XXXXX forced photometry from ATLAS\n=============================================\nForced photometry values for individual 30s exposures in orange (o) and cyan (c) are provided in the long table. The measurements are are in a flux unit, not magnitudes. But conversion is simple. \nThe flux unit used is microJanskys, so AB mags are just\n\nm_AB  = -2.5*log(Flux * 10^-6) + 8.9\n\nThe error in m_AB can be calculated as above. Of course, will not be meangingful when the significance is < 3 sigma.\nIn those cases, the n-sigma upper limit (you can chose n) can be estimated from \n\n m_AB (n-sigma upper limit) > -2.5*log(n * Flux_error * 10^-6) + 8.9 \n\nIn the two other tables, the multiple measurements per night have been combined into a nightly mean. It is a weighted mean, with the points weighted by the inverse variance. The number of 30s exposures which were combined together is given in the last column. There are a small number of outliers, which you will see. You can ignore these rogue points toward the end of the lightcurve,  as you probably have good larger aperture coverage there (nothing  rogue at the critical early discovery phases).'

	with open(filename_2, 'w') as datafile_id:
	# here, you open the ascii file
		
		np.savetxt(datafile_id, data_raw_o, fmt=['%s','%s','%s'], delimiter='\t\t', header=note + '\n\n\n\nTime (MJD), Flux and Flux Error (microjanskys) for Orange Filter (Raw data)',footer='\n\n\n')
		np.savetxt(datafile_id, data_raw_c, fmt=['%s','%s','%s'], delimiter='\t\t', header='Time (MJD), Flux and Flux Error (microjanskys) for Cyan Filter (Raw data)',footer='\n\n\n')
		np.savetxt(datafile_id, data_wei_o, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Orange Filter (Weighted Averages)', footer='\n\n\n')
		np.savetxt(datafile_id, data_wei_c, fmt=['%s','%s','%s','%d'], delimiter='\t\t', header='Time (MJD), Flux, Flux Error (microjanskys) and No. Measurements per Weighted Mean for Cyan Filter (Weighted Averages)', footer='\n\n\n')


	##################################### DATA PLOTTING #####################################
	# Now, we plot the data on the graph. 
	# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
	# capsize determines the size of the error bar caps.
	# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.
	# Two graphs will be plotted on one figure: the data, and an analysis of the standard deviations

	plt.figure("Flux vs Time - " + supernova, figsize = [7,7])

	plt.subplots_adjust(hspace=0.7, wspace=0)

	plt.subplot(313)
	plt.subplot(313).set_title("Weighted Clipped Data")

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

	plt.subplot(312)
	plt.subplot(312).set_title("Weighted Data")

	plt.errorbar(mean_data_o["Time"], mean_data_o["Flux"], yerr=mean_data_o["Error"], fmt='o', color='red', capsize=5)
	plt.errorbar(mean_data_c["Time"], mean_data_c["Flux"], yerr=mean_data_c["Error"], fmt='o', color='blue', capsize=5)
	plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["STDEV"], fmt='o', color='orange', alpha = 0.2, capsize=5)
	plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["STDEV"], fmt='o', color='c', alpha = 0.2, capsize=5)

	plt.xlabel('MJD')
	plt.ylabel('Transient Flux ($\mu$Jy)')

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	plt.subplot(311)
	plt.subplot(311).set_title("Raw Data")

	plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["STDEV"], fmt='o', color='orange', alpha = 0.4, capsize=5)
	plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["STDEV"], fmt='o', color='c', alpha = 0.4, capsize=5)

	plt.xlabel('MJD')
	plt.ylabel('Transient Flux ($\mu$Jy)')

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	fig_name = directory + supernova + '_flux_vs_time_raw_weighted_clipped.pdf'

	# Before plotting the figure, we save it
	plt.savefig(fig_name)

	# Now we display the figure itself!
	# The block=False is to enable the following; we print the plot to the screen, hold for 2 seonds, then close. This allows the code to run for many data files without the user needing to manually perform running the code for each file -- enough time to glimpse each plot, but brief enough to ensure the code can run for many files within a reasonable timeframe.
	plt.show(block=False)
	plt.pause(1)
	plt.close()


#####################################################################################

# To call this code for multiple files, use the following code in a bash terminal:

#	for file in `ls *.csv`; do python test.py $file; done

# Note the backquote ` -- it means take the result of the command to list all the .csv files (the asterisk), and iterate through each one line by line. 'file' is the result of the `ls *.csv` and the 'do' loop is the oject which performs the iteration. (syntax: for "files" do "everything in the do loop" done (done closes the loop). A variable inside bash is represented by the dollar $ sign.

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

