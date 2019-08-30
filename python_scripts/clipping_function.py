	
def clipping_function(input_dictionary, output_dictionary):

	output_dictionary = {}

	# We loop through all the days of measurements, and loop through all the measurements taken on each day (nested loops).

	for key, value in input_dictionary.items():

		# Define the number of points per day in the initial, unclipped data.
		list_length = len(value)

		# Define the number of points per day in the clipped data - this will be subject to change of value with each iteration
		list_length_new = len(value)

		# Create an array of list lengths, starting with original list length
		length_array = [list_length]

		# Finding the standard deviation and median values for each day; the function returns two variables, and assigns the values in a specific order, so be careful!
		sigma, med = median_and_stdev(value)

		# Performs the clipping an initial first time, calling the function 'remove_row' to remove an outlying data point (if one exists).
		new_list = remove_row(value, sigma, med)

		# Appends the length of the new, clipped list to the array.
		length_array.append(len(new_list))

		print(length_array)

		while(True): # Infinite loop, until the last two elements in the array are of equal length

			# calculate new s.d. and median for every clipping iteration

			sigma, med = median_and_stdev(new_list)

			# If no more points have been clipped (i.e. the number of unclipped points in a day after passing the data through the clipping function is the same), we want the algorithm to stop for a given day.
			if length_array[-1] == length_array[-2]:

				# The newest list is appended to the empty dictionary for clipped data, with the same key as the original, unclipped data.

				output_dictionary[key] = new_list
				print("Break Out")			
				print(length_array)
				return new_list
				break

			# If clipping has been performed (i.e. if the new clipped list is shorter than before), we want this to continue.

			else:
				# perform clipping again
				new_list = remove_row(value, sigma, med)
				# newest list added to the clipped data dictionary (it seemingly overwrites the original array)
				# number of remaining data points calculated, and appended to the appropriate array
				length_array.append(len(new_list))
				print(length_array)
				sigma, med = median_and_stdev(new_list)
				output_dictionary[key] new_list

	return output_dictionary

















