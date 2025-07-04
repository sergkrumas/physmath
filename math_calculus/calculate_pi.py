








import math



pi_value = 2

NUMBER_OF_ITERATIONS = 100000000

for n in range(1, NUMBER_OF_ITERATIONS, 2):
	rational = (n+1)/(n)
	pi_value *= rational
	rational = (n+1)/(n+2)
	pi_value *= rational
print("выч ", pi_value)
print("наст", math.pi)



print(math.sqrt(2)+math.sqrt(3), math.pi)
