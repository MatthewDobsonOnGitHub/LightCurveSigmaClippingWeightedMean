# CALCULATION OF MEAN

# The transient magnitude values are all taken over separate days.
# Some are taken on the same day, but not at the exact same time.
# Thus, to find the mean value of the transient magnitude for each day, we must 'bin' the results 
# by the day they were taken.

# To do this, we can consider a pair of data points: time and corresponding magnitude. 
# We also want to calculate the mean time of all the measurements on one day.
# We can round down the time values using the floor function to find the day it was taken
# and thus this allows us to bin the values according to date, for latter averaging.
# For a given date value, we can then sum all the magnitudes that correspond to that date 
# and then take the average.


# Define an array of zeros to be the average time that every magnitude measurements occur on for each day.

times_mean = np.zeros(len(x_raw))


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
