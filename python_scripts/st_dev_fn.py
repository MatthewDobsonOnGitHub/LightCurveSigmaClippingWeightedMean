######### STANDARD DEVIATION FUNCTION (WILL BE USEFUL LATER) #########

def standard_deviation(array):

	mu = stat.mean(array)

	summ = 0

	for i in range(0, len(array)):

		diff = mu - array[i]

		sq_diff = diff**2

		summ = summ + sq_diff


denominator = len(array) - 1

variance = summ / denominator

sigma = variance**(1/2)

return sigma
