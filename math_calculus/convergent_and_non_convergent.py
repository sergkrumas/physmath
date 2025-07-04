











N = 10000

value1 = 1 # расходящийся
value0 = 1 # сходящийся
for n in range(1, N):
    value1 += 1/n

print(value1)

d = 2
for n in range(1, N):
    value0 += 1/d
    d *= 2

# print(d)
# ValueError: Exceeds the limit (4300) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
print(value0)



##################################################################
##################################################################
##################################################################
##################################################################
