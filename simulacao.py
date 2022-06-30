import matplotlib.pyplot as plt
import time
import math as m

t0 = time.time()

v = 10.0
ang = 40.0
x0 = 0.15
y0 = 0.10

vx = (v*m.cos(ang*(m.pi/180.0)))
vy = (v*m.sin(ang*(m.pi/180.0)))

alt_max = -1

et = []
ex = []
ey = []

while(True):
    t = (time.time()-t0)
    et.append(t)
    x = (x0 + (vx*t))
    ex.append(x)
    y = (y0 + (vy*t) - ((9.807*m.pow(t, 2))/2.0))
    ey.append(y)
    if(y > alt_max):
        alt_max = y
    if(y < 0):
        alcance = (x + x0)
        t_voo = t
        break
    print(x, y)

print('\n=> Alcance: \t' + str(round(alcance, 4)) + ' m')
print('\n=> Altura maxima: \t' + str(round(alt_max, 4)) + ' m')
print('\n=> Tempo de trajetoria: \t' + str(round(t_voo, 4)) + ' s')  

plt.plot(ex, ey)
plt.show()