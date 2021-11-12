from tkinter import *
import time
import random
from service import *
import math
import ghostscript

root = Tk()
root.title('Метод Монте-Карло. t=0')

#Вводные данные
X=7;Y=9;N=9
T=100; W=1; Q=0.1
t=0

#Рисовка объектов
st=88
canvas = Canvas(root, width=st*X, height=st*Y)
canvas.pack()

from PIL import Image
images=[]
def save_as_png(canvas,fileName):
    global images

    # save postscipt image
    canvas.postscript(file = fileName + '.eps')
    # use PIL to convert to PNG
    img = Image.open(fileName + '.eps')
    images.append(img)
    img.save(fileName + '.png', 'png')

from PIL import ImageGrab

def getter(widget):
    x=root.winfo_rootx()+widget.winfo_x()
    y=root.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save("1.png")

def build_square():
    y = 0
    while y < st*Y:
        x = 0
        while x < st*X:
            canvas.create_rectangle(x, y, x+st, y+st, fill='#fff', outline='#000')
            x += st

        y += st


def build_board():
    fill = '#FECD72'
    outline = '#825100'
    for i in range(0, X):
        for j in range(0, Y):
            canvas.create_rectangle(i*st, j*st, i*st + st, j*st + st, fill=fill, outline=outline)
            fill, outline = outline, fill

        fill, outline = outline, fill

def checkers(board=False):
    build_board()
    # A - белые, B - черные

    # mprint(board)
    outline = '#000'

    for i in range(Y):
        for j in range(X):
            value = board[i][j]
            if value == "":
                continue

            color = 'white' if value == "A" else 'black'

            x1, y1, x2, y2 = j * st+10, i * st+10, j * st + st-10, i * st + st-10
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline)
    root.update()




def get_step(x,y,dx,dy,board): # Исследование 1 варианта развития событий
    ret={}
    x2=x+dx
    y2=y+dy
    if x2==X:x2=0;
    if y2==Y:y2=0;
    if x2<0:x2=X-1;
    if y2<0:y2=Y-1;
    ret['x']=x;ret['y']=y;ret['x2']=x2;ret['y2']=y2
    if board[y][x]=='B':
        if board[y2][x2]=='':
            ret['speed']=W  # Если клетка свободна -скорость равна W
            ret['c2']="B" # на новом месте - В
        else: ret['speed']=0 #Частицы типа A и B, B и B не реагируют (скорость перехода равна 0).
    if board[y][x] == 'A':
        if board[y2][x2]=='':
            ret['speed']=W  # Если клетка свободна -скорость равна W
            ret['c2'] = "A" # A перемещается
        if board[y2][x2]=='B':
            ret['speed']=0  # Частицы типа A и B не реагируют (скорость перехода равна 0)
        if board[y2][x2]=='A':
            ret['speed']=Q  # . Если клетка занята частицей типа A - то скорость равна Q
            ret['c2'] = "B" # На новом месте будет В
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

def move_cell(board,t):
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
                left=get_step(x=j,y=i,dx=-1,dy=0,board=board)
                right=get_step(x=j,y=i,dx=+1,dy=0,board=board)
                up=get_step(x=j,y=i,dx=0,dy=-1,board=board)
                down=get_step(x=j,y=i,dx=0,dy=+1,board=board)
                R=R+left['speed']+right['speed']+up['speed']+down['speed']
                events.append(left)
                events.append(right)
                events.append(up)
                events.append(down)



    #шаг 3 Случайно выбирается одно из возможных элементарных событий с вероятностью, пропорциональной его скорости.
    # Изменяется состояние решётки в соответствии с выбранным событием
    ev = get_r_event(events=events, R=R)
    board[ev['y']][ev['x']]=""
    board[ev['y2']][ev['x2']]=ev['c2']
    # time.sleep(0.01)

    # шаг 4 Вычисление шага по времени. Вычисляется момент времени t2 выхода системы
    # из текущего состояния: t2=t1-ln(E)/R, где E - случайная величина, равномерно распределённая на интервале (0,1).
    E=random.random()
    t=t-math.log(E)/R
    return board,t

#отрисовка решетки
build_square()
build_board()

#step 1 Заполняем начальное состояние решетки
board=[['' for i2 in range(X)] for i in range(Y)]
i=0
while i < N:
    x=random.randint(0, X-1)
    y=random.randint(0, Y-1)
    if board[y][x]=="":
        i=i+1
        board[y][x]="A"
#отрисовка частиц
checkers(board=board)
save_as_png(canvas=canvas, fileName=f'out/00')

for i in mrange(1,T): # Проходим Т шагов, отображаем каждый 10, создаем анимацию Гиф
    board, t = move_cell(board=board, t=t)
    root.title(f'Метод Монте-Карло. t={t}, step={i}')
    checkers(board=board)
    if i%1==0:
        canvas.create_text(250, 20, fill="black", font="Times 30 italic bold",
                           text=f"t={t}, step={i}")
        save_as_png(canvas=canvas, fileName=f'out/{i}')

images[0].save('out/monte_Carlo1.gif',
               save_all=True,
               append_images=images[1:],
               duration=1000,
               loop=0)
root.mainloop()
