#!/usr/bin/env python
#
#
# Load in the necessary libraries; importing them as smaller strings for brevity.

import numpy as np
import matplotlib.pyplot as plt
import math
import pylab


# Now, we load in the transient data.
# Enter data file name inside brackets.
# This will store the data from the file as an array called 'data'.

data = np.loadtxt('textfile.txt')	


# If needs be, we can set the size fo the output graph, but this is optional.
# dpi = 'Dots Per Inches'.

fig = plt.figure(figsize=(12,6), dpi = 100)


# DATA PLOTTING

# Firstly, we store the desired data to be plotted in arrays, one for each axis.
# To do this, we select a given column, denoted by a number, and select all rows in the column (:).
# Note: the 1st row/column is denoted '0', the 2nd row/column denoted '1', etc.

x = data[:,0]
y = data[:,1]
y_error = data[:,2]


# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size fo the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.errorbar(x, y, yerr = y_error, fmt = 'ob', capsize = 5, linestyle = '')


# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Days.
# y-axis is flux of light.

plt.xlabel('MJD')
plt.ylabel('Transient Flux')

# Setting the numerical limits of the x- and y-axes

plt.xlim([0,11])
plt.ylim([-20,120])


# We can also set gridlines and tick marks on the graph.

plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')


# Before plotting the figure, we save it

plt.savefig('test_plot.pdf')


# Now we display the figure itself!

plt.show()






