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

time_raw = data[:,8]		# Time (MJD)
mag_raw = data[:,3]		# Raw Magnitude Values







# CALCULATION OF MEAN

# The transient magnitude values are all taken over separate days.
# Some are taken on the same day, but not at the exact same time.
# Thus, to find the mean value of the transient magnitude for each day, we must 'bin' the results by the day they were taken.


# To do this, we can consider a pair of data points: time and corresponding magnitude. 
# We also want to calculate the mean time of all the measurements on one day.
# We can round down the time values using the floor function to find the day it was taken and thus this allows us to bin the values according to date, for latter averaging.
# For a given date value, we can then sum all the magnitudes that correspond to that date and then take the average.


# First of all, we need values to compare the measurement times to, to determine how they are supposed to be binned. 
# For example, say one measurement occurs at 1.9 MJD, and another occurs at 2.1 MJD. Although close 	  together, they would not be averaged together; all the measurements in range 1 =< MJD < 2 would be averaged together.
# Therefore, we need to use the floor function, to go through every measurement

floored_time = np.zeros(len(time_raw))

for i in range(0, len(time_raw)):
	floored_time[i] = math.floor(time_raw[i])

#print(floored_time)
#print(time_raw)





# Now, to remove redundancy in the floored_time array. This will provide a list of dates with which the floor values of the raw dates can be compared.

floored_time_unique = []

for i in range(0, len(floored_time)):

	if floored_time[i] not in floored_time_unique:

		floored_time_unique.append(floored_time[i])

	else:

		continue

#print(floored_time_unique)





# As of now, we have three arrays of time:
# 1. the raw time values of the measurements
# 2. the floored values of the time values
# 3. the floored values without redundancy.
# However, we still need to calculate the 4th required array: the mean time measurement values.
# To do this, we must cycle through the raw time values, and check the condition if the floor of said values is equal to the nth value in the floored_time_unique array. If so, the time value is summed to an cumulative sum value, and a counter is increased in value by 1. If not, that summed value is divided by said counter, and the result appended to an empty array. The cycle will continue, but this time comparing the raw time values to the next ( n+1th ) floored time value in the floored_time_unique array.


# We also want to calculate the mean of the magnitude measurements that were taken at given times.


time_divisor = 0		# How many time values are being averaged in a given binned day

mag_divisor = 0			# How many magnitude values are being averaged in a given binned day

cumulative_time_sum = 0		# The sum of all the time values in a given binned day.

cumulative_mag_sum = 0		# The sum of all the magnitude values in a given binned day.

time_mean = []			# Empty array, to store all the mean time values.

mag_mean = []			# Empty array, to store all the mean magnitude values.

counter = 0


# Runs through all the floored time values (i.e. the MJD integer date values)
for i in range(0, len(floored_time_unique)):	


	# For every new date, the variables used in the calculations are reset.
	cumulative_time_sum = 0			 						  

	cumulative_mag_sum = 0

	time_divisor = 0

	mag_divisor = 0

	mean_time_calculated = 0				


	# Runs through all the observed magnitude values and their times of measurement.
	for j in range(counter, len(time_raw)):


		if math.floor(time_raw[j]) == floored_time_unique[i] and math.isnan(mag_raw[j]) != True:


			# Cumulative sum of time values
			cumulative_time_sum = cumulative_time_sum + time_raw[j]
											  

			# Keeps count of number of time values that have been summed thus far
			time_divisor = time_divisor + 1	


			# Cumulative sum of magnitude values
			cumulative_mag_sum += mag_raw[j] 

			# Keeps count of number of magnitude values that have been summed thus far. 				Note, if the magnitude value was only a limit, we do not sum it to the total. 
			mag_divisor = mag_divisor + 1			
	

			# Keeps count of item in array that has been analysed.
			counter = counter + 1



		elif math.floor(time_raw[j]) == floored_time_unique[i] and math.isnan(mag_raw[j]) == True:

			# Cumulative sum of time values
			cumulative_time_sum = cumulative_time_sum + time_raw[j]
											  

			# Keeps count of number of time values that have been summed thus far
			time_divisor = time_divisor + 1	


			# Cumulative sum of magnitude values
			#cumulative_mag_sum += mag_raw[j] 

			# Keeps count of number of magnitude values that have been summed thus far. 				Note, if the magnitude value was only a limit, we do not sum it to the total.
			#mag_divisor = mag_divisor + 1			
	

			# Keeps count of item in array that has been analysed.
			counter = counter + 1


		else:
			if mag_divisor == 0:
				mag_divisor = 1

			if math.isnan(cumulative_mag_sum) != True or mag_divisor != 0:
				# When we've reached the end of a day, we calculate the mean time... 
				mean_time_calculated = cumulative_time_sum / time_divisor


				# ...and the mean magnitude...
				mean_mag_calculated = cumulative_mag_sum / mag_divisor


				# ...and append them to the appropriate arrays.
				time_mean.append(mean_time_calculated)
				mag_mean.append(mean_mag_calculated)	


			break


# However, we do not want the inner nested loop to restart; we want it to continue along the list fo raw time values; we just want the index of the outer loop (for the date values) to increase by 1.


# Print out results to see what's going on
print(time_raw)
print(time_mean)		
print(mag_raw)
print(mag_mean)


# Checking dimensions of the arrays.			
print(len(time_raw))		
#print(len(floored_time))	
#print(len(floored_time_unique))		
print(len(mag_raw))
print(len(time_mean))
print(len(mag_mean))


#
if len(time_mean) == len(mag_mean):
	print("Arrays of mean magnitude and time values are equal in size")

print(time_mean)
print(mag_mean)


# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.plot(time_mean, mag_mean,'ob')




# Setting the titles for the x- and y-axes.
# x-axis is time in units if Modified Julian Date.
# y-axis is magnitude of transient's light.

plt.xlabel('MJD')
plt.ylabel('Transient Magnitude')




# We can also set gridlines and tick marks on the graph.

plt.minorticks_on()
plt.grid(which='major', linestyle=':')
plt.grid(which='minor', linestyle=':')




# Remembering that the more negative the magnitude the brighter the transient, so we must reverse the direction of the y-axis. (This must be done before setting the x- and y-axis limits, for some reason.)

plt.gca().invert_yaxis()




# We can also adjust the x- and y-axis limits:

plt.xlim([58620, 58680])
plt.ylim([22, 17])




# Before plotting the figure, we save it

plt.savefig('mag_vs_time_plot_4.pdf')




# Now we display the figure itself!

plt.show()






