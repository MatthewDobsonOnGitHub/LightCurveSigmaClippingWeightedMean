summed_time_c = np.zeros(len(dates_c))

dict_c = {}




for i in range(0, len(dates_c)):


	#print("raw data------>", dates_c[i])


	time_divisor_c = 0

	flux_divisor_c = 0

	time_sum_c = 0

	flux_sum_c = 0

	mean_time_c = 0

	mean_flux_c = 0

	for j in range(counter_c, len(time_c)):

		c_array = [] 		

		#if math.floor(time_c[j]) == dates_c[i]:

			print("actual time------>", time_c[j])

			# Sum of all the time values (unweighted)
			time_sum_c = time_sum_c + time_c[j]

			# Sum of all flux values (unweighted)
			flux_sum_c = flux_sum_c + flux_c[j]

			# Keeps count of number of time values that have been summed thus far
			time_divisor_c = time_divisor_c + 1

			# Keeps count of number of flux values that have been summed thus far
			flux_divisor_c = flux_divisor_c + 1

			# Keeps count of items in flux and time arrays that have been analysed
			counter_c = counter_c + 1

			print("Counter for Cyan Filter:")
			print(counter_c)


		#elif math.floor(time_c[j]) != dates_c[i]:	# This condition is when we have reached 									a measured time which occured the 									succeeding day.


			# However, we need to take into account the possibility that a single 				measurement occured on a day, to prevent division by zero.

			if flux_divisor_c == 0 or time_divisor_c == 0:

				flux_divisor_c = 1
				time_divisor_c = 1

			# When we've reached the end of a day, we calculate the mean time... 
			mean_time_calculated = time_sum_c / time_divisor_c


			# ...and the mean flux...
			mean_flux_calculated = flux_sum_c / flux_divisor_c


			# ...and append them to the appropriate arrays.
			time_mean_c.append(mean_time_calculated)
			flux_mean_c.append(mean_flux_calculated)

			counter2 = counter2 + 1
			print("How many days")
			print(counter2)

			print("Times: (MJD)")
			print(time_c[j])
			print("Dates: (MJD)")
			print(dates_c[i])


			break

