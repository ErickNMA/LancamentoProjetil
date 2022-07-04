import matplotlib.pyplot as plt
import time
import math as m
from tkinter import *
from tkinter import messagebox



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
    messagebox.showinfo(message='Valor de ângulo inválido!') 

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
main_window['bg'] = '#444445'

btn1 = Button(main_window, text='Iniciar Simulação', command=time_sim, font='Impact 14', fg='#ffffff', bg='#9d9d9e')
btn1.grid(row=1, column=0)
btn2 = Button(main_window, text='Gráfico', command=traj_plot)
btn2.grid(row=2, column=0)

t1 = StringVar()
t1.set(('Aceleração em m/s'+'\u00B2'))

l1 = Label(main_window, textvariable=t1, width=20, height=2, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
l1.grid(row=0, column=0)

e1 = Entry(main_window)
e1.grid(row=3, column=0)

s1 = Scale(main_window, from_=0, to=90, orient=HORIZONTAL, resolution=0.1)
print(s1.keys())
s1.grid(row=4, column=0)



main_window.mainloop()