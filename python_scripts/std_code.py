def standard_deviation(array):


	mu = stat.mean(array)
	summ = 0
	denominator = len(array)-1

	for i in range(0, len(array)):

		diff = 0
		diff = mu - array[i]
		sq_diff = diff**2
		summ = summ + sq_diff

	variance = summ / denominator
	sigma = variance**(1/2)

	return sigma

array = [130.98, -16.168, -4.301, 19.726]

answer = standard_deviation(array)

print(answer)

# ANSWER SHOULD BE: 67.29246

