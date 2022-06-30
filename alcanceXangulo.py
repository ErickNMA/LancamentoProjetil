import matplotlib.pyplot as plt
import math as m

v = 10.0

theta = []
r = []
alc_max = -1

for i in range(0, 90):
    theta.append(i)
    current_r = ((m.pow(v, 2)*m.sin(2*(i*(m.pi/180.0))))/9.807)
    r.append(current_r)
    if(current_r > alc_max):
        alc_max = current_r
        ang_max = i

print('Angulo para aclance maximo: ' + str(ang_max))

plt.plot(theta, r)
plt.show()