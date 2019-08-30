counter_o = 0
counter_c = 0


# FOR ORANGE LENS:

# Thw following arrays are for use in the loop

summed_time_o = np.zeros(len(dates_o))

time_divisor_o = np.zeros(len(dates_o))

summed__weighted_flux_o = np.zeros(len(dates_o))

summed_weights_o = np.seros(len(dates_o))


# The following arrays are for the final calculation of the weighted means

time_mean_o = np.zeros(len(dates_o))

flux_weighted_mean_o = np.zeros(len(dates_o))


# Used in calculations

time_counter_o = 0

flux_counter_o = 0

for i in range(0, len(dates_o)):

	time_counter_o = 0

	flux_counter_o = 0

	for j in range(counter_o, len(time_o)):

		time_counter_o = 0

		flux_counter_o = 0

		if math.floor(time_o[j]) == dates_o[i]:


			# Time
			
			time_counter_o += 1

			flux_counter_o += 1

			summed_time_o[i] += time_o[j]

			time_divisor_o[i] += time_counter_o 

			summed_weighted_flux_o[i] += flux_o[j]*weights_o[j]

			summed_weights_o[i] += weights_o[j]


			# Counter for inner loop

			counter_o += 1





for i in range(0, len(time_mean_o)):

	time_mean_o[i] = summed_time_o[i]/time_divisor_o[i]
	flux_weighted_mean_o[i] = summed_weighted_flux_o[i]/summed_weights_o[i]


print("Summed time----------->", summed_time_o)
print("Summed flux----------->", summed_flux_o)
print("No. times  summed----->", time_divisor_o)
print("No. fluxes summed----->", flux_divisor_o)
print("Mean Time------------->", time_mean_o)
print("Mean Flux------------->", flux_mean_o)
