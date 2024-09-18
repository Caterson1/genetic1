import math
import sympy
from vectors import *

totalint = 0

for x in range(50):
    totalint += sympy.fibonacci(x)
    print(totalint)

list = [Vec(1) + Vec(1) + Vec(1)]
print(sum(list, Vec()))