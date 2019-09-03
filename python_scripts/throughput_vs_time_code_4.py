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



###############################	ZERO POINT MAGNITUDE #####################################

def general_code1(filename, telescope):

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

		row["FILE"] = row["FILE"].strip()
		row["MJD-OBS"] = row["MJD-OBS"].strip()
		row["CAMID"] = row["CAMID"].strip()
		row["FILTER"] = row["FILTER"].strip()
		row["MAGZPT"] = row["MAGZPT"].strip()
		row["MAG5SIG"] = row["MAG5SIG"].strip()
		row["AIRMASS"] = row["AIRMASS"].strip()
		row["SEEING"] = row["SEEING"].strip()
		row["SKYMAG"] = row["SKYMAG"].strip()
		row["CLOUD"] = row["CLOUD"].strip()
		row["MOONSKY"] = row["MOONSKY"].strip()
		row["MANGLE"] = row["MANGLE"].strip()

		if not row["MAGZPT"].strip():
			continue
		if not row["SEEING"].strip():
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
	data_o["Zero Point Magnitude"] = magzpt_o
	data_c["Zero Point Magnitude"] = magzpt_c

	#print(data_o["Time (MJD)"])
	#print(data_c["Time (MJD)"])
	#print(data_o["Magnitude ZeroPoint"])
	#print(data_c["Magnitude ZeroPoint"])


	##################### DATA PLOTTING ########################
	# Now, we plot the data on the graph. 
	# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

	plt.figure("Throughput (Zero Point Magnitude) vs Time - " + telescope)

	plt.errorbar(data_o["Time (MJD)"], data_o["Zero Point Magnitude"], fmt='o', color='orange', alpha = 0.4, markersize = 0.5)
	plt.errorbar(data_c["Time (MJD)"], data_c["Zero Point Magnitude"], fmt='o', color='c', alpha = 0.4, markersize = 0.5)

	plt.xlabel('MJD')
	plt.ylabel('Zero Point Magnitude')

	#plt.xlim((,))
	plt.ylim((21,23))

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	fig_name = directory + telescope + '_throughput_(magzpt)_vs_time.png'

	# Before plotting the figure, we save it
	plt.savefig(fig_name)
	plt.show()





###############################	5 SIGMA MAGNITUDE #####################################


def general_code2(filename, telescope):

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

		row["FILE"] = row["FILE"].strip()
		row["MJD-OBS"] = row["MJD-OBS"].strip()
		row["CAMID"] = row["CAMID"].strip()
		row["FILTER"] = row["FILTER"].strip()
		row["MAGZPT"] = row["MAGZPT"].strip()
		row["MAG5SIG"] = row["MAG5SIG"].strip()
		row["AIRMASS"] = row["AIRMASS"].strip()
		row["SEEING"] = row["SEEING"].strip()
		row["SKYMAG"] = row["SKYMAG"].strip()
		row["CLOUD"] = row["CLOUD"].strip()
		row["MOONSKY"] = row["MOONSKY"].strip()
		row["MANGLE"] = row["MANGLE"].strip()

		if not row["MAGZPT"].strip():
			continue
		if not row["MAG5SIG"].strip():
			continue

		row["MJD-OBS"] = float(row["MJD-OBS"])
		row["MAG5SIG"] = float(row["MAG5SIG"])

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

	# By this stage, we have two dictionaries - one for each filter - that contain data about every measurement made for that telescope. Each key:value pair takes the format: mjd-date of obervation : data in a dictionary. Now, we define two empty dictionaries for the extracted data of time and throughput. 

	data_o = {}
	data_c = {}

	# Define empty arrays of time and throughput - for each filter.
	time_o = []
	time_c = []
	mag5sig_o = []
	mag5sig_c = []

	for key, value in odict.items():

		# For set of data for a measurement
		for row in value:

			# Appends values to appropriate arrays
			time_o.append(float(row["MJD-OBS"]))
			mag5sig_o.append(float(row["MAG5SIG"]))

	for key, value in cdict.items():

		# For set of data for a measurement
		for row in value:

			# Appends values to appropriate arrays
			time_c.append(float(row["MJD-OBS"]))
			mag5sig_c.append(float(row["MAG5SIG"]))

	data_o["Time (MJD)"] = time_o
	data_c["Time (MJD)"] = time_c
	data_o["5 Sigma Magnitude"] = mag5sig_o
	data_c["5 Sigma Magnitude"] = mag5sig_c

	#print(data_o["Time (MJD)"])
	#print(data_c["Time (MJD)"])
	#print(data_o["Magnitude ZeroPoint"])
	#print(data_c["Magnitude ZeroPoint"])


	##################### DATA PLOTTING ########################
	# Now, we plot the data on the graph. 
	# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

	plt.figure("Throughput (5 Sigma Magnitude) vs Time - " + telescope)

	plt.errorbar(data_o["Time (MJD)"], data_o["5 Sigma Magnitude"], fmt='o', color='orange', alpha = 0.4, markersize = 0.5)
	plt.errorbar(data_c["Time (MJD)"], data_c["5 Sigma Magnitude"], fmt='o', color='c', alpha = 0.4, markersize = 0.5)

	plt.xlabel('MJD')
	plt.ylabel('5 Sigma Magnitude')

	#plt.xlim((,))
	plt.ylim((10,20))

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	fig_name = directory + telescope + '_throughput_(mag5sig)_vs_time.png'

	# Before plotting the figure, we save it
	plt.savefig(fig_name)
	plt.show()



###############################	SEEING #####################################

def general_code3(filename, telescope):

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

		row["FILE"] = row["FILE"].strip()
		row["MJD-OBS"] = row["MJD-OBS"].strip()
		row["CAMID"] = row["CAMID"].strip()
		row["FILTER"] = row["FILTER"].strip()
		row["MAGZPT"] = row["MAGZPT"].strip()
		row["MAG5SIG"] = row["MAG5SIG"].strip()
		row["AIRMASS"] = row["AIRMASS"].strip()
		row["SEEING"] = row["SEEING"].strip()
		row["SKYMAG"] = row["SKYMAG"].strip()
		row["CLOUD"] = row["CLOUD"].strip()
		row["MOONSKY"] = row["MOONSKY"].strip()
		row["MANGLE"] = row["MANGLE"].strip()

		if not row["MAGZPT"].strip():
			continue
		if not row["SEEING"].strip():
			continue

		row["MJD-OBS"] = float(row["MJD-OBS"])
		row["SEEING"] = float(row["SEEING"])

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

	# By this stage, we have two dictionaries - one for each filter - that contain data about every measurement made for that telescope. Each key:value pair takes the format: mjd-date of obervation : data in a dictionary. Now, we define two empty dictionaries for the extracted data of time and throughput. 

	data_o = {}
	data_c = {}

	# Define empty arrays of time and throughput - for each filter.
	time_o = []
	time_c = []
	seeing_o = []
	seeing_c = []

	for key, value in odict.items():

		# For set of data for a measurement
		for row in value:

			# Appends values to appropriate arrays
			time_o.append(float(row["MJD-OBS"]))
			seeing_o.append(float(row["SEEING"]))

	for key, value in cdict.items():

		# For set of data for a measurement
		for row in value:

			# Appends values to appropriate arrays
			time_c.append(float(row["MJD-OBS"]))
			seeing_c.append(float(row["SEEING"]))

	data_o["Time (MJD)"] = time_o
	data_c["Time (MJD)"] = time_c
	data_o["Seeing"] = seeing_o
	data_c["Seeing"] = seeing_c

	#print(data_o["Time (MJD)"])
	#print(data_c["Time (MJD)"])
	#print(data_o["Magnitude ZeroPoint"])
	#print(data_c["Magnitude ZeroPoint"])


	##################### DATA PLOTTING ########################
	# Now, we plot the data on the graph. 
	# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

	plt.figure("Throughput (Seeing) vs Time - " + telescope)

	plt.errorbar(data_o["Time (MJD)"], data_o["Seeing"], fmt='o', color='orange', alpha = 0.4, markersize = 0.5)
	plt.errorbar(data_c["Time (MJD)"], data_c["Seeing"], fmt='o', color='c', alpha = 0.4, markersize = 0.5)

	plt.xlabel('MJD')
	plt.ylabel('Seeing')

	#plt.xlim((,))
	plt.ylim((3,15))

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	fig_name = directory + telescope + '_throughput_(seeing)_vs_time.png'

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

	print()
	print("Select Measure of Throughput:")
	print("1. Zero Point Magnitude")
	print("2. 5 Sigma Magnitude")
	print("3. 'Seeing'")
	print("Input 1, 2 or 3 (no spaces)")

	measure = input()

	if confirm == 'y':

		if measure == '1':

			general_code1(filename, telescope)

		if measure == '2':

			general_code2(filename, telescope)

		if measure == '3':

			general_code3(filename, telescope)

	return


# The double underscore is a python-ism, and has special meaning.
if __name__ == '__main__':

	main()
