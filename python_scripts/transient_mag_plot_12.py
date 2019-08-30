#!/usr/bin/env python
#
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab




# DATA IMPORT

# Now, we read in the transient data.
# Data file has columns separated by commas.
# To prevent it reading an entire row as a string,
# we use a function np.genfromtxt to generate an array from the data,
# recognising that the columns are separated by commas using delimiter=','
# Enter data file name inside brackets.
# This will store the data from the file as an array called 'data'.

data = np.genfromtxt("k9B7deoy.txt", delimiter=',')	





# DATA MANIPULATION

# Firstly, we store the desired data to be plotted in arrays, one for each axis.
# To do this,
# we select a given column, 
# denoted by a number, 
# and select all rows in the column (:).
# Note: the 1st row/column is denoted '0', the 2nd row/column denoted '1', etc.
# The magnitude values of the transient will be plotted on the y-axis, against time in Mean Julian Date

x = data[:,8]		# Time (MJD)
y = data[:,3]	# Raw Magnitude Values

y_error = data[:,4]	# Error on Magnitude




# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.errorbar(x, y, yerr = y_error, fmt = 'ob', capsize = 5, linestyle = '')




# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.

plt.xlabel('MJD')
plt.ylabel('Transient Magnitude')




# We can also set gridlines and tick marks on the graph.

plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')




# Remembering that the more negative the magnitude the brighter the transient, so we must reverse the direction of the y-axis when measuring in magnitudes.

plt.gca().invert_yaxis()




# Before plotting the figure, we save it

plt.savefig('mag_plot_1.pdf')




# Now we display the figure itself!

plt.show()






