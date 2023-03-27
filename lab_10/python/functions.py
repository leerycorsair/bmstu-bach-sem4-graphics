from math import sqrt, sin, cos, exp

def f1(x, z):
    return sin(x) * sin(x) + cos(z) * cos(z)

def f2(x, z):
    return x**2 / 20 - z**2 / 20

def f3(x, z):
    return x**2 / 20 + z**2 / 20

def f4(x, z):
    return sin(sin(x) * sin(x) + cos(z) * cos(z))
