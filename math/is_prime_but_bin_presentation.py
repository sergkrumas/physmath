import math

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True



for n in range(1000):
    if is_prime(n):
        print( f'{n:012b}', n)


