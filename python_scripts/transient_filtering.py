for i in range(0, len(peakfit)):

	index_o = (zeropoint_o[i] + apfit_o[i])/(-2.5) + 9.56
	flux_numerator_o = peakfit_o[i]*major_o[i]*minor_o[i]
	flux_value_o = (flux_numerator_o/exposuretime)*10**index_o
	flux_o.append(flux_value_o)

	index_c = (zeropoint_c[i] + apfit_c[i])/(-2.5) + 9.56
	flux_numerator_c = peakfit_c[i]*major_c[i]*minor_c[i]
	flux_value_c = (flux_numerator_c/exposuretime)*10**index_c
	flux_c.append(flux_value_c)


for i in range(0, len(dpeakfit)):
	index_o = (zeropoint_o[i] + apfit_o[i])/(-2.5) + 9.56
	dflux_numerator_o = dpeakfit_o[i]*major_o[i]*minor_o[i]
	dflux_value_o = (dflux_numerator_o/exposuretime)*10**index_o
	dflux_o.append(dflux_value_o)

	index_c = (zeropoint_c[i] + apfit_c[i])/(-2.5) + 9.56
	dflux_numerator_c = dpeakfit_c[i]*major_c[i]*minor_c[i]
	dflux_value_c = (dflux_numerator_c/exposuretime)*10**index_c
	dflux_c.append(dflux_value_c)
