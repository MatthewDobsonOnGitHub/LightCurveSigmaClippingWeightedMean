import numpy as np
import matplotlib.pyplot as plt
import math
import pylab
import csv
import sys


# DATA IMPORT

# Now, we read in the transient data.
# Data file has columns separated by commas.
# We can read in the data as a set of dictionaries; a row contains a list of data pairs: a key and its associated value
# csv.DictReader is much better better than the np.genfromtxt. Save the file as a CSV (.csv).

# in case the filename needs to be changed, it's more accessible here.    
filename = "SN2019ehk_raw_data.csv" 

# each row in the datafile becomes its own row; the array 'reader' contains many dictionaries.
reader = csv.DictReader(open(filename))



# Here's an idea for making the code more readable!  This is a bit of a cheat!
# It uses a special object called a defaultdict which automatically initialises
# a row with a blank value.

from collections import defaultdict

odict = defaultdict(list)
cdict = defaultdict(list)


for row in reader:	# cycles through all the elements in the array 'reader' - every element is 				itself a dictionary!

    if row["filter"] == 'o':

        if row["mjd"] != 'None' and row["peakfit"] != 'None' and row["major"] != 'None' and row["minor"] != 'None' and row["zp"] != 'None' and row["apfit"] != 'None':

            # Automatically initialise the list and append this row
            odict[int(float(row["mjd"]))].append(row)


    elif row["filter"] == 'c':

        if row["mjd"] != 'None' and row["peakfit"] != 'None' and row["major"] != 'None' and row["minor"] != 'None' and row["zp"] != 'None' and row["apfit"] != 'None':

            # Automatically initialise the list and append this row
            cdict[int(float(row["mjd"]))].append(row)

print()
print(cdict)
print()


print()
print("********** CYAN ***********")
print()
# To loop through a dictionary, we must use the .items() function, which produces a list of all the key:value pairs in a dictionary as a long list to cycle through. Two counters are used in such a loop - one for the keys, the other for their associated values.
# These loops calculate the mean values of measurement time and 'peakfit' value (the latter is used to calculate the flux value) for a given day fo measurement, binning them by day.

for key, value in cdict.items():
    print (key)		# Prints the integer day of measurement.
    mjdSum = 0.0	# Define a cumulative sum for time, and set it to zero for every new day of 				measurement.
    peakfitSum = 0.0	# Define a cumulative sum for peakfit, and set it to zero for every new day of 				measurement.
    for row in value:
        print(row["mjd"], row["peakfit"])	# For every column in the value
        mjdSum = mjdSum + float(row["mjd"])
        peakfitSum = peakfitSum + float(row["peakfit"])
    print("Mean mjd = ", mjdSum / len (value))
    print("Mean peakfit = ", peakfitSum / len (value))
    print()


print ("********** ORANGE ***********")
print ()
for key, value in odict.items():
    print (key)
    mjdSum = 0.0
    peakfitSum = 0.0
    for row in value:
        print(row["mjd"], row["peakfit"])
        mjdSum = mjdSum + float(row["mjd"])
        peakfitSum = peakfitSum + float(row["peakfit"])
    print("Mean mjd = ", mjdSum / len (value))
    print("Mean peakfit = ", peakfitSum / len (value))
    print()
