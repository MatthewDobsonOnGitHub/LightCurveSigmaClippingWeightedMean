#!/usr/bin/env python
#
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab


# Now, we read in the transient data.
# Data file has columns separated by commas.
# To prevent it reading an entire row as a string,
# we use a function np.genfromtxt to generate an array from the data,
# recognising that the columns are separated by commas using delimiter=','
# Enter data file name inside brackets.
# This will store the data from the file as an array called 'data'.

data = np.genfromtxt("k9B7deoy.txt", delimiter=',')	


# If needs be, we can set the size fo the output graph, but this is optional.
# dpi = 'Dots Per Inches'.

fig = plt.figure(figsize=(12,6), dpi = 100)


# DATA MANIPULATION

# Firstly, we store the desired data to be plotted in arrays, one for each axis.
# To do this,
# we select a given column, 
# denoted by a number, 
# and select all rows in the column (:).
# Note: the 1st row/column is denoted '0', the 2nd row/column denoted '1', etc.
# The magnitude values of the transient will be plotted on the y-axis, against time in Mean Julian Date

x = data[:,8]		# Time (MJD)
y_raw = data[:,3]	# Raw Magnitude Values

y_error = data[:,4]	# Error on Magnitude


# The raw data for the magnitudes contain upper limits, which are ot needed at the moment. 
# We need a way to sort through the column to eliminate such values.
# We create an array of zeros using the function np.zeros()
# that is the same length as the y_error_raw array.
# If the magnitude values are known, 
# they are slotted into the equivalent element in the empty array 'y_error'
# If the magnitude values contain the character '>'
# We make the element containing that value empty in both the x- and y-axis arrays.

#y = np.zeros(len(y_raw))

#for element in y_raw:
#	string = y_raw[element]
#	if string.isdigit() == 'False':
#		y[element] = np.empty(y[element])
#		x[element] = np.empty(x[element])
#	else:
#		y[element] = y_raw[element]


# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.errorbar(x, y_raw, yerr = y_error, fmt = 'ob', capsize = 5, linestyle = '')


# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.

plt.xlabel('MJD')
plt.ylabel('Transient Magnitude')


# Setting the numerical limits of the x- and y-axes

#plt.xlim([0,11])
plt.ylim([17,22])


# We can also set gridlines and tick marks on the graph.

plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')


# Before plotting the figure, we save it

plt.savefig('mag_plot_1.pdf')


# Now we display the figure itself!
# Remembering that the more negative the magnitude the brighter the transient
# we reverse the direction of the y-axis.

plt.gca().invert_yaxis()

plt.show()






