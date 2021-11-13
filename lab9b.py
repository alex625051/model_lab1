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

# Вводные данные
nol0=decimal.Decimal('0')
X = 20;
Y = 20;
T = 300;
Nco=X*Y*0.5
No=X*Y*0.0
Pco=decimal.Decimal('0.3');k1_=decimal.Decimal('10000');k1=decimal.Decimal(Pco*k1_);
k1minus=decimal.Decimal('300')
k2=decimal.Decimal('2500')
k3=decimal.Decimal('25000')
k4=decimal.Decimal('0.11')
k5=decimal.Decimal('0.0065')
k6=decimal.Decimal('100000')
k7=k6
k8=k6


def get_event_2x2(x, y, dx, dy, board):  # Исследование 1 варианта развития событий при 2 узлах в 2 стороны
    # new_board = mcopy(board)
    ret = {'speed': nol0}
    x2 = x + dx
    y2 = y + dy
    if x2 == X:
        x2 = 0;
    elif y2 == Y:
        y2 = 0;
    ret['y'] = y;
    ret['x'] = x;
    ret['y2'] = y2;
    ret['x2'] = x2;

    if board[y][x] == '*':
        if board[y2][x2] == '*':
            ret['speed'] = k2  #
            ret['yx'] = "[O]"  #
            ret['y2x2'] = "[O]"  #
            return [ret]

    return []


def get_event_2x4(x,y,dx,dy,board): # Исследование 1 варианта развития событий при 2 узлах на 4 стороны
    # new_board=mcopy(board)
    ret={'speed':nol0}
    x2=x+dx
    y2=y+dy
    if x2==X:x2=0;
    elif y2==Y:y2=0;
    elif x2<0:x2=X-1;
    elif y2<0:y2=Y-1;
    ret['y'] = y;
    ret['x'] = x;
    ret['y2'] = y2;
    ret['x2'] = x2;

    if board[y][x]=='[CO]':
        if board[y2][x2]=='[O]':
            ret['speed']=k3  #
            ret['yx']="*" #
            ret['y2x2']="*" #
            return [ret]
        elif board[y2][x2]=='[O]v':
            ret['speed']=k5  #
            ret['yx']="*" #
            ret['y2x2']="*" #
            return [ret]
        elif board[y2][x2]=='*':
            ret['speed']=k6  #
            ret['yx']="*" #
            ret['y2x2']="[CO]" #
            return [ret]

    elif board[y][x]=='[O]':
        if board[y2][x2]=='*':
            ret['speed']=k7  #
            ret['yx']="*" #
            ret['y2x2']="[O]" #
            return [ret]

    elif board[y][x]=='[O]v':
        if board[y2][x2]=='*':
            ret['speed']=k8  #
            ret['yx']="*" #
            ret['y2x2']="[O]v" #
            return [ret]

# ### TEST!!!
#     elif board[y][x] == '*':
#         if board[y2][x2] == '*':
#             ret['speed'] = k2  #
#             ret['yx'] = "[O]"  #
#             ret['y2x2'] = "[O]"  #
#             return [ret]
#
#     elif board[y][x]=='[O]':
#         if board[y2][x2]=='[CO]':
#             ret['speed']=k3  #
#             ret['yx']="*" #
#             ret['y2x2']="*" #
#             return [ret]
#
#     elif board[y][x]=='[O]v':
#         if board[y2][x2]=='[CO]':
#             ret['speed']=k5  #
#             ret['yx']="*" #
#             ret['y2x2']="*" #
#             return [ret]
#
#     if board[y][x]=='*':
#         if board[y2][x2]=='[CO]':
#             ret['speed']=k6  #
#             ret['yx']="[CO]" #
#             ret['y2x2']="*" #
#             return [ret]
#         elif board[y2][x2]=='[O]':
#             ret['speed']=k7  #
#             ret['yx']="[O]" #
#             ret['y2x2']="*" #
#             return [ret]
#         elif board[y2][x2]=='[O]v"':
#             ret['speed']=k8  #
#             ret['yx']="[O]v"#
#             ret['y2x2']="*" #
#             return [ret]
    return []

#


# def get_r_event(events,R): #method 1 (метлод отрезков)
#     rand=random.uniform(float('0.00000001'), float(str(R)))
#     ev_number=nol0;
#     for ev in events:# возвращаем событие, на отрезке которого выпало случайное число
#         if ev['speed']==0:continue;
#         ev_number=ev_number+ev['speed']
#         if (rand<ev_number) and (rand>(ev_number-ev['speed'])):
#             print(f'rand={rand}, event={ev["speed"]}, left={ev_number-ev["speed"]}, right={ev_number}, R={R} ({type(R)})')
#             return ev

# def get_r_event(events,R): #method 2 (Линейный поиск (выбор) события)
#     Ep_minus1=nol0
#     E=decimal.Decimal(str(numpy.random.uniform()))
#     for ev in events:
#         # if ev['speed']==0:continue;
#         if (E*R>Ep_minus1) and ((E*R)<=(Ep_minus1+ev['speed'])):
#             # print(f'rand={E*R}, event={ev["speed"]}, left={Ep_minus1}, right={Ep_minus1+ev["speed"]}, R={R}')
#             # print(events)
#             return ev
#         Ep_minus1=Ep_minus1+ev['speed']

def get_r_event(events,R,first_line_events):
    Ep_minus2 = nol0
    Ep_minus1 = nol0
    E = decimal.Decimal(str(numpy.random.uniform()))
    l=random.randint(0,len(first_line_events)-1)

    for ev in first_line_events:
        # if ev['speed']==0:continue;
        if (E*R>Ep_minus2) and ((E*R)<=(Ep_minus2+ev['R_'])):
            # print(f'rand={E*R}, event={ev["speed"]}, left={Ep_minus1}, right={Ep_minus1+ev["speed"]}, R={R}')
            # print(events)
            first_line_event = ev
            break
        Ep_minus2=Ep_minus2+ev['R_']




    position_events=first_line_event['events_']
    R_=first_line_event['R_']
    for ev in position_events:
        # if ev['speed']==0:continue;
        if (E*R_>Ep_minus1) and ((E*R_)<=(Ep_minus1+ev['speed'])):
            # print(f'rand={E*R}, event={ev["speed"]}, left={Ep_minus1}, right={Ep_minus1+ev["speed"]}, R={R}')
            # print(events)
            return ev
        Ep_minus1=Ep_minus1+ev['speed']
    return False




def get_event_1(x,y,board): #получить события для одного узла
    # new_board=mcopy(board)
    ret={'speed':nol0}
    ret['y'] = y;
    ret['x'] = x;
    if board[y][x] == '*':
        ret['speed'] = k1  # Если клетка * -скорость равна k1
        ret['yx'] = "[CO]"
        return [ret]
    elif board[y][x] == '[CO]':
        ret['speed'] = k1minus  # -скорость равна k1minus
        ret['yx'] = "*"
        return [ret]
    elif board[y][x] == '[O]':
        ret['speed'] = k4  # -скорость равна k4
        ret['yx'] = "[O]v"
        return [ret]
    return []

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


def move_cell(board,t):
    #шаг 2
    # Вычисление скоростей элементарных событий. На текущий момент времени t1 и вычисление суммарной скорости R
    R=nol0;
    events=[]
    first_line_events=[]
    for i in prange(Y):
        for j in prange(X):
            value = board[i][j]
            events_,R_ = inv_1_point(i,j,board)
            # events_=[i  for i in events_ if i['speed']>0]
            events=events+events_
            R=R+R_
            if R_>0:
                first_line_events.append({'i':i, 'j':j, 'R_':R_, 'events_':events_})


    # print(events)
    #шаг 3 Случайно выбирается одно из возможных элементарных событий с вероятностью, пропорциональной его скорости.
    # Изменяется состояние решётки в соответствии с выбранным событием
    ev = get_r_event(events=events, R=R, first_line_events=first_line_events)
    # шаг 4 Вычисление шага по времени. Вычисляется момент времени t2 выхода системы
    # из текущего состояния: t2=t1-ln(E)/R, где E - случайная величина, равномерно распределённая на интервале (0,1).
    E=decimal.Decimal(str(random.random()))
    if R==0:
        print('Нет возможных событий для текущего состояния системы')
        exit()
    dt=-decimal.Decimal(str(math.log(E)))/R
    t=t+dt
    board[ev['y']][ev['x']]=ev['yx']
    if ev.get('y2x2'):
        board[ev['y2']][ev['x2']] = ev['y2x2']

    return board,t


def start_status():
    board=[['*' for i2 in prange(X)] for i in prange(Y)]
    CO=0
    O=0
    while CO < Nco:
        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        if board[y][x] == "*":
            CO = CO + 1
            board[y][x] = "[CO]"
    while (O < No) and ((O+CO)<X*Y):
        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        if board[y][x] == "*":
            O = O + 1
            board[y][x] = "[O]"
    return board

def main():
    t = nol0

    # Рисовка объектов
    st = (700 * 2) / (X + Y)

    root, canvas = create_TK(width=st * X, height=st * Y)
    root.title('Метод Монте-Карло. t=0')
    #отрисовка решетки
    build_square(canvas,st, X,Y)
    build_board(canvas, st, X,Y)

    #step 1 Заполняем начальное состояние решетки
    board=start_status()

    #отрисовка частиц в начальном состоянии и сохранение кадра визуализации
    checkers2(root, canvas, st, X, Y,board=board)
    save_as_png(canvas=canvas, fileName=f'out/00')

    i=0
    while t<=300: # Алгоритм работает до времени T, отображаем каждый 10, создаем анимацию Гиф
        # tt1=time.time()
        i=i+1
        board, t = move_cell(board=board, t=t)
# конец работы основного алгоритма ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


        # Формирование кадров демонстрационой анимации
        if i%100==0:
            # time.sleep(1)
            root.title(f'Метод Монте-Карло. t={t}, step={i}')
            checkers2(root, canvas, st, X, Y,board=board)
            # print(time.time()-tt1)
        # if i%100==0:
        #     canvas.create_text(250, 20, fill="black", font="Times 30 italic bold",
        #                        text=f"t={t}, step={i}")
        #     save_as_png(canvas=canvas, fileName=f'out/{i}')

    #Формирование файла демонстрационой анимации
    images[0].save('out/KMK_Kurkina.gif',
                   save_all=True,
                   append_images=images[1:],
                   duration=1000,
                   loop=0)

    root.mainloop()

if __name__ == '__main__':
    main()
