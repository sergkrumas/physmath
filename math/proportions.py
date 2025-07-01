






def main1():
    arguments = [0.920, 0.800, 0.670, 0.720]

    for arg in arguments:
        # считаем пропорцию
        x = arg*0.250/3
        y = arg*0.300/3

        # переводим обратно в граммы
        x*=1000
        y*=1000

        print(arg, x, y)



def calc_arg(argument):
    return 4586/6000*argument

def main2():

    print('сахар', calc_arg(200), 'гр.')
    print('масло', calc_arg(200), 'гр.')

    print('соль', calc_arg(30), 'гр.')
    print('уксус', calc_arg(100), 'гр.')




# main2()



def calc_arg3(argument):
    return 1682/2500*argument

def main3():

    print('свекла', calc_arg3(2.5), 'кг.')
    print('рост. масло', calc_arg3(150), 'мл.')

    print('соли', calc_arg3(2), '???')
    print('сахар', calc_arg3(6), '???')

    print('кислота', calc_arg3(2), '???')


# main3()
main2()
