import matplotlib.pyplot as plt
import time
import math as m
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
import numpy as np
import cv2 as cv
import copy



#global v, ang, dist, g

v = 30.0
ang = 45.0
dist = 0.25
g = 9.807



x0 = (dist*m.cos(ang*(m.pi/180.0)))
y0 = (dist*m.sin(ang*(m.pi/180.0)))
vx = (v*m.cos(ang*(m.pi/180.0)))
vy = (v*m.sin(ang*(m.pi/180.0)))

calc_ymax = ((m.pow(v, 2)*pow(m.sin(ang*(m.pi/180.0)), 2))/(2*g))
calc_tvoo = (2*(vy/g))
calc_tsub = (vy/g)
calc_alc = ((m.pow(v, 2)*m.sin((2*ang)*(m.pi/180.0)))/g)

rt_t = []
rt_x = []
rt_y = []
global rt_ymax, rt_tvoo, rt_tsub, rt_alc, rt_img

def rt_sim():
    if(calc()):
        return 1
    rt_t.clear()
    rt_x.clear()
    rt_y.clear()
    t0 = time.time()
    rt_ymax = 0
    rt_x_ymax = 0
    rt_tvoo = 0
    rt_tsub = 0
    rt_alc = 0

    array = (np.ones((screen_h, screen_w, 3), dtype=np.float32)*255)

    x_space = int(screen_w/6.0)
    y_space = int(screen_h/6.0)

    k = ((screen_w-(2*x_space)) / calc_alc)
    if((k * calc_ymax) > (screen_h-(2*y_space))):
        k = ((screen_h-(2*y_space)) / calc_ymax)
    
    dx_vet = int(80/(m.sqrt(1+m.tan(ang*(m.pi/180.0)))))
    dy_vet = int(80/(m.sqrt(1+(1.0/m.tan(ang*(m.pi/180.0))))))
    
    
    #Fixar problemas de largura da área de simulação e detalhes nos cálculos, passando detalhes, faltando detalhes...


    while(True):
        current_frame = copy.deepcopy(array)
        t = (time.time()-t0)

        #Cronômetro:
        cv.rectangle(current_frame, ((int((screen_w*6.4)/8.0)-10), (int((screen_h*0.5)/8.0))-35), ((int((screen_w*6.4)/8.0)+270), (int((screen_h*0.5)/8.0))+20), (0, 0, 0), 2)
        cv.putText(current_frame, ('Tempo: ' + str(round(t, 2)) + 's'), (int((screen_w*6.4)/8.0), int((screen_h*0.5)/8.0)), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 1)

        #Vetor v0:
        #Ver direção da seta...
        current_frame = cv.arrowedLine(current_frame, (int(x_space+(k*x0)), int(screen_h-y_space-(k*y0))), (int((x_space+(k*x0))+dx_vet), int((screen_h-y_space-(k*y0))-dy_vet)), (0, 100, 255), 6, tipLength=0.2)
        cv.putText(current_frame, ('V = ' + str(round(v, 2)) + 'm/s'), (int((x_space+(k*x0))+dx_vet-180), int((screen_h-y_space-(k*y0))-dy_vet+30)), cv.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1)
        #cv.putText(current_frame, ('\u00D8' + ' = ' + str(round(ang, 1)) + '\u00B0'), (int((x_space+(k*x0))+dx_vet-180), int((screen_h-y_space-(k*y0))-dy_vet+80)), cv.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1)

        rt_t.append(t)
        x = (x0 + (vx*t))
        rt_x.append(x)
        y = (y0 + (vy*t) - ((g*m.pow(t, 2))/2.0))
        rt_y.append(y)

        #Ângulo em tempo real:
        current_vy = (vy - (g*t))
        current_angle = ((m.atan(current_vy/vx)/m.pi)*180.0)

        #Cota horizontal:
        cv.line(current_frame, (int(x_space+(k*x0)), int(screen_h-y_space)), (int(x_space+(k*x0)), int((screen_h-y_space)+50)), (0, 0, 0), 3)
        current_frame = cv.arrowedLine(current_frame, (int(x_space+(k*x0)), int((screen_h-y_space)+25)), (int(x_space+(k*x)), int((screen_h-y_space)+25)), (0, 0, 0), 3, tipLength=0.03)
        cv.putText(current_frame, ('R = ' + str(round(x, 2)) + 'm'), (int(((int(x_space+(k*x))-int(x_space+(k*x0)))/2.0)+x_space-100), int((screen_h-y_space)+70)), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 1)

        #Cota vertical:
        cv.line(current_frame, (int((x_space+(k*rt_x_ymax))-25), int(screen_h-y_space)), (int((x_space+(k*rt_x_ymax))+25), int(screen_h-y_space)), (0, 0, 0), 3)
        current_frame = cv.arrowedLine(current_frame, (int(x_space+(k*rt_x_ymax)), int(screen_h-y_space)), (int(x_space+(k*rt_x_ymax)), int(screen_h-y_space-(k*rt_ymax))), (0, 0, 0), 3, tipLength=0.06)
        cv.putText(current_frame, ('h = ' + str(round(rt_ymax, 2)) + 'm'), (int(x_space+(k*rt_x_ymax)+20), int(screen_h+((int(screen_h-y_space-(k*rt_ymax))-int(screen_h-y_space))/2.0)-y_space)), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 1)
        cv.putText(current_frame, ('t = ' + str(round(rt_tsub, 2)) + 's'), (int(x_space+(k*rt_x_ymax)-45), int(screen_h-y_space-(k*rt_ymax))-20), cv.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1)

        #Vetores vx e vy:
        current_frame = cv.arrowedLine(current_frame, (int(x_space+(k*x)), int((screen_h-y_space)-(k*y))), (int(x_space+(k*x)+(vx*3)), int((screen_h-y_space)-(k*y))), (0, 0, 0), 3, tipLength=0.1)
        current_frame = cv.arrowedLine(current_frame, (int(x_space+(k*x)), int((screen_h-y_space)-(k*y))), (int(x_space+(k*x)), int((screen_h-y_space)-(k*y)-(current_vy*3))), (0, 0, 0), 3, tipLength=0.1)
        cv.putText(current_frame, ('Vx = ' + str(round(vx, 2)) + 'm/s'), (int(x_space+(k*x)+(vx*3)+10), int((screen_h-y_space)-(k*y)-30)), cv.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1)
        cv.putText(current_frame, ('Vy = ' + str(round(current_vy, 2)) + 'm/s'), (int(x_space+(k*x)+10), int((screen_h-y_space)-(k*y)-(current_vy*3)-(30*(abs(current_angle)/current_angle)))), cv.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1)

        #Vetor v:
        mod_v = m.sqrt(m.pow(vx, 2)+m.pow(current_vy, 2))
        current_frame = cv.arrowedLine(current_frame, (int(x_space+(k*x)), int((screen_h-y_space)-(k*y))), (int(x_space+(k*x)+((mod_v*m.cos(current_angle*(m.pi/180.0)))*3)), int((screen_h-y_space)-(k*y)-((mod_v*m.sin(current_angle*(m.pi/180.0)))*3))), (0, 0, 0), 4, tipLength=0.15)

        #Rastro de trajetória:
        cv.circle(array, (int(x_space+(k*x)), int((screen_h-y_space)-(k*y))), 5, (0, 0, 255), -1)

        #Projétil:
        cv.circle(current_frame, (int(x_space+(k*x)), int((screen_h-y_space)-(k*y))), 10, (255, 0, 0), -1)
        
        cv.imshow('Imagem', array)
        cv.imshow('Imagem', current_frame)
        cv.waitKey(1)

        if(y > rt_ymax):
            rt_ymax = y
            rt_x_ymax = x
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
    #messagebox.showinfo(message='Valor de ângulo inválido!')

    t2.set('Tempo de voo: \t' + str(round(rt_tvoo, 2)) + 's')
    t4.set('Alcance: \t' + str(round(rt_alc, 2)) + 'm')
    t6.set('Altura: \t' + str(round(rt_ymax, 2)) + 'm')

    #mix_img(array, current_frame)

    return 0

def plotagem():
    if(len(rt_t) > 1):
        if(ra_val.get() == 1):
            plt.title('Lançamento Oblíquo: V = ' + str(v) + 'm/s e ângulo de ' + str(ang) + ' graus')
            plt.xlabel('Tempo (s)')
            plt.ylabel('x (m)')
            plt.plot(rt_t, rt_x)
        elif(ra_val.get() == 2):
            plt.title('Lançamento Oblíquo: V = ' + str(v) + 'm/s e ângulo de ' + str(ang) + ' graus')
            plt.xlabel('Tempo (s)')
            plt.ylabel('y (m)')
            plt.plot(rt_t, rt_y)
        elif(ra_val.get() == 3):
            plt.title('Lançamento Oblíquo: V = ' + str(v) + 'm/s e ângulo de ' + str(ang) + ' graus')
            plt.xlabel('x (m)')
            plt.ylabel('y (m)')
            plt.plot(rt_x, rt_y)
        plt.show()
    else:
        messagebox.showinfo(message='A simulação deve ser executada antes da plotagem!')

def calc():
    global v, ang, g, x0, y0, vx, vy, calc_ymax, calc_tvoo, calc_tsub, calc_alc
    try:
        v = float(e1.get())
        if(v <= 0):
            messagebox.showinfo(message='Informe uma velocidade positiva e com casas decimais separadas por ponto!')
            return 1
    except:
        messagebox.showinfo(message='Informe uma velocidade positiva e com casas decimais separadas por ponto!') 
        return 1
    ang = s1_val.get()
    aux = e2.get()
    if(aux == ''):
        g = 9.807
    else:
        try:
            g = float(aux)
            if(g <= 0):
                messagebox.showinfo(message='Informe uma gravidade positiva e com casas decimais separadas por ponto!') 
                return 1
        except:
            messagebox.showinfo(message='Informe uma gravidade positiva e com casas decimais separadas por ponto!') 
            return 1

    x0 = (dist*m.cos(ang*(m.pi/180.0)))
    y0 = (dist*m.sin(ang*(m.pi/180.0)))
    vx = (v*m.cos(ang*(m.pi/180.0)))
    vy = (v*m.sin(ang*(m.pi/180.0)))

    calc_ymax = ((m.pow(v, 2)*pow(m.sin(ang*(m.pi/180.0)), 2))/(2*g))
    calc_tvoo = (2*(vy/g))
    calc_tsub = (vy/g)
    calc_alc = ((m.pow(v, 2)*m.sin((2*ang)*(m.pi/180.0)))/g)

    t1.set('Tempo de voo: \t' + str(round(calc_tvoo, 2)) + 's')
    t3.set('Alcance: \t' + str(round(calc_alc, 2)) + 'm')
    t5.set('Altura: \t' + str(round(calc_ymax, 2)) + 'm')
    


    return 0
    
#def mix_img(im1, im2):
    #out = (np.ones((screen_h, screen_w, 3), dtype=np.float32)*255)
    #for i in range(len(im1)):
        #for j in range(len(im1[0])):
            #if((im1[i][j][0] != 255) or (im1[i][j][1] != 255) or (im1[i][j][2] != 255)):
                #out[i][j] = im1[i][j]
            #if((im2[i][j][0] != 255) or (im2[i][j][1] != 255) or (im2[i][j][2] != 255)):
                #out[i][j] = im2[i][j]
    #rt_img = copy.deepcopy(out)

#def grav():
#    if(ck1_val.get()):
#        e2_st.set('disabled')
#    else:
#        e2_st.set('normal')
    

 

main_window = Tk()
main_window.title('Lançamento Oblíquo')
screen_w = main_window.winfo_screenwidth()
screen_h = main_window.winfo_screenheight()
main_window.geometry('%dx%d+%d+%d' % (screen_w, screen_h, 0, 0))
main_window.resizable(False, False)
main_window.state('zoomed')
main_window.iconbitmap('logo.ico')
main_window['bg'] = '#444445'





#label1.place(x=0, y=0)

space = 5

#Linha 0:
#Espaçador:
Label(main_window, width=17, height=8, bg='#444445').grid(row=0, column=0)
Label(main_window, width=17, height=8, bg='#444445').grid(row=0, column=8)

#Linha 1:
Label(main_window, text='Parâmetros:', font='Impact 20', fg='#000000', bg='#444445').grid(row=1, column=4, padx=space, pady=space)

#Linha 2:
Label(main_window, text='Velocidade: (m/s)', font='Impact 14', fg='#000000', bg='#444445').grid(row=2, column=3, padx=space, pady=space)
Label(main_window, text=('Ângulo: (' + '\u00B0' + ')'), font='Impact 14', fg='#000000', bg='#444445').grid(row=2, column=4, padx=space, pady=space)
Label(main_window, text=('Gravidade: (m/s' + '\u00B2' + ')'), font='Impact 14', fg='#000000', bg='#444445').grid(row=2, column=5, padx=space, pady=space)

#Linha 3:
#Entrada de velocidade:
e1 = Entry(main_window, width=6)
e1.grid(row=3, column=3, padx=space, pady=space)
#Entrada de ângulo:
s1_val = DoubleVar()
s1 = Scale(main_window, from_=1, to=90, orient=HORIZONTAL, resolution=0.1, variable=s1_val)
s1.grid(row=3, column=4, padx=space, pady=space)
#Entrada de gravidade:
#ck1_val = IntVar()
#ck1 = Checkbutton(main_window, text=('g = 9.807 m/s'+'\u00B2'), variable=ck1_val, command=grav)
#ck1.grid(row=3, column=4, padx=space, pady=space)
e2_st = StringVar()
e2_st.set('normal')
e2 = Entry(main_window, state=e2_st.get(), width=6)
e2.grid(row=3, column=5, padx=space, pady=space)

#Linha 4:
#Espaçador:
Label(main_window, width=22, height=12, bg='#444445').grid(row=4, column=2)
Label(main_window, width=22, height=12, bg='#444445').grid(row=4, column=6)

#Linha 5:
Label(main_window, text='Teórico:', font='Impact 20', fg='#000000', bg='#444445').grid(row=5, column=1, padx=space, pady=space)
Label(main_window, text='Gráfico:', font='Impact 20', fg='#000000', bg='#444445').grid(row=5, column=4, padx=space, pady=space)
Label(main_window, text='Simulação:', font='Impact 20', fg='#000000', bg='#444445').grid(row=5, column=7, padx=space, pady=space)

#Linha 6:
#Botão calcular:
btn1 = Button(main_window, text='Calcular', command=calc, font='Impact 14', fg='#ffffff', bg='#9d9d9e')
btn1.grid(row=6, column=1, padx=space, pady=space)
Label(main_window, text='Dados (simulação):', font='Impact 14', fg='#000000', bg='#444445').grid(row=6, column=4, padx=space, pady=space)
#Botão iniciar simulação:
btn1 = Button(main_window, text='Iniciar Simulação', command=rt_sim, font='Impact 14', fg='#ffffff', bg='#9d9d9e')
btn1.grid(row=6, column=7, padx=space, pady=space)

#Linha 7:
t1 = StringVar()
t1.set('Tempo de voo: ')
l1 = Label(main_window, textvariable=t1, width=25, height=1, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
l1.grid(row=7, column=1, padx=space, pady=space)
ra_val = IntVar()
ra1 = Radiobutton(main_window, text='x | t', variable=ra_val, value=1)
ra1.grid(row=7, column=4, padx=space, pady=space)
t2 = StringVar()
t2.set('Tempo de voo: ')
l2 = Label(main_window, textvariable=t2, width=25, height=1, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
l2.grid(row=7, column=7, padx=space, pady=space)

#Linha 8:
t3 = StringVar()
t3.set('Alcance: ')
l3 = Label(main_window, textvariable=t3, width=25, height=1, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
l3.grid(row=8, column=1, padx=space, pady=space)
ra2 = Radiobutton(main_window, text='y | t', variable=ra_val, value=2)
ra2.grid(row=8, column=4, padx=space, pady=space)
t4 = StringVar()
t4.set('Alcance: ')
l4 = Label(main_window, textvariable=t4, width=25, height=1, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
l4.grid(row=8, column=7, padx=space, pady=space)

#Linha 9:
t5 = StringVar()
t5.set('Altura: ')
l5 = Label(main_window, textvariable=t5, width=25, height=1, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
l5.grid(row=9, column=1, padx=space, pady=space)
ra3 = Radiobutton(main_window, text='y | x', variable=ra_val, value=3)
ra3.grid(row=9, column=4, padx=space, pady=space)
t6 = StringVar()
t6.set('Altura: ')
l6 = Label(main_window, textvariable=t6, width=25, height=1, anchor=CENTER, justify=CENTER, font='Impact 14', fg='#000000', bg='#ffffff', bd=3, relief='sunken')
l6.grid(row=9, column=7, padx=space, pady=space)

#Linha 10:
btn2 = Button(main_window, text='Plotar', command=plotagem, font='Impact 14', fg='#ffffff', bg='#9d9d9e')
btn2.grid(row=10, column=4, padx=space, pady=space)

	
#asksaveasfile(mode='w', **options)



#Label(main_window, width=10, height=10, bg='#444445').grid(row=1, column=5)



#img1 = PhotoImage(file=array)
#lim1 = Label(main_window, image=array)
#lim1.grid(row=0, column=0)



main_window.mainloop()