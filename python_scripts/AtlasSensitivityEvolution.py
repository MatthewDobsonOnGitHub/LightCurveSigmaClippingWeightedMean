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

def general_code(filename1, filename2, telescope, firstLine1, firstLine2, throughput, timeKey, delimitingcharacter, throughput_label):

	############## DATA IMPORT ################

	# Firstly, we need to read in the telescope data.
	# Data file has columns of physical quantities, separated by commas. We can read in the data as a set of dictionaries; a row in the original data file contains a list of data pairs: a key and its associated value.
	# We define the name of the telescope under examination as a string, to be concatenated to the file(s) that this code produces, and to identify which data files to read in. 

	# This code will produce a plot of zero point magnitude (or some other quantifier of throughput) against time.

	# each row in the datafile becomes its own row; 'reader' contains many dictionaries. Each dictionary is an 'ordered dictionary'.
	# In short, 'reader' is an array, with each element a dictionary, whose key:value pairs are the physical quantites and their values.

	reader1 = csv.DictReader(open(filename1), delimiter=delimitingcharacter, skipinitialspace=True)
	reader2 = csv.DictReader(open(filename2), delimiter=delimitingcharacter, skipinitialspace=True)

	reader = []

	for row in reader1:
		reader.append(row)
	for row in reader2:
		reader.append(row)

	###################### DATA SORTING ######################
	# Here, we create two empty dictionaries, one for each filter used, that will contain as keys: the integer measurement times; and their associated values: arrays, each element of which is a dictionary containing data about a given measurement with the telescope.

	odict = {}
	cdict = {}

	#'reader' is a massive array, with each element a dictionary. The following code extracts the time of measurement, the quantifier of throughput and the filter used for that measurement.

	for row in reader:

		if "FILE" in firstLine1:
			row["FILE"] = row["FILE"].strip()
		if "FILE" in firstLine2:
			row["FILE"] = row["FILE"].strip()

		row[timeKey] = row[timeKey].strip()
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

		row[timeKey] = float(row[timeKey])
		row[throughput] = float(row[throughput])

		# If the measurement was made with the orange filter:
		if row["FILTER"] == 'o':

			try:
			# This appends the data of a single measurement to the dictionary appropriate to the filter that measurement was taken on. 
				odict[row[timeKey]].append(dict(row))

			except KeyError as e:
				odict[row[timeKey]] = []
				odict[row[timeKey]].append(dict(row))

		# If the measurement was made with the orange filter:
		if row["FILTER"] == 'c':

			try:
			# This appends the data of a single measurement to the dictionary appropriate to the filter that measurement was taken on. 
				cdict[row[timeKey]].append(dict(row))

			except KeyError as e:
				cdict[row[timeKey]] = []
				cdict[row[timeKey]].append(dict(row))

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
			time_o.append(float(row[timeKey]))
			magzpt_o.append(float(row[throughput]))

	for key, value in cdict.items():

		# For set of data for a measurement
		for row in value:

			# Appends values to appropriate arrays
			time_c.append(float(row[timeKey]))
			magzpt_c.append(float(row[throughput]))

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

	plt.figure("Throughput (" + throughput_label + ") vs Time - " + telescope + " - to present day")

	plt.errorbar(data_o["Time (MJD)"], data_o["Zero Point Magnitude"], fmt='o', color='orange', alpha = 0.4, markersize = 0.5)
	plt.errorbar(data_c["Time (MJD)"], data_c["Zero Point Magnitude"], fmt='o', color='c', alpha = 0.4, markersize = 0.5)

	plt.xlabel('MJD')

	if throughput == "MAGZPT":
		plt.ylim((21,22.75))
		plt.ylabel('Zero Point Magnitude')
	if throughput == "MAG5SIG":
		plt.ylim((17,20))
		plt.ylabel('5 Sigma Magnitude')
	if throughput == "SEEING":
		plt.ylim((3,11))
		plt.ylabel('Seeing (arcseconds)')

	plt.minorticks_on()
	plt.grid(which='major', linestyle=':')
	plt.grid(which='minor', linestyle=':')

	fig_name = telescope + '_throughput_('  + throughput_label +  ')_vs_time.png'

	# Before plotting the figure, we save it
	plt.savefig(fig_name)
	plt.show()



def main(argv=None):
	if argv is None:
		argv = sys.argv

# The number of arguments to the code can be set to any given number; we set it to 1, as two files must be entered at a time.
	usage = "Usage: %s <Throughput filename> <Throughput filename>" % argv[0]
	if len(argv) != 3:
		sys.exit(usage)

	filename1 = str(argv[1])
	filename2 = str(argv[2])

	f1 = open(filename1)
	f2 = open(filename2)
	firstLine1 = f1.readlines()[0]
	print(firstLine1)
	firstLine2 = f2.readlines()[0]
	print(firstLine2)

	if "MJD-OBS" in firstLine1 and "MJD-OBS" in firstLine2:
		timeKey = "MJD-OBS"
		delimitingcharacter = '\t'


	telescope = input("Enter name of telescope under check: ")

	print()
	print("Confirm telescope name:")
	print(telescope)
	print("Continue? y/n")
	print()

	confirm = input()

	if confirm == 'y':

		print()
		print("Select Measure of Throughput:")
		print("1. Zero Point Magnitude")
		print("2. 5 Sigma Magnitude")
		print("3. 'Seeing'")
		print("Input 1, 2 or 3 (no spaces)")

		measure = input()

		if measure == '1':
			throughput = "MAGZPT"
			throughput_label = "Zero Point Magnitude"
			general_code(filename1, filename2, telescope, firstLine1, firstLine2, throughput, timeKey, delimitingcharacter, throughput_label)
		if measure == '2':
			throughput = "MAG5SIG"
			throughput_label = "5 Sigma Magnitude"
			general_code(filename1, filename2, telescope, firstLine1, firstLine2, throughput, timeKey, delimitingcharacter, throughput_label)
		if measure == '3':
			throughput = "SEEING"
			throughput_label = "Seeing"
			general_code(filename1, filename2, telescope, firstLine1, firstLine2, throughput, timeKey, delimitingcharacter, throughput_label)
		return

	elif confirm == 'n':

		return

	else:

		return


# The double underscore is a python-ism, and has special meaning.
if __name__ == '__main__':

	main()
