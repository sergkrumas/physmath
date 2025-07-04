




s = 0
import math
for n in range(100):
	s += 0.05
	print( "%2s: " % n,math.ceil(s), math.floor(s), round(s), math.trunc(s)," ", s)
