











    # алгоритм считает площадь каждой из трёх частей квадрата, образованными линиями графиков функций x^2 и sqrt(x)
    # каждая часть должна быть в итоге равна 1/3




import random
import math



class Point():

    def __init__(self):
        self.x = random.random()
        self.y = random.random()

    def __str__(self):
        return f'{self.x} {self.y}'


def main():

    count = 1000000

    unter_parabola = 0
    ueber_sqrt = 0
    middle = 0

    count_passed = 0


    for n in range(count):

        p = Point()

        middle = False
        unter_sqrt = False
        ueber_parabola = False

        if p.y <= (p.x**2) :
            unter_parabola += 1
        else:
            ueber_parabola = True

        if p.y >= math.sqrt(p.x):
            ueber_sqrt += 1
        else:
            unter_sqrt = True

        if ueber_parabola and unter_sqrt:
            middle += 1
            unter_sqrt = False
            ueber_parabola = False

        count_passed += 1

        part1_area = unter_parabola/count_passed
        part2_area = ueber_sqrt/count_passed
        part3_area = middle/count_passed

        all_area = part1_area + part2_area + part3_area

        print(part1_area, part2_area, part3_area, all_area)



main()





