	
def median_and_stdev(value)	

	# To calculate the standard deviation of the daily flux measurements, we append them to an 		empty array, and so the same for their uncertainties and measurement times (to separate arrays, of 		course). The standard deviation function we defined at the start requires two inputs: values and raw 		errors, in order to compute the error for a lone measurement in a day.
	measurement_clipping_array_o = []  
	uncertainty_clipping_array_o = []
	time_clipping_array_o = []
	# Resetting the values of sigma and median to zero, for every iteration.
	sigma = 0
	med = 0

	for row in value:

		measurement_clipping_array_o.append(row["calc_flux"]) 
		uncertainty_clipping_array_o.append(row["calc_dflux"]) 
		time_clipping_array_o.append(row["mjd"]) 
			
	# Calculates the standard deviation of all flux values in a day
	sigma = standard_deviation(measurement_clipping_array_o, uncertainty_clipping_array_o)

	# Calculates the median of all flux values in a day
	med = stat.median(measurement_clipping_array_o)

	return sigma, med
