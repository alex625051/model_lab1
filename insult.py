from tkinter import *
import time
import random
from service import *
import math
import ghostscript
from numba import njit, prange
import copy
import multiprocessing
import decimal
import numpy
import concurrent.futures as pool
import pandas as pd
import json
import os.path


continued=False
showVisualDelay=1;
unlimetedSteps=True;
unlimetedLimits=False;
startIcellsFromCenter=True;
continuedVer='1.5'
# Вводные данные
nol0=decimal.Decimal('0')
X = 10;
Y = 10;
T = 300;
N_I=X*Y*0.3
N_D=X*Y*0.000
N_F=X*Y*0.0
k1=decimal.Decimal('0')/90; # H->I
k1minus=decimal.Decimal('0')/90; # I->H
k2=decimal.Decimal('0')/360; # I->D
k4=decimal.Decimal('0.0') # I->F
k4minus=decimal.Decimal('0.0') # F->I
k5=decimal.Decimal('0.0') # F->H
k7=decimal.Decimal('0.3')/90; # IH->HH
k8=decimal.Decimal('0.4')/90; # HI->II
k9=decimal.Decimal('0.4')/360 # HD->ID
k10=decimal.Decimal('0.2')/360 # ID->DD
k11=decimal.Decimal('0.2')/360 # II->DI

R = nol0; # глобальная переменная с R
FetaD_array=[]

speeds_dict={}
for i in prange(Y):
    for j in prange(X):
        speeds_dict[f'{i}_{j}']={'i':i,'j':j}

def start_status():
    board=[['H' for i2 in prange(X)] for i in prange(Y)]
    I=0
    D=0
    F=0
    if startIcellsFromCenter:
        xCenter = round(X / 2)
        yCenter = round(Y / 2)
        radius=math.ceil(math.sqrt(N_I/math.pi))
        pointsInRadius =list()
        for x in range(0, X):
            for y in range(0, Y):
                if math.sqrt((x - xCenter) ** 2 + (y - yCenter) ** 2) < radius:
                    pointsInRadius.append({"x": x, "y": y})
    while I < N_I:
        if startIcellsFromCenter:
            if not len(pointsInRadius):
                break
            onePoint=pointsInRadius.pop()
            x=onePoint['x'];y=onePoint['y'];
        else:
            x = random.randint(0, X - 1)
            y = random.randint(0, Y - 1)
        if board[y][x] == "H":
            I = I + 1
            board[y][x] = "I"
    while (D < N_D) and ((I+D)<X*Y):

        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        if board[y][x] == "H":
            D = D + 1
            board[y][x] = "D"
    while (F < N_F) and ((I+D+F)<X*Y):
        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        if board[y][x] == "H":
            F = F + 1
            board[y][x] = "F"

    return board
def get_event_2x2_limits(x, y, dx, dy): # граничные условия
    x2 = x + dx
    y2 = y + dy
    if unlimetedLimits:
        # Бесконечная решетка
        if x2 == X:
            x2 = 0;
        elif y2 == Y:
            y2 = 0;
        return x, y, dx, dy, x2, y2
    else:
        # Граничные условия с "H"
        if x2 == X:
            x2 = False;
        elif y2 == Y:
            y2 = False;
        return x, y, dx, dy, x2, y2



def get_event_2x2(x, y, dx, dy, board):  # Исследование 1 варианта развития событий при 2 узлах в 2 стороны
    # new_board = mcopy(board)
    ret = {'speed': nol0}
    x, y, dx, dy, x2, y2 = get_event_2x2_limits(x, y, dx, dy)
    ret['y'] = y;
    ret['x'] = x;
    if y2 and x2:
        secondCell= board[y2][x2]
        ret['y2'] = y2;
        ret['x2'] = x2;
    else:
        secondCell="H"


    if board[y][x] == 'I':
        if secondCell == 'I':
            ret['speed'] = k11  #
            ret['yx'] = "D"  #
            if y2 and x2:
                ret['y2x2'] = "I"  #
            return [ret]
    return []

def get_event_2x4_limits(x, y, dx, dy):
    x2 = x + dx
    y2 = y + dy
    if unlimetedLimits:
        if x2 == X:
            x2 = 0;
        elif y2 == Y:
            y2 = 0;
        elif x2 < 0:
            x2 = X - 1;
        elif y2 < 0:
            y2 = Y - 1;
        return x, y, dx, dy, x2, y2
    else:
        if x2 == X:
            x2 = False;
        elif y2 == Y:
            y2 = False;
        elif x2 < 0:
            x2 = False;
        elif y2 < 0:
            y2 = False;
        return x, y, dx, dy, x2, y2


def get_event_2x4(x,y,dx,dy,board): # Исследование 1 варианта развития событий при 2 узлах на 4 стороны
    # new_board=mcopy(board)
    ret={'speed':nol0}
    x, y, dx, dy, x2, y2 = get_event_2x4_limits(x, y, dx, dy)
    ret['y'] = y;
    ret['x'] = x;
    if y2 and x2:
        secondCell = board[y2][x2]
        ret['y2'] = y2;
        ret['x2'] = x2;
    else:
        secondCell = "H"


    if board[y][x] == 'H':
        if secondCell == 'I':
            ret['speed'] = k8  #
            ret['yx'] = "I"  #
            if y2 and x2:
                ret['y2x2'] = "I"  #
            return [ret]
        if secondCell == 'D':
            ret['speed'] = k9  #
            ret['yx'] = "I"  #
            if y2 and x2:
                ret['y2x2'] = "D"  #
            return [ret]

    if board[y][x] == 'I':
        if secondCell == 'H':
            ret['speed'] = k7  #
            ret['yx'] = "H"  #
            if y2 and x2:
                ret['y2x2'] = "H"  #
            return [ret]
        if secondCell == 'D':
            ret['speed'] = k10  #
            ret['yx'] = "D"  #
            if y2 and x2:
                ret['y2x2'] = "D"  #
            return [ret]
    return []


def get_r_event(R):
    Ep_minus2 = nol0
    Ep_minus1 = nol0
    E = decimal.Decimal(str(numpy.random.uniform()))
    # l=random.randint(0,len(first_line_events)-1)


  # напрямую
    for key in speeds_dict:
        if speeds_dict[key]['R_']==0:continue
        position_events=speeds_dict[key]['events_']
        for ev in position_events:
            ER=E*R
            # if ev['speed']==0:continue;
            if (ER>Ep_minus1) and ((ER)<=(Ep_minus1+ev['speed'])):
                # print(f'rand={E*R}, event={ev["speed"]}, left={Ep_minus1}, right={Ep_minus1+ev["speed"]}, R={R}')
                # print(events)
                return ev
            Ep_minus1=Ep_minus1+ev['speed']
    return False



def get_event_1(x,y,board): #получить события для одного узла
    ret=[]
    if board[y][x] == 'H':
        ret.append({"yx": "I", "speed": k1,    "x": x, "y": y});

    elif board[y][x] == 'I':
        ret.append({"yx": "H", "speed": k1minus,    "x": x, "y": y})
        ret.append({"yx": "D", "speed": k2,    "x": x, "y": y})
        ret.append({"yx": "F", "speed": k4,    "x": x, "y": y});

    elif board[y][x] == 'F':
        ret.append({"yx": "H", "speed": k5,    "x": x, "y": y});
        ret.append({"yx": "I", "speed": k4minus,    "x": x, "y": y});
    return ret

def inv_1_point(i,j,board):
    R_=nol0;
    events=[]
    # генерация скоростей для 4 направлений, добавлених в список событий и подсчет R
    # проверяем на все 4 направления=> обратные реакции учитываются, когда относительно следующей точки происходит проверка
    left = get_event_2x4(x=j, y=i, dx=-1, dy=0, board=board)
    right = get_event_2x4(x=j, y=i, dx=+1, dy=0, board=board)
    up = get_event_2x4(x=j, y=i, dx=0, dy=-1, board=board)
    down = get_event_2x4(x=j, y=i, dx=0, dy=+1, board=board)

    # узлы одинаковые - необходимо только 1 раз учитывать
    down2 = get_event_2x2(x=j, y=i, dx=0, dy=+1, board=board)
    right2 = get_event_2x2(x=j, y=i, dx=+1, dy=0, board=board)

    # смотрим сам узел
    this_point = get_event_1(x=j, y=i, board=board)

    for i in left:R_=R_+i['speed']
    for i in right:R_=R_+i['speed']
    for i in right2:R_=R_+i['speed']
    for i in up:R_=R_+i['speed']
    for i in down:R_=R_+i['speed']
    for i in down2:R_=R_+i['speed']
    for i in this_point:R_=R_+i['speed']


    # добавляем события. будут и с 0 вероятностью
    events=events+left
    events=events+right
    events=events+up
    events=events+down
    events=events+down2
    events=events+right2
    events=events+this_point
    return events, R_


def move_cell(board,t,changed_points):
    global speeds_dict
    global R
    #шаг 2
    # Вычисление скоростей элементарных событий. На текущий момент времени t1 и вычисление суммарной скорости R
    events=[]
    first_line_events=[]


    if changed_points:
        for point in changed_points:
            i=point['y']
            j=point['x']
            events_, R_ = inv_1_point(i, j, board)
            # events_=[i  for i in events_ if i['speed']>0]
            events = events + events_
            R = R - speeds_dict[f'{i}_{j}']['R_']
            speeds_dict[f'{i}_{j}']['R_'] = R_;
            speeds_dict[f'{i}_{j}']['events_'] = events_;


            R = R + speeds_dict[f'{i}_{j}']['R_']



    if not changed_points:
        for i in prange(Y):
            for j in prange(X):
                value = board[i][j]
                events_,R_ = inv_1_point(i,j,board)
                # events_=[i  for i in events_ if i['speed']>0]
                events=events+events_
                R=R+R_
                speeds_dict[f'{i}_{j}']['R_']=R_;
                speeds_dict[f'{i}_{j}']['events_']=events_;

    # for k in speeds_dict:
    #     R = R + speeds_dict[k]['R_']
    #         first_line_events.append({'i': speeds_dict[k]['i'], 'j': speeds_dict[k]['j'], 'R_': speeds_dict[k]['R_'], 'events_': speeds_dict[k]['events_']})


    # print(events)
    #шаг 3 Случайно выбирается одно из возможных элементарных событий с вероятностью, пропорциональной его скорости.
    # Изменяется состояние решётки в соответствии с выбранным событием
    ev = get_r_event(R=R)
    # шаг 4 Вычисление шага по времени. Вычисляется момент времени t2 выхода системы
    # из текущего состояния: t2=t1-ln(E)/R, где E - случайная величина, равномерно распределённая на интервале (0,1).
    E=decimal.Decimal(str(random.random()))
    if R==0:
        return False
    dt=decimal.Decimal(str(math.log(1/E)))/R
    t=t+dt
    try:
        board[ev['y']][ev['x']]=ev['yx']
    except:
        return False

    def get_near_points(x,y):
        x1 = x + 1
        y1 = y + 0
        x2 = x - 1
        y2 = y + 0
        x3 = x + 0
        y3 = y + 1
        x4 = x + 0
        y4 = y - 1
        if x1==X: x1=0
        if x2<0: x2=X-1
        if y3==Y: y3=0;
        if y4 <0: y4=Y-1
        return [{'x':x1,'y':y1},{'x':x2,'y':y2},{'x':x3,'y':y3},{'x':x4,'y':y4}]



    def get_changed_points(ev):
        points=[]
        points=points+get_near_points(x=ev['x'],y=ev['y'])
        if ev.get('y2x2'):
            points = points + get_near_points(x=ev['x2'], y=ev['y2'])
        else:
            points = points +[{'x':ev['x'],'y':ev['y']}]
        return points

    if ev.get('y2x2'):
        board[ev['y2']][ev['x2']] = ev['y2x2']

    changed_points=get_changed_points(ev)

    return board,t, changed_points


def main():
    global speeds_dict
    t = nol0
    step=0
    changed_points=[]
    # Рисовка объектов
    st = (700 * 2) / (X + Y)

    root, canvas = create_TK(width=st * X, height=st * Y)
    root.title('Метод Монте-Карло. t=0')
    #отрисовка решетки
    build_square(canvas,st, X,Y)
    build_board(canvas, st, X,Y)

    #step 1 Заполняем начальное состояние решетки
    board=start_status()

    # Продолжение работы:
    if continued and os.path.exists(f'out/present_status_{continuedVer}.json'):
        with open(f'out/present_status_{continuedVer}.json', 'r') as f:
            js=f.readlines()
            if len(js)>0:
                present_status=json.loads(js[-1], cls=DecimalDecoder)
                speeds_dict=present_status['speeds_dict']
                board=present_status['board']
                t=present_status['t']
                step=present_status['step']
                fetaD=present_status['fetaD']


    #отрисовка частиц в начальном состоянии и сохранение кадра визуализации
    checkers4(root, canvas, st, X, Y,board=board,visibable=True)
    root.title(f'Метод Монте-Карло. t={t}, step={step}')

    # save_as_png(canvas=canvas, fileName=f'out/00')


    while unlimetedSteps or t<=300: # Алгоритм работает до времени T, отображаем каждый 10, создаем анимацию Гиф
        # tt1=time.time()
        step=step+1
        try:
            board, t, changed_points = move_cell(board=board, t=t, changed_points=changed_points)
        except:
            print("Нет возможных событий для текущего состояния системы.\n Нажмите любую клавишу")
            pause_var = StringVar()
            root.bind('<Key>', lambda e: pause_var.set(1))
            root.wait_variable(pause_var)
            exit()

        # конец работы основного алгоритма ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


        # Формирование кадров демонстрационой анимации
        if step % showVisualDelay == 0:
            # time.sleep(1)
            root.title(f'Метод Монте-Карло. t={t}, step={step}')

            fetaD = checkers4(root, canvas, st, X, Y, board=board, visibable=True)
            dF=pd.DataFrame(FetaD_array)
            dF.to_csv(f'out/FetaD_array_{continuedVer}.csv',index=False,mode='a',header=False)
            if continued:
                present_status={'speeds_dict':speeds_dict, 'board':board,'t':t,'step':step,'fetaD':fetaD}
                with open(f'out/present_status_{continuedVer}.json','a') as f:
                    f.write(json.dumps(present_status,cls=DecimalEncoder)+'\n')




        if step%1000==0:
            # time.sleep(1)
            # root.title(f'Метод Монте-Карло. t={t}, step={step}')

            fetaD=checkers4(root, canvas, st, X, Y,board=board,visibable=False)
            FetaD_array.append({'fetaD':fetaD,'t':t})
            # print(time.time()-tt1)
        # if i%100==0:
        #     canvas.create_text(250, 20, fill="black", font="Times 30 italic bold",
        #                        text=f"t={t}, step={i}")
        #     save_as_png(canvas=canvas, fileName=f'out/{i}')

    #Формирование файла демонстрационой анимации
    # images[0].save('out/KMK_Kurkina.gif',
    #                save_all=True,
    #                append_images=images[1:],
    #                duration=1000,
    #                loop=0)

    root.mainloop()

if __name__ == '__main__':
    main()
