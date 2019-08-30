	
def remove_row(value, sigma, median):

	empty_list = []

	for row in value:	

		# If a measurement lies outside the 1 sigma range from the median (i.e. it is an outlier)...
		if row["calc_flux"] < (sigma + median) or row["calc_flux"] > (sigma - median):

			# ... then we delete the entire measurement from the dictionary
			empty_list.append(row)


	return empty_list
