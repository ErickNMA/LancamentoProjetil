import matplotlib.pyplot as plt
import time
import math as m
from tkinter import *



v = 10.0
ang = 40.0
x0 = 0.15
y0 = 0.10



vx = (v*m.cos(ang*(m.pi/180.0)))
vy = (v*m.sin(ang*(m.pi/180.0)))

et = []
ex = []
ey = []

def time_sim():
    t0 = time.time()
    alt_max = -1
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

def traj_plot():
    plt.plot(ex, ey)
    plt.show()

 

main_window = Tk()
main_window.title('Lançamento Oblíquo')
screen_w = main_window.winfo_screenwidth()
screen_h = main_window.winfo_screenheight()
main_window.geometry('%dx%d+%d+%d' % (screen_w, screen_h, 0, 0))
main_window.resizable(False, False)
main_window.state('zoomed')
main_window.iconbitmap('logo.ico')
main_window['bg'] = 'gray'

btn1 = Button(main_window, text='Iniciar Simulação', command=time_sim)
btn1.pack()
btn2 = Button(main_window, text='Gráfico', command=traj_plot)
btn2.pack()


main_window.mainloop()