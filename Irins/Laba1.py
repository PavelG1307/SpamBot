n = input('Введите число: ')
m =''
for i in range(len(n)-1,-1,-1):
    m += n[i]
print(f'Число задом наперед: {m}')