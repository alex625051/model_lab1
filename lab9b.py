from tkinter import *
import time
import random
from service import *
import math
import ghostscript

# Вводные данные
X = 20;
Y = 20;
T = 300;
Pco=0.3;k1_=10**4;k1=Pco*k1_;
k1minus=3*(10**2)
k2=2.5*(10**3)
k3=2.5*(10**4)
k4=0.11
k5=6.5*(10**(-3))
k6=10**5
k7=k6
k8=k6


def get_event_2x2(x, y, dx, dy, board):  # Исследование 1 варианта развития событий при 2 узлах на 2 стороны
    new_board = mcopy(board)
    ret = {'speed': 0}
    x2 = x + dx
    y2 = y + dy
    if x2 == X:
        x2 = 0;
    elif y2 == Y:
        y2 = 0;

    if new_board[y][x] == '*':
        if new_board[y2][x2] == '*':
            ret['speed'] = k2  #
            new_board[y][x] = "[O]"  #
            new_board[y2][x2] = "[O]"  #

    ret['board'] = mcopy(new_board)
    return ret


def get_event_2x4(x,y,dx,dy,board): # Исследование 1 варианта развития событий при 2 узлах на 4 стороны
    new_board=mcopy(board)
    ret={'speed':0}
    x2=x+dx
    y2=y+dy
    if x2==X:x2=0;
    elif y2==Y:y2=0;
    elif x2<0:x2=X-1;
    elif y2<0:y2=Y-1;
    if new_board[y][x]=='[CO]':
        if new_board[y2][x2]=='[O]':
            ret['speed']=k3  #
            new_board[y][x]="*" #
            new_board[y2][x2]="*" #
        elif new_board[y2][x2]=='[O]v':
            ret['speed']=k5  #
            new_board[y][x]="*" #
            new_board[y2][x2]="*" #
        elif new_board[y2][x2]=='*':
            ret['speed']=k6  #
            new_board[y][x]="*" #
            new_board[y2][x2]="[CO]" #

    elif new_board[y][x]=='[O]':
        if new_board[y2][x2]=='*':
            ret['speed']=k7  #
            new_board[y][x]="*" #
            new_board[y2][x2]="[O]" #

    elif new_board[y][x]=='[O]v':
        if new_board[y2][x2]=='*':
            ret['speed']=k8  #
            new_board[y][x]="*" #
            new_board[y2][x2]="[O]v" #

    ret['board']=mcopy(new_board)
    return ret


def get_r_event(events,R): #method 2 (Линейный поиск (выбор) события)
    Ep_minus1=0
    E=random.random()
    for ev in events:
        if ev['speed']==0:continue;
        if (E*R>Ep_minus1) and ((E*R)<=(Ep_minus1+ev['speed'])):
            return ev
        Ep_minus1=Ep_minus1+ev['speed']

def get_event_1(x,y,board): #получить события для одного узла
    new_board=mcopy(board)
    ret={'speed':0}
    if new_board[y][x] == '*':
        ret['speed'] = k1  # Если клетка * -скорость равна k1
        new_board[y][x] = "[CO]"
    elif new_board[y][x] == '[CO]':
        ret['speed'] = k1minus  # -скорость равна k1minus
        new_board[y][x] = "*"
    elif new_board[y][x] == '[O]':
        ret['speed'] = k4  # -скорость равна k4
        new_board[y][x] = "[O]v"
    ret['board']=mcopy(new_board)
    return ret


def move_cell(board,t):
    #шаг 2
    # Вычисление скоростей элементарных событий. На текущий момент времени t1 и вычисление суммарной скорости R
    R=0;
    events=[]
    for i in range(Y):
        for j in range(X):
            value = board[i][j]

             #генерация скоростей для 4 направлений, добавлених в список событий и подсчет R
            # проверяем на все 4 направления=> обратные реакции учитываются, когда относительно следующей точки происходит проверка
            left=get_event_2x4(x=j,y=i,dx=-1,dy=0,board=board)
            right=get_event_2x4(x=j,y=i,dx=+1,dy=0,board=board)
            up=get_event_2x4(x=j,y=i,dx=0,dy=-1,board=board)
            down=get_event_2x4(x=j,y=i,dx=0,dy=+1,board=board)

            #узлы одинаковые - необходимо только 1 раз учитывать
            down2=get_event_2x2(x=j,y=i,dx=0,dy=+1,board=board)
            right2=get_event_2x2(x=j,y=i,dx=+1,dy=0,board=board)

            #смотрим сам узел
            this_point=get_event_1(x=j,y=i,board=board)

            R=R+left['speed']+right['speed']+right2['speed']+up['speed']+down['speed']+down2['speed']+this_point['speed']

            #добавляем события. будут и с 0 вероятностью
            events.append(left)
            events.append(right)
            events.append(up)
            events.append(down)
            events.append(down2)
            events.append(right2)
            events.append(this_point)



    #шаг 3 Случайно выбирается одно из возможных элементарных событий с вероятностью, пропорциональной его скорости.
    # Изменяется состояние решётки в соответствии с выбранным событием
    ev = get_r_event(events=events, R=R)
    print(ev['speed'])
    # board[ev['y']][ev['x']]=""
    # board[ev['y2']][ev['x2']]=ev['c2']
    # time.sleep(0.01)

    # шаг 4 Вычисление шага по времени. Вычисляется момент времени t2 выхода системы
    # из текущего состояния: t2=t1-ln(E)/R, где E - случайная величина, равномерно распределённая на интервале (0,1).
    E=random.random()
    t=t-math.log(E)/R
    # mprint(ev['board'])
    return mcopy(ev['board']),t


def start_status():
    board=[['*' for i2 in range(X)] for i in range(Y)]
    return board

def main():
    t = 0

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
    while t<=T: # Алгоритм работает до времени T, отображаем каждый 10, создаем анимацию Гиф
        i=i+1
        board, t = move_cell(board=board, t=t)
# конец работы основного алгоритма ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # Формирование кадров демонстрационой анимации
        root.title(f'Метод Монте-Карло. t={t}, step={i}')
        checkers2(root, canvas, st, X, Y,board=board)
        if i%100==0:
            canvas.create_text(250, 20, fill="black", font="Times 30 italic bold",
                               text=f"t={t}, step={i}")
            save_as_png(canvas=canvas, fileName=f'out/{i}')

    #Формирование файла демонстрационой анимации
    images[0].save('out/KMK_Kurkina.gif',
                   save_all=True,
                   append_images=images[1:],
                   duration=1000,
                   loop=0)

    root.mainloop()

if __name__ == '__main__':
    main()
