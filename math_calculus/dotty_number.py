













import math


x = math.pi/2
counter = 0

while counter < 100:
	print(counter, x)
	x = math.cos(x)
	counter +=1

print(math.cos(x))
