	index_o = float(row["zp"]) + float(row["apfit"])/(-2.5) + 9.56
	flux_numerator_o = float(row["peakfit"])*float(row["major"])*float(row["minor"])
	flux_value_o = (flux_numerator_o/exposuretime)*10**index_o
	row["calcflux"] = flux_value_o
