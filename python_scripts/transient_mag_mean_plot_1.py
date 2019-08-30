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

x_raw = data[:,8]		# Time (MJD)
y_raw = data[:,3]	# Raw Magnitude Values





# CALCULATION OF MEAN

# The transient magnitude values are all taken over separate days.
# Some are taken on the same day, but not at the exact same time.
# Thus, to find the mean value of the transient magnitude for each day, we must 'bin' the results 
# by the day they were taken.

# To do this, we can consider a pair of data points: time and corresponding magnitude. 
# We can round down the time values using the floor function to find the day it was taken
# For a given date value, we can then sum all the magnitudes that correspond to that date 
# and then take the average.


# Define an array of zeros to be the dates that every magnitude measurement occur on.

time = np.zeros(len(x_raw))


# Cycle through the meaurement time values and apply the floor function to get the integer MJD value.

for element in range(0, len(time)):

	time[element] = math.floor(x_raw[element])

print(x_raw)	# Print both arrays to make sure.
print(time)




# Now to create a list of the integer MJD values but without the duplication.


date_values = []


for i in range(0, len(time)):
	if time[i] not in date_values:
		date_values.append(time[i])
	else:
		continue


print(date_values)


mean_magnitudes = []	# This will later be plotted.
counter1 = 1		# This will keep count ofhow many measurement occured on a given day
sum_value = 0		# This keeps count of the summed magnitude on one day, later to be divided by 				  counter1


for date_counter in range(0, len(date_values)):

	for time_counter in range(0, len(time)):

		if time[time_counter] == date_values[date_counter]:

			sum_value = sum_value + y_raw[time_counter]
			counter1 = counter1 + 1

		else:
				
			mean_value = sum_value / counter1
			mean_magnitudes.append(mean_value)	

# Appends the mean value of the magnitudes of a given date to the mean_magnitude array
				
			sum_value = 0
			counter1 = 1

	






# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.plot(date_values, mean_magnitudes, fmt = 'ob', capsize = 5, linestyle = '')




# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.

plt.xlabel('MJD')
plt.ylabel('Transient Magnitude')




# We can also set gridlines and tick marks on the graph.

plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')




# Remembering that the more negative the magnitude the brighter the transient
# we reverse the direction of the y-axis.

plt.gca().invert_yaxis()




# Before plotting the figure, we save it

plt.savefig('mag_plot_1.pdf')




# Now we display the figure itself!

plt.show()


