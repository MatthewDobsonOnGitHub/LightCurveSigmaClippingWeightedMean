#!/usr/bin/env python
#
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab
import csv
import sys






# DATA IMPORT

# Now, we read in the transient data.
# Data file has columns separated by commas (csv)
# We can read in the data as a set of dictionaries; a dictionary contains a list of data pairs: a key and its associated value. This will allow us to sort through the data much more rigorously.

# csv.reader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).


# in case the filename needs to be changed, it's more accessible here.	
filename = "SN2019ehk_raw_data.csv" 

# each row in the datafile becomes its own dictionary; 'reader' contains many dictionaries.
data = csv.DictReader(open(filename))


# Since the data is taken using two separate colour filters, we must keep data taken in different filters separate.
# To do this, we must sort through the object 'reader', which contains many dictionaries (each corresponding to a row in the original table of data in the file the data was read from), and separate out the rows according to which filter with which the data was taken.
# We can make use of a special function called defaultdict(), which can automatically initialise a dictionary with a blank values and with the attributes of a list (permiting the 'append' function to be used) -- a subtle difference between creating an empty dictionary with {}.
# To do this, we must import another library of code.

from collections import defaultdict

dict_o = defaultdict(list)
dict_c = defaultdict(list)

# Now to sort through the data

for row in data:

# If the dictionary of data was taken with the orange filter

	if row["filter"] == 'c':	

# Below condition ensures data is only appended to the filter-specific dictionaries if there are no blank entries of data.

		if row["mjd"] != 'None' and row["peakfit"] != 'None' and row["major"] != 'None' and row["minor"] != 'None' and row["zp"] != 'None' and row["apfit"] != 'None':

# Automatically initialises the list and append this row

			dict_c[math.floor(float(row["mjd"]))].append(row)


# If the dictionary of data was taken with the cyan filter

	elif row["filter"] == 'o':

# Below condition ensures data is only appended to blank dictionaries if there is no blank entries of data.

		if row["mjd"] != 'None' and row["peakfit"] != 'None' and row["major"] != 'None' and row["minor"] != 'None' and row["zp"] != 'None' and row["apfit"] != 'None':

# Automatically initialise the list and append this row

            		dict_o[math.floor(float(row["mjd"]))].append(row)

print()
print()
print("FULL DATA")
print(data)
print()
print()
print("ORANGE DATA")
print(dict_o)
print()
print()
print("CYAN DATA")
print(dict_c)


# Note: MJD means the time of observation of a given data point, in Mean Julian Date.

# Note that for the loops below, we use the .items() function to return the list with all dictionary keys and their associated values (a dictionary in Python is an unordered collection of data values). .items() returns a view object that displays a list of a given dictionary's key-value pairs.

print()
print("********** CYAN ***********")
print()
for key, value in dict_c.items():
    print (key)
    mjdSum = 0.0
    #peakfitSum = 0.0
    for row in value:
        print(row["mjd"], row["peakfit"])
        mjdSum = mjdSum + float(row["mjd"])
        #peakfitSum = peakfitSum + float(row["peakfit"])
    print("Mean mjd = ", mjdSum / len (value))
    #print("Mean peakfit = ", peakfitSum / len (value))
    print()


print ("********** ORANGE ***********")
print ()
for key, value in dict_o.items():
    print (key)
    mjdSum = 0.0
    #peakfitSum = 0.0
    for row in value:
        print(row["mjd"], row["peakfit"])
        mjdSum = mjdSum + float(row["mjd"])
        #peakfitSum = peakfitSum + float(row["peakfit"])
    print("Mean mjd = ", mjdSum / len (value))
    #print("Mean peakfit = ", peakfitSum / len (value))
    print()



