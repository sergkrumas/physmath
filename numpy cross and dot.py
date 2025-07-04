









import numpy as np

v = np.array([-10.4, -1.3, -3.5])


import math
sqrt = math.sqrt(2)

n = np.array([0.0, 1.0, 0.0])  


r1 = np.cross(np.cross(n, v), n)


r2 = v*np.dot(n, n) - 2*n*np.dot(n, v)



print(v)

print("cross prod", r1)
print("equivalent", r2)
