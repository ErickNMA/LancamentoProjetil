import math as m
import matplotlib.pyplot as plt



def g(x):

    R = 10**3

    C = 160*10**-9

    return (1/m.sqrt(((R*2*m.pi*x*C)**2)+1))



f = []
At = []

for i in range((10**4)+1):
    f.append(i)
    At.append(g(i))



plt.plot(f, At)
plt.show()