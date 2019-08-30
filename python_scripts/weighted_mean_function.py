def weighted_mean_function(dictionary)	

	r_time_o = []
	r_flux_o = []
	r_dev_o = []
	m_time_o = []
	w_flux_o = []
	s_dev_o = []
	num_o = []
	new_error_o = []


	for key, value in dictionary.items():
	    
		time_sum_o = 0.0
		flux_weight_product_sum_o = 0.0
		weight_sum_o = 0.0
		stdv_o = 0.0
		sqdiff_o = 0.0
		print()
		print("Day MJD")
		print(key)
		measurement_array_o = []  
		uncertainty_array_o = []
		time_array_o = []

		for row in value:

			print(row["mjd"], row["calc_flux"], row["calc_dflux"], row["weight"])   
			time_sum_o += float(row["mjd"])   
			flux_weight_product_sum_o += (float(row["calc_flux"])*float(row["weight"]))
			weight_sum_o += float(row["weight"])         
			measurement_array_o.append(row["calc_flux"]) 
			uncertainty_array_o.append(row["calc_dflux"]) 
			time_array_o.append(row["mjd"]) 
			r_flux_o.append(float(row["calc_flux"])) 
			r_dev_o.append(float(row["calc_dflux"])) 
			r_time_o.append(float(row["mjd"])) 

	  
		print()	
		mean_time_o = time_sum_o / len(value)
		weighted_flux_o = flux_weight_product_sum_o / weight_sum_o
		stdv_o = standard_deviation(measurement_array_o, uncertainty_array_o)

		m_time_o.append(mean_time_o)
		w_flux_o.append(weighted_flux_o)
		s_dev_o.append(stdv_o)
		num_o.append(len(value))

		if len(value) > 1:

			for row in value:

				sqdiff_o += float(row["weight"])*((weighted_flux_o - float(row["calc_flux"]))**2)

			ratio_o = (len(value)-1)/ len(value)
			weighted_variance_o = sqdiff_o/(ratio_o*weight_sum_o)
			weighted_standard_deviation_o = weighted_variance_o**(1/2) 
			new_error_o.append(weighted_standard_deviation_o)

# Sometimes, we will have a single data point for a day. The weighted standard deviation equation cannot cope with this, as it causes division by zero. For such cases, the raw error for that lone datapoint is used for the 'weighted error', and its value appended to the latter's appropriate array.

		elif len(value) == 1:

			stdv_o = standard_deviation(measurement_array_o, uncertainty_array_o)
			new_error_o.append(stdv_o)

	return r_time_o, r_flux_o, r_dev_o, m_time_o, w_flux_o, s_dev_o, num_o, new_error_o

	r_time_o = []
	r_flux_o = []
	r_dev_o = []
	m_time_o = []
	w_flux_o = []
	s_dev_o = []
	num_o = []
	new_error_o = []

