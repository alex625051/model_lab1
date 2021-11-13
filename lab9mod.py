from tkinter import *
import time
import random
from service import *
import math
import ghostscript

# Вводные данные
X = 20;
Y = 20;
N = 9
T = 100;
W = 1.0;
Q = 0.1

def get_step(X, Y, x,y,dx,dy,board): # Исследование 1 варианта развития событий
    new_board=mcopy(board)
    ret={}
    x2=x+dx
    y2=y+dy
    if x2==X:x2=0;
    elif y2==Y:y2=0;
    elif x2<0:x2=X-1;
    elif y2<0:y2=Y-1;
    # ret['x']=x;ret['y']=y;ret['x2']=x2;ret['y2']=y2
    if new_board[y][x]=='B':
        if new_board[y2][x2]=='':
            ret['speed']=W  # Если клетка свободна -скорость равна W
            new_board[y][x]="" # на cтаром месте - пусто теперь
            new_board[y2][x2]="B" # на новом месте - В
        else: ret['speed']=0 #Частицы типа A и B, B и B не реагируют (скорость перехода равна 0).
    elif new_board[y][x] == 'A':
        if new_board[y2][x2]=='':
            ret['speed']=W  # Если клетка свободна -скорость равна W
            new_board[y][x] = "" # A на старом месте убираем
            new_board[y2][x2] = "A" # A перемещается
        elif new_board[y2][x2]=='B':
            ret['speed']=0  # Частицы типа A и B не реагируют (скорость перехода равна 0)
        elif new_board[y2][x2]=='A':
            ret['speed']=Q  # . Если клетка занята частицей типа A - то скорость равна Q
            new_board[y][x] = "" # На старом месте теперь пусто
            new_board[y2][x2] = "B" # На новом месте будет В
    ret['board']=mcopy(new_board)
    return ret


# def get_r_event(events,R): #method 1 (метлод отрезков)
#     rand=random.uniform(0.000001, R)
#     ev_number=0;
#     for ev in events:# возвращаем событие, на отрезке которого выпало случайное число
#         if ev['speed']==0:continue;
#         ev_number=ev_number+ev['speed']
#         if (rand<ev_number) and (rand>(ev_number-ev['speed'])):
#             print(f'rand={rand}, event={ev["speed"]}, left={ev_number-ev["speed"]}, right={ev_number}, R={R}')
#             return ev

def get_r_event(events,R): #method 2 (Линейный поиск (выбор) события)
    Ep_minus1=0
    E=random.random()
    for ev in events:
        if ev['speed']==0:continue;
        if (E*R>Ep_minus1) and ((E*R)<=(Ep_minus1+ev['speed'])):
            return ev
        Ep_minus1=Ep_minus1+ev['speed']

def move_cell(X,Y,board,t):
    #шаг 2
    # Вычисление скоростей элементарных событий. На текущий момент времени t1 и вычисление суммарной скорости R
    R=0;
    events=[]
    for i in range(Y):
        for j in range(X):
            value = board[i][j]
            if value == "": #Если клетка пустая - никаких событий не генерирует
                continue
            else: #генерация скоростей для 4 направлений, добавлених в список событий и подсчет R
                left=get_step(X=X,Y=Y,x=j,y=i,dx=-1,dy=0,board=board)
                right=get_step(X=X,Y=Y,x=j,y=i,dx=+1,dy=0,board=board)
                up=get_step(X=X,Y=Y,x=j,y=i,dx=0,dy=-1,board=board)
                down=get_step(X=X,Y=Y,x=j,y=i,dx=0,dy=+1,board=board)
                R=R+left['speed']+right['speed']+up['speed']+down['speed']
                events.append(left)
                events.append(right)
                events.append(up)
                events.append(down)



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
    mprint(ev['board'])
    return mcopy(ev['board']),t


def start_status():
    board=[['' for i2 in range(X)] for i in range(Y)]
    i=0
    while i < N:
        x=random.randint(0, X-1)
        y=random.randint(0, Y-1)
        if board[y][x]=="":
            i=i+1
            board[y][x]="A"
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
    checkers(root, canvas, st, X, Y,board=board)
    save_as_png(canvas=canvas, fileName=f'out/00')

    for i in mrange(1,T): # Проходим Т шагов, отображаем каждый 10, создаем анимацию Гиф
        board, t = move_cell(X=X, Y=Y,board=board, t=t)
# конец работы основного алгоритма ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # Формирование кадров демонстрационой анимации
        root.title(f'Метод Монте-Карло. t={t}, step={i}')
        checkers(root, canvas, st, X, Y,board=board)
        if i%100==0:
            canvas.create_text(250, 20, fill="black", font="Times 30 italic bold",
                               text=f"t={t}, step={i}")
            save_as_png(canvas=canvas, fileName=f'out/{i}')

    #Формирование файла демонстрационой анимации
    images[0].save('out/monte_Carlo1.gif',
                   save_all=True,
                   append_images=images[1:],
                   duration=1000,
                   loop=0)

    root.mainloop()

if __name__ == '__main__':
    main()
