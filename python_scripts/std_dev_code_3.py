############################ STANDARD DEVIATION OF WEIGHTED MEAN FLUXES #################################


# The standard deviation is equal to the square root of the ratio of the sum of the square of the differences of each data point in a day compared to the mean, to the number of data points in a day minus one.

# FOR ORANGE FILTER


denom_o = np.zeros(len(dates_o))

counter_o = 0

for i in range(0, len(dates_o)):

	flux_counter_sd_o = 0

	for j in range(counter_o, len(time_o)):

		flux_counter_sd_o = 0

		if math.floor(time_o[j]) == dates_o[i]:

			flux_counter_sd_o += 1
			
			denom_o[i] += flux_counter_sd_o

			counter_o += 1


counter_o = 0

print("orange denominators")
print(denom_o)
print()

# Calculating the n-1 of the standard deviation denominator

denominators_o = np.zeros(len(dates_o))

for i in range(0, len(denom_o)):

	denominators_o[i] = denom_o[i] - 1

print("orange denominators minus one")
print(denominators_o)
print()

# Now, to start calculating the numerator

sq_diff_sum_o = np.zeros(len(dates_o))

for i in range(0, len(dates_o)):

	flux_counter_sd_o = 0

	for j in range(counter_o, len(time_o)):

		flux_counter_sd_o = 0

		if math.floor(time_o[j]) == dates_o[i] and denominators_o[i] != 0:

			diff_from_mean = 0
			
			diff_from_mean = flux_o[j] - flux_weighted_mean_o[i]

			squared_diff_from_mean = diff_from_mean**2

			sq_diff_sum_o[i] += squared_diff_from_mean

		if math.floor(time_o[j]) == dates_o[i] and denominators_o[i] == 0:

			sq_diff_sum_o[i] = dflux_o[j]



print()
print("orange square difference sum")
print(sq_diff_sum_o)
print()



var_o = np.zeros(len(dates_o))
stdev_o = np.zeros(len(dates_o))

for i in range(0, len(dates_o)):

	if denominators_o[i] != 0:	# If more than one data point in a day have been averaged

		var_o[i] = sq_diff_sum_o[i] / denominators_o[i]
	
		stdev_o[i] = var_o[i]**(1/2)

	elif denominators_o[i] == 0:	# if only one data point in a day has been averaged

		denominators_o[i] = 1

		var_o[i] = sq_diff_sum_o[i] / denominators_o[i]

		stdev_o[i] = var_o[i]**(1/2)

print("orange flux standard deviations")
print(stdev_o)
print()




# FOR CYAN FILTER


denom_c = np.zeros(len(dates_c))

counter_c = 0

for i in range(0, len(dates_c)):

	flux_counter_sd_c = 0

	for j in range(counter_c, len(time_c)):

		flux_counter_sd_c = 0

		if math.floor(time_c[j]) == dates_c[i]:

			flux_counter_sd_c += 1
			
			denom_c[i] += flux_counter_sd_c

			counter_c += 1


counter_c = 0

print("orange denominators")
print(denom_c)
print()

# Calculating the n-1 of the standard deviation denominator

denominators_c = np.zeros(len(dates_c))

for i in range(0, len(denom_c)):

	denominators_c[i] = denom_c[i] - 1

print("orange denominators minus one")
print(denominators_c)
print()

# Now, to start calculating the numerator

sq_diff_sum_c = np.zeros(len(dates_c))

for i in range(0, len(dates_c)):

	flux_counter_sd_c = 0

	for j in range(counter_c, len(time_c)):

		flux_counter_sd_c = 0

		if math.floor(time_c[j]) == dates_c[i] and denominators_c[i] != 0:

			diff_from_mean = 0
			
			diff_from_mean = flux_c[j] - flux_weighted_mean_c[i]

			squared_diff_from_mean = diff_from_mean**2

			sq_diff_sum_c[i] += squared_diff_from_mean

		if math.floor(time_c[j]) == dates_c[i] and denominators_c[i] == 0:

			sq_diff_sum_c[i] = dflux_c[j]



print()
print("orange square difference sum")
print(sq_diff_sum_c)
print()



var_c = np.zeros(len(dates_c))
stdev_c = np.zeros(len(dates_c))

for i in range(0, len(dates_c)):

	if denominators_c[i] != 0:	# If more than one data point in a day have been averaged

		var_c[i] = sq_diff_sum_c[i] / denominators_c[i]
	
		stdev_c[i] = var_c[i]**(1/2)

	elif denominators_c[i] == 0:	# if only one data point in a day has been averaged

		denominators_c[i] = 1

		var_c[i] = sq_diff_sum_c[i] / denominators_c[i]

		stdev_c[i] = var_c[i]**(1/2)

print("orange flux standard deviations")
print(stdev_c)
print()










#used to stop program at this point in the code.
#sys.exit(0) 
