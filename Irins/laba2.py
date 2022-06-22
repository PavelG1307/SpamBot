from random import randint

N = 5
M = 11

x = randint(N,M)
print(f'Число {x}')

def chetvert_coord_ploscosti():
    x = int(input('Введите х: '))
    y = int(input('Введите у: '))
    if x > 0 and y > 0:
        print('Точка в 1 четверти')
    elif x < 0 and y > 0:
        print('Точка во 2 четверти')
    elif x < 0 and y < 0:
        print('Точка в 3 четверти')
    elif x > 0 and y < 0:
        print('Точка в 4 четверти')
    elif x == 0 and y == 0:
        print('Точка в начале координат')
    elif x == 0:
        print('Точка на оси х')
    elif y == 0:
        print('Точка на оси y')

if x == 5:
    rimsk_chislo = 'V'
elif x == 6:
    rimsk_chislo = 'VI'
elif x == 7:
    rimsk_chislo = 'VII'
    chetvert_coord_ploscosti()
elif x == 8:
    rimsk_chislo = 'VIII'
elif x == 9:
    rimsk_chislo = 'IX'
elif x == 10:
    rimsk_chislo = 'X'
elif x == 11:
    rimsk_chislo = 'XI'      
print(f'Римское число: {rimsk_chislo}')  