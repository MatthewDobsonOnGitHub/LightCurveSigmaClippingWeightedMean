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

def general_code(filename, telescope):

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

	reader = csv.DictReader(open(filename), delimiter='\t', skipinitialspace=False)

	###################### DATA SORTING ######################
	# Here, we create two empty dictionaries, one for each filter used, that will contain as keys: the integer measurement times; and their associated values: arrays, each element of which is a dictionary containing data about a given measurement with the telescope.

	odict = {}
	cdict = {}

	#'reader' is a massive array, with each element a dictionary. The following code extracts the time of measurement, the quantifier of throughput and the filter used for that measurement.

	for row in reader:

		row["FILTER"] = row["FILTER"].strip()

		#for k,v in row[0].items():
		#	row[0][k]=v.strip()

		if not row["MAGZPT"].strip():
			continue

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

		print(row)
		#sys.exit(0)

	# By this stage, we have two dictionaries - one for each filter - that contain data about every measurement made for that telescope. Each key:value pair takes the format: mjd-date of obervation : data in a dictionary. Now, we define two empty dictionaries for the extracted data of time and throughput. 

	data_o = {}
	data_c = {}

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

	data_o["Time (MJD)"] = time_o
	data_c["Time (MJD)"] = time_c
	data_o["Magnitude ZeroPoint"] = magzpt_o
	data_c["Magnitude ZeroPoint"] = magzpt_c

	print(data_o["Time (MJD)"])
	print(data_c["Time (MJD)"])
	print(data_o["Magnitude ZeroPoint"])
	print(data_c["Magnitude ZeroPoint"])


	##################### DATA PLOTTING ########################
	# Now, we plot the data on the graph. 
	# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

	plt.figure("Throughput vs Time - " + telescope, figsize = [7,7])

	plt.plot(data_o["Time (MJD)"], data_o["Magnitude ZeroPoint"], 'o', color='orange', alpha = 0.4)
	plt.plot(data_c["Time (MJD)"], data_c["Magnitude ZeroPoint"], 'o', color='c', alpha = 0.4)

	plt.xlabel('MJD')
	plt.ylabel('Transient Flux ($\mu$Jy)')

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	fig_name = directory + telescope + '_throughput_vs_time.pdf'

	# Before plotting the figure, we save it
	plt.savefig(fig_name)
	plt.show()

def main(argv=None):
	if argv is None:
		argv = sys.argv

# The number of arguments to the code can be set to any given number; we set it to 1, as only one file need be entered at a time.
	usage = "Usage: %s <SN filename>" % argv[0]
	if len(argv) != 2:
		sys.exit(usage)

	filename = str(argv[1])

	f = open(filename)
	firstLine = f.readlines()[0]
	print(firstLine)

	telescope = input("Enter name of telescope under check: ")

	print()
	print("Confirm telescope name:")
	print(telescope)
	print("Continue? y/n")
	print()

	confirm = input()

	if confirm == 'y':

		general_code(filename, telescope)

	return


# The double underscore is a python-ism, and has special meaning.
if __name__ == '__main__':

	main()
