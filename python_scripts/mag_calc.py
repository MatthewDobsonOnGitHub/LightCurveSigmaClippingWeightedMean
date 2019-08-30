############################ CROSS-CHECKING FLUX CALCULATIONS ############################

# This is a method to cross-check the flux calculations. We convert the calculated flux values into janskys, then into magnitudes, and then plot them against the raw magnitude values in the original datafile.

# The magnitude values read into the arrays contain minimum mag values, with the '>' symbol. This prevents the values from being read in as floats, and therefore, these values require removal.

# Since we don't know exactly how many magnitude values will be sorted and calculated without looking at the raw data file beforehand, we must define arrays that will contain the indermediate calculated quantities as empty, and append values to them.

magnitude_calc_o = []	# non-upperlimit measured magnitudes (orange - all)
magnitude_calc_c = []	# non-upperlimit measured magnitudes (cyan - all)
magnitude_recalc_o = []	# recalculated magnitude values (orange - all)
magnitude_recalc_c = []	# recalculated magnitude values (cyan - all)
flux_corresponding_o = [] 
flux_corresponding_c = []
time_corresponding_o = []
time_corresponding_c = []


for key, value in raw_data_o.items():

	for i in raw_data_o[value]:

		if '>' not in raw_data_o["Magnitude"][i] and raw_data_o["Flux"][i] >= 0:
			mag_float_o = float(raw_data_o["Magnitude"][i])
			magnitude_calc_o.append(mag_float_o)
			flux_corresponding_o.append(raw_data_o["Flux"][i])
			time_corresponding_o.append(raw_data_o["Time"][i])

for key, value in raw_data_c.items():

	for i in raw_data_c[value]:

		if '>' not in raw_data_c["Magnitude"][i] and raw_data_c["Flux"][i] >= 0:
			mag_float_c = float(raw_data_c["Magnitude"][i])
			magnitude_calc_c.append(mag_float_c)
			flux_corresponding_c.append(raw_data_c["Flux"][i])
			time_corresponding_c.append(raw_data_c["Time"][i])

# Converting microjansky flux values to janskys
flux_jan_o = np.zeros(len(flux_corresponding_o))

for i in range(0, len(flux_jan_o)):
	flux_jan_o[i] = flux_corresponding_o[i]*10**(-6)

flux_jan_c = np.zeros(len(flux_corresponding_c))

for i in range(0, len(flux_jan_c)):
	flux_jan_c[i] = flux_corresponding_c[i]*10**(-6)

# Now we must calculate the magnitudes:
for i in range(0, len(flux_jan_o)):
	if flux_jan_o[i] >= 0:
		mag_o = (-2.5) * math.log(flux_jan_o[i], 10) + 8.9
		magnitude_recalc_o.append(mag_o)

for i in range(0, len(flux_jan_c)):
	if flux_jan_c[i] >= 0:
		mag_c = (-2.5) * math.log(flux_jan_c[i], 10) + 8.9
		magnitude_recalc_c.append(mag_c)

print()
print("Measured magnitudes - orange")
print(magnitude_calc_o)
print("Re-calculated magnitudes - orange")
print(magnitude_recalc_o)
print("Measured magnitudes - cyan")
print(magnitude_calc_c)
print("Re-calculated magnitudes - cyan")
print(magnitude_recalc_c)
print()
print("Re-calculated magnitudes length - orange")
print(len(magnitude_recalc_o))
print("Re-calculated magnitudes length - cyan")
print(len(magnitude_recalc_c))
print()		

# Now to calculate the difference between the measured and the recalculated magnitudes

mag_diff_o = []
mag_diff_c = []

for i in range(0, len(magnitude_recalc_o)):
	mag_diff_for_o = magnitude_recalc_o[i] - magnitude_calc_o[i]
	mag_diff_o.append(mag_diff_for_o)

for i in range(0, len(magnitude_recalc_c)):
	mag_diff_for_c = magnitude_recalc_c[i] - magnitude_calc_c[i]
	mag_diff_c.append(mag_diff_for_c)

mag_rel_diff_o = np.zeros(len(mag_diff_o))
mag_rel_diff_c = np.zeros(len(mag_diff_c))

for i in range(0, len(mag_diff_o)):
	mag_rel_diff_o[i] = (mag_diff_o[i] / magnitude_calc_o[i])*100
for i in range(0, len(mag_diff_c)):
	mag_rel_diff_c[i] = (mag_diff_c[i] / magnitude_calc_c[i])*100

print("Magnitude Difference for Orange Filter")
print(mag_diff_o)
print()
print("Magnitude Difference for Cyan Filter")
print(mag_diff_c)
print()
print("Raw Cyan Data Dictionary")
print(raw_data_c)
print()
