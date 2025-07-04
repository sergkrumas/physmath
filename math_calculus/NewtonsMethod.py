














# метод Ньютона
x1 = x2 = 1000.0
a = 25

for n in range(20):
    a2 = a/x1
    x1_old = x1
    x1 = 0.5 *(x1 + a2)
    x2 = x2 - (x2*x2-a)/(2*x2)

    print(n, x1, x2, a2, x1_old)



print()






# метод касательных
x1 = 100
x2 = 1000
a = 25 

def func(x):
    return x*x - a

for n in range(20):
    
    old_x2 = x2

    func_diff = func(x2) - func(x1)
    if func_diff == 0.0:
        break
    x2 = x1 - func(x1) * ((x2-x1)/func_diff)

    x1 = old_x2

    print(n, x2)

