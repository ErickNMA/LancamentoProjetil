import matplotlib.pyplot as plt
import time
import math as m
from tkinter import *
from tkinter import messagebox
import numpy as np
import cv2 as cv
import copy



v = 10.0
ang = 40.0
dist = 0.25
g = 9.807



x0 = (dist*m.cos(ang*(m.pi/180.0)))
y0 = (dist*m.sin(ang*(m.pi/180.0)))
vx = (v*m.cos(ang*(m.pi/180.0)))
vy = (v*m.sin(ang*(m.pi/180.0)))

rt_t = []
rt_x = []
rt_y = []
global rt_ymax, rt_tvoo, rt_tsub, rt_alc

def rt_sim():
    rt_t.clear()
    rt_x.clear()
    rt_y.clear()
    t0 = time.time()
    rt_ymax = -1
    rt_tvoo = -1
    rt_tsub = -1

    array = (np.ones((screen_h, screen_w, 3), dtype=np.float32)*255)

    x_space = int(screen_w/6.0)
    y_space = int(screen_h/6.0)

    k = ((screen_w-(2*x_space)) / calc_alc)
    if((k * calc_ymax) > (screen_h-(2*y_space))):
        k = ((screen_h-(2*y_space)) / calc_ymax)
    
   


    while(True):
        current_frame = copy.deepcopy(array)
        t = (time.time()-t0)

        cv.rectangle(current_frame, ((int((screen_w*6.7)/8.0)-10), (int((screen_h*0.5)/8.0))-35), ((int((screen_w*6.7)/8.0)+270), (int((screen_h*0.5)/8.0))+20), (0, 0, 0), 2)
        cv.putText(current_frame, ('Tempo: ' + str(round(t, 2)) + 's'), (int((screen_w*6.7)/8.0), int((screen_h*0.5)/8.0)), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 1)

        rt_t.append(t)
        x = (x0 + (vx*t))
        rt_x.append(x)
        y = (y0 + (vy*t) - ((g*m.pow(t, 2))/2.0))
        rt_y.append(y)

        cv.circle(current_frame, (int(x_space+(k*x)), int((screen_h-y_space)-(k*y))), 5, (0, 0, 255), -1)
        cv.imshow('Imagem', current_frame)
        cv.waitKey(1)

        if(y > rt_ymax):
            rt_ymax = y
            rt_tsub = t
        if(y < 0):
            rt_alc = (x + x0)
            rt_tvoo = t
            break
    cv.waitKey()
    #print(x, y)
    #print('\n=> Alcance: \t' + str(round(alcance, 4)) + ' m')
    #print('\n=> Altura maxima: \t' + str(round(rt_ymax, 4)) + ' m')
    #print('\n=> Tempo de trajetoria: \t' + str(round(rt_tvoo, 4)) + ' s')
    messagebox.showinfo(message='Valor de ângulo inválido!') 

rt_mode = 0

def rt_plot():
    if(rt_mode == 0):
        #y em função de x
        plt.plot(rt_x, rt_y)
    elif(rt_mode == 1):
        #y em função de t
        plt.plot(rt_t, rt_y)
    elif(rt_mode == 2):
        #x em função de t
        plt.plot(rt_t, rt_x)
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



calc_ymax = ((m.pow(v, 2)*pow(m.sin(ang*(m.pi/180.0)), 2))/(2*g))
calc_tvoo = (2*(vy/g))
calc_tsub = (vy/g)
calc_alc = ((m.pow(v, 2)*m.sin((2*ang)*(m.pi/180.0)))/g)



btn1 = Button(main_window, text='Iniciar Simulação', command=rt_sim, font='Impact 14', fg='#ffffff', bg='#9d9d9e')
btn1.grid(row=1, column=0)
btn2 = Button(main_window, text='Gráfico', command=rt_plot)
btn2.grid(row=2, column=0)

print(btn1.keys())

t1 = StringVar()
t1.set(('Aceleração em m/s'+'\u00B2'))

l1 = Label(main_window, textvariable=t1, width=20, height=2, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
#l1.grid(row=0, column=0)

e1 = Entry(main_window)
#e1.grid(row=3, column=0)

s1_val = IntVar()
s1 = Scale(main_window, from_=0, to=90, orient=HORIZONTAL, resolution=0.1, variable=s1_val)
#s1.grid(row=4, column=0)

ck1_val = IntVar()
ck1 = Checkbutton(main_window, text='Checkbox Exemplo', variable=ck1_val)
#ck1.grid(row=5, column=0)



#img1 = PhotoImage(file=array)
#lim1 = Label(main_window, image=array)
#lim1.grid(row=0, column=0)



main_window.mainloop()