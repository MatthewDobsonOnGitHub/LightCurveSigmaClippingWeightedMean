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
# To prevent it reading an entire row as a string, we use a function np.genfromtxt to generate an array from the data, recognising that the columns are separated by commas using delimiter=','
# Enter data file name inside brackets.
# This will store the data from the file as an array called 'data'.

data = np.genfromtxt("k9B7deoy.txt", delimiter=',')	






# DATA EXTRACTION

# Firstly, we store the desired data to be plotted in arrays, one for each axis.
# To do this, we select a given column, denoted by a number, and select all rows in the column (:).
# Note: the 1st row/column is denoted '0', the 2nd row/column denoted '1', etc.
# The magnitude values of the transient will be plotted on the y-axis, against time in Mean Julian Date

time_raw = data[:,8]		# Time (MJD)
mag_raw = data[:,3]		# Raw Magnitude Values







# CALCULATION OF MEAN TIMES AND MAGNITUDES, BINNED BY DAYS

# The transient magnitude values are all taken over separate days.
# Some are taken on the same day, but not at the exact same time.
# Thus, to find the mean value of the transient magnitude for each day, we must 'bin' the results by the day they were taken.


# To do this, we can consider pairs of data points: time and corresponding magnitude. 
# We also want to calculate the mean time of all the measurements on one day.
# We can round down the time values using the floor function to find the day it was taken, thus allowing us to bin the values according to date, for later averaging.
# For a given date value, we can then sum all the magnitudes that correspond to that date and then take the mean average.


# First of all, we need values to compare the measurement times to, to determine how they are supposed to be binned. 
# For example, say one measurement occurs at 1.9 MJD, and another occurs at 2.1 MJD. Although close 	  together, they would not be averaged together; all the measurements in range 1 =< MJD < 2 would be averaged together.
# Therefore, we need to use the floor function, to go through every measurement

floored_time = np.zeros(len(time_raw))

for i in range(0, len(time_raw)):
	floored_time[i] = math.floor(time_raw[i])

#print(floored_time)
#print(time_raw)


# Now, to remove redundancy in the floored_time array. 
# This will provide a list of dates with which the floor values of the raw dates can be compared.

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
# We don't really nead array no. 2.
# However, we still need to calculate the 4th required array: the mean time measurement values.
# To do this, we must cycle through the raw time values, and check the condition if the floor of said values is equal to the nth date in the floored_time_unique array. If so, the time value is added to an cumulative sum variable, and a divisor counter is increased in value by 1. If not, that summed value is divided by said divisor, and the result appended to an initially empty array. The cycle will then continue, but this time comparing the raw time values to the next ( n+1th ) date in the floored_time_unique array.

# However, we do not want the inner nested loop to restart; we want it to continue along the list fo raw time values; we just want the index of the outer loop (for the date values) to increase by 1.

# To do this, we define a counter that increases by 1 from zero every time a magnitude-time data pair is analysed. When the inner, nested loop is broken and the outer loop ticks over by 1, this counter, entered as the lower limit of the inner loop's range, will cause the inner loop to 'resume' from where it was.

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

# The 'NaN' entries for magnitude measurements that are only upper limits cause problems with the summation. Therefore, we must define two conditions, based on whether or not the magnitude measurement is a known value or merely an upper limit.

		if math.floor(time_raw[j]) == floored_time_unique[i] and math.isnan(mag_raw[j]) != True:


			# Cumulative sum of time values
			cumulative_time_sum = cumulative_time_sum + time_raw[j]
											  

			# Keeps count of number of time values that have been summed thus far
			time_divisor = time_divisor + 1	


			# Cumulative sum of magnitude values
			cumulative_mag_sum += mag_raw[j] 

			# Keeps count of number of magnitude values that have been summed thus far. 				Note, if the magnitude value was only a limit, we do NOT sum it to the total, as 				this would give an average magnitude value much less than the true. 
			mag_divisor = mag_divisor + 1			
	

			# Keeps count of item in array that has been analysed.
			counter = counter + 1



		elif math.floor(time_raw[j]) == floored_time_unique[i] and math.isnan(mag_raw[j]) == True:

			# Cumulative sum of time values
			cumulative_time_sum = cumulative_time_sum + time_raw[j]
											  

			# Keeps count of number of time values that have been summed thus far (but I'm 				keepin it commented here as a reminder)
			time_divisor = time_divisor + 1	


			# We do not add such magnitude values to the total if the above condition is 				true, i.e. if we only have an upper limit on the magnitude. (but I'm keeping it 			here just as a reminder)
			#cumulative_mag_sum += mag_raw[j] 

			# This would keep count of number of magnitude values that have been summed thus 				far. But for the above condition, we don't do this. Note, if the magnitude value 				was only a limit, we do not sum it to the total. (but I'm keepin it commented 				here as a reminder)
			#mag_divisor = mag_divisor + 1			
	

			# Keeps count of item in array that has been analysed.
			counter = counter + 1


		else:	# If we've reached a measurement time which occured the succeeding day:

			# The condition below takes into account the situation where a single upper-limit 				measurement occured on a given day, and prevents division by zero.
			if mag_divisor == 0:
				mag_divisor = 1


			# When we've reached the end of a day, we calculate the mean time... 
			mean_time_calculated = cumulative_time_sum / time_divisor


			# ...and the mean magnitude...
			mean_mag_calculated = cumulative_mag_sum / mag_divisor


			# ...and append them to the appropriate arrays.
			time_mean.append(mean_time_calculated)
			mag_mean.append(mean_mag_calculated)	


			break


# Print out results to see what's going on
#print(time_raw)
#print(time_mean)		
#print(mag_raw)
#print(mag_mean)


# Checking dimensions of the arrays.			
#print(len(time_raw))		
#print(len(floored_time))	
#print(len(floored_time_unique))		
#print(len(mag_raw))
#print(len(time_mean))
#print(len(mag_mean))


# The array lengths must be the same in order for plotting to occur.
if len(time_mean) == len(mag_mean):
	print("Arrays of mean magnitude and time values are equal in size")

#print(time_mean)
#print(mag_mean)





# DATA FINESSING

# The mean-value arrays still contain the upper limit measurements, either as 'NaN' or magnitude = 0.0. The loop below is used to filter out these values.

time_mean_final = []
mag_mean_final = []

# Use code just below if magnitude data contains 'NaN' for an upper limit
for i in range(0, len(mag_mean)):
	if math.isnan(mag_mean[i]) != True and mag_mean[i] != 0.0:
		time_mean_final.append(time_mean[i])
		mag_mean_final.append(mag_mean[i])
	else:
		continue



print(time_mean_final)
print(mag_mean_final)
print(len(time_mean))
print(len(mag_mean))
print(len(time_mean_final))
print(len(mag_mean_final))




# DATA PLOTTING

# Now, we plot the data on the graph. 
# Note, we have errors associated with the y-values of the data, and so must be plotted also. To do this, we use the errorbar() function.
# 'fmt' determines the style (1st letter) and colour (2nd letter) of the datapoints; 'o' makes circular points, 'b' makes blue points.
#capsize determines the size of the error bar caps.
# linestyle determies the style of the line that joins the data points; here, we leave it blank, so no line is formed.

plt.plot(time_mean_final, mag_mean_final,'ob')



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

#plt.xlim([58620, 58680])
#plt.ylim([22, 17])



# Before plotting the figure, we save it

plt.savefig('mag_vs_time_plot_7.pdf')



# Now we display the figure itself!

plt.show()






