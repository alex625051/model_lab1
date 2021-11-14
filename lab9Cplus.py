from numba import njit, prange
import math
import random
import os
from service import mprint
clear = lambda: os.system('cls')
from numba.typed import List
from numba.typed import Dict
from numba.core import types
from numba import int16, int32
import numba

X = 20;
Y = 20;
T = 300;
Nco=X*Y*1.0
No=X*Y*0.0
Pco=0.3000;k1_=10000.0000;k1=Pco*k1_;
k1minus=300.0000
k2=2500.0000
k3=25000.0000
k4=0.1100
k5=0.0065
k6=100000.0000
k7=k6
k8=k6
R = 0; # глобальная переменная с R
FetaCO=[]


@njit( types.DictType(types.unicode_type,types.float64)(int16, int16, int16,int16,numba.typed.typedlist.List[:]))
def get_event_2x4(x,y,dx,dy,board): # Исследование 1 варианта развития событий при 2 узлах на 4 стороны
    # The Dict.empty() constructs a typed dictionary.
    # The key and value typed must be explicitly declared.
    ret = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.float64,
    )
    ret['speed']=0
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
    ret['found']=True

    if board[y][x]==1:
        if board[y2][x2]==2:
            ret['speed']=25000  #
            ret['yx']=0#
            ret['y2x2']=0 #
            return ret
        elif board[y2][x2]=='3':
            ret['speed']=0.0065  #
            ret['yx']=0 #
            ret['y2x2']=0 #
            return ret
        elif board[y2][x2]==0:
            ret['speed']=k6  #
            ret['yx']=0 #
            ret['y2x2']=1 #
            return ret

    elif board[y][x]==2:
        if board[y2][x2]==0:
            ret['speed']=k7  #
            ret['yx']=0 #
            ret['y2x2']=2 #
            return ret

    elif board[y][x]==3:
        if board[y2][x2]==0:
            ret['speed']=k8  #
            ret['yx']=0 #
            ret['y2x2']=3 #
            return ret


    ret['found']=False
    return ret

def get_event_1(x,y,board): #получить события для одного узла
    # new_board=mcopy(board)
    ret={'speed':0}
    ret['found']=True

    ret['y'] = y;
    ret['x'] = x;
    if board[y][x] == 0:
        ret['speed'] = k1  # Если клетка * -скорость равна k1
        ret['yx'] = 1
        return ret
    elif board[y][x] == 1:
        ret['speed'] = k1minus  # -скорость равна k1minus
        ret['yx'] = 0
        return ret
    elif board[y][x] == 2:
        ret['speed'] = k4  # -скорость равна k4
        ret['yx'] = 3
        return ret

    ret['found']=False
    return ret

def get_event_2x2(x, y, dx, dy, board):  # Исследование 1 варианта развития событий при 2 узлах в 2 стороны

    # new_board = mcopy(board)
    ret = {'speed': 0}
    ret['found']=True

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

    if board[y][x] == 0:
        if board[y2][x2] == 0:
            ret['speed'] = k2  #
            ret['yx'] = 2  #
            ret['y2x2'] = 2  #
            return ret

    ret['found']=False
    return ret

def inv_1_point(i,j,board0):
    R_=0;
    events=[]
    board = List()
    for i in board0:
        l = List()
        for i2 in i:
            l.append(i2)
        board.append(l)




    left = get_event_2x4(x=j, y=i, dx=-1, dy=0, board=board)
    right = get_event_2x4(x=j, y=i, dx=+1, dy=0, board=board)
    up = get_event_2x4(x=j, y=i, dx=0, dy=-1, board=board)
    down = get_event_2x4(x=j, y=i, dx=0, dy=+1, board=board)

    # # узлы одинаковые - необходимо только 1 раз учитывать
    down2 = get_event_2x2(x=j, y=i, dx=0, dy=+1, board=board)
    right2 = get_event_2x2(x=j, y=i, dx=+1, dy=0, board=board)
    #
    # # смотрим сам узел
    this_point = get_event_1(x=j, y=i, board=board)

    R_=R_+left['speed']
    R_=R_+right['speed']
    R_=R_+up['speed']
    R_=R_+down['speed']

    R_ = R_ + down2['speed']
    R_ = R_ + right2['speed']
    R_=R_+this_point['speed']


    # добавляем события. будут и с 0 вероятностью

    if left['found']:events.append(left)
    if right['found']:events.append(right)
    if up['found']:events.append(up)
    if down['found']:events.append(down)
    if down2['found']:events.append(down2)
    if right2['found']:events.append(right2)
    if this_point['found']:events.append(this_point)
    return events, R_


def get_r_event(events,R): #method 2 (Линейный поиск (выбор) события)
    Ep_minus1=0
    E=random.random()
    for ev in events:
        # if ev['speed']==0:continue;
        if (E*R>Ep_minus1) and ((E*R)<=(Ep_minus1+ev['speed'])):
            # print(f'rand={E*R}, event={ev["speed"]}, left={Ep_minus1}, right={Ep_minus1+ev["speed"]}, R={R}')
            # print(events)
            return ev
        Ep_minus1=Ep_minus1+ev['speed']


def move_cell(board,t):
    R=0
    events=[]

    for i in prange(Y):
        for j in prange(X):
            events_,R_ = inv_1_point(i,j,board)
            events=events+events_
            R=R+R_

    ev = get_r_event(events=events,R=R)

    E=random.random()
    if R==0:
        print('Нет возможных событий для текущего состояния системы')
        exit()
    dt=math.log(1/E)/R
    t=t+dt
    board[ev['y']][ev['x']]=ev['yx']


    if ev.get('y2x2'):
        board[ev['y2']][ev['x2']] = ev['y2x2']


    return board,t


def main():
    board = [[0 for i2 in prange(X)] for i in prange(Y)]
    t = 0
    step=0

    #step 1 Заполняем начальное состояние решетки
    # board=start_status()


    while t<=300: # Алгоритм работает до времени T, отображаем каждый 10, создаем анимацию Гиф
        # tt1=time.time()
        step=step+1
        board, t = move_cell(board=board, t=t)
        if step%10000==0:
            print(t)
            mprint(board)
            print('--------------------------------------------------------------------')
# конец работы основного алгоритма ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

if __name__ == '__main__':
    main()