from math import sin, pi, exp

def f1(x):
    return 3 * x - sin(2 * x)

def f2(x):
    return exp(-2 * x) - 2 * x + 1

def integral(a,b,func):
    n = 1000
    f = 0
    for k in range(n):
        f += func(a+k*(b-a)/n)
    f = f*(b-a)/n
    return f

Q = integral(pi, 2*pi, f1) + integral(0, pi, f2)
print(Q)