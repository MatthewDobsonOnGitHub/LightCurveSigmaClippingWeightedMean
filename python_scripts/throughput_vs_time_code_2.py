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


############## DATA IMPORT ################

# Firstly, we need to read in the telescope data.
# Data file has columns of physical quantities, separated by commas. We can read in the data as a set of dictionaries; a row in the original data file contains a list of data pairs: a key and its associated value.
# We define the name of the telescope under examination as a string, to be concatenated to the file(s) that this code produces, and to identify which data files to read in. 

# This code will produce a plot of zero point magnitude (or some other quantifier of throughput) against time. We want to store it in a directory, which we define here:

directory = '/home/mdobson/Archive/ObservationData/' + telescope + '/ATLAS/'

# If this directory (file) does not already exist, we can created it using the code here.
	if not os.path.exists(directory):
		os.makedirs(directory)


# each row in the datafile becomes its own row; 'reader' contains many dictionaries. Each dictionary is an 'ordered dictionary'.
# In short, 'reader' is an array, with each element a dictionary, whose key:value pairs are the physical quantites and their values.
reader = csv.DictReader(open(filename))

###################### DATA SORTING ######################
# Here, we create two empty dictionaries, one for each filter used, that will contain as keys: the integer measurement times; and their associated values: arrays, each element of which is a dictionary containing data about a given measurement with the telescope.

odict = {}
cdict = {}

#'reader' is a massive array, with each element a dictionary. The following code extracts the time of measurement, the quantifier of throughput and the filter used for that measurement.

for row in reader:

	row["MJD-OBS"] = float(row["MJD-OBS"])
	row["MAGZPT"] = float(row["MAGZPT"])

	# If the measurement was made with the orange filter:
	if row["FILTER"] == 'o':

		try:
		# This appends the data of a single measurement to the dictionary appropriate to the filter that measurement was taken on. 
			odict[row["MJD-OBS"]].append(dict(row))

		except KeyError as e:
			odict[row["MJD-OBS"]] = []
			odict[row["MJD-OBS"]].append(dict(row))

	# If the measurement was made with the orange filter:
	if row["FILTER"] == 'c':

		try:
		# This appends the data of a single measurement to the dictionary appropriate to the filter that measurement was taken on. 
			cdict[row["MJD-OBS"]].append(dict(row))

		except KeyError as e:
			cdict[row["MJD-OBS"]] = []
			cdict[row["MJD-OBS"]].append(dict(row))

# By this stage, we have two dictionaries - one for each filter - that contain data about every measurement made for that telescope. Each key:value pair takes the format: mjd-date of obervation : data in a dictionary.

# Define empty arrays of time and throughput - for each filter.
time_o = []
time_c = []
magzpt_o = []
magzpt_c = []

for key, value in odict.items():

	# For set of data for a measurement
	for row in value:

		# Appends values to appropriate arrays
		time_o.append(float(row["MJD-OBS"]))
		magzpt_o.append(float(row["MAGZPT"]))

for key, value in cdict.items():

	# For set of data for a measurement
	for row in value:

		# Appends values to appropriate arrays
		time_c.append(float(row["MJD-OBS"]))
		magzpt_c.append(float(row["MAGZPT"]))


##################### DATA PLOTTING ########################
# Now, we plot the data on the graph. 
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.figure("Throughput vs Time - " + telescope, figsize = [7,7])

plt.errorbar(raw_data_o["Time"], raw_data_o["Flux"], yerr=raw_data_o["STDEV"], fmt='o', color='orange', alpha = 0.4, capsize=5)
plt.errorbar(raw_data_c["Time"], raw_data_c["Flux"], yerr=raw_data_c["STDEV"], fmt='o', color='c', alpha = 0.4, capsize=5)

plt.xlabel('MJD')
plt.ylabel('Transient Flux ($\mu$Jy)')

plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')

fig_name = directory + telescope + '_throughput_vs_time.pdf'

# Before plotting the figure, we save it
plt.savefig(fig_name)
plt.show(block=False)





