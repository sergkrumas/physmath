






def fit_complex(t, input_a, input_b, output_a, output_b):
	# input_min = min(input_a, input_b)
	# input_max = max(input_a, input_b)
	# output_max = max(output_a, output_b)
	# output_min = min(output_a, output_b)
	input_min = input_a
	input_max = input_b
	output_min = output_a
	output_max = output_b
	t = max(input_min, min(input_max, t))
	factor = t/(input_max-input_min)
	output = output_min + factor*(output_max-output_min) 
	return output




def fit(t, input_a, input_b, output_a, output_b):
	t = max(input_a, min(input_b, t))
	factor = (t-input_a)/(input_b-input_a)
	return output_a + factor*(output_b-output_a)

def fit01(t, output_a, output_b):
	return fit(t, 0.0, 1.0, output_a, output_b)


for i in range(-10, 11): #range(-20, 21):
	value = (i/10)
	o1 = fit01(value, -100, 300)
	o2 = fit(value, 0.0, 1.0, 200, -100)
 
	if value == -1.0 or value == 0.0:
		print('-'*50)
	print(str(value).rjust(10), str(o1).rjust(10), str(o2).rjust(10))
	if value == 1.0:
		print('-'*50)
