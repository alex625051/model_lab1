import io
from tkinter import *
import datetime
import random
from matplotlib.ticker import FuncFormatter
from service import *
import math
from numba import njit, prange
import decimal
import numpy
import pandas as pd
import json
import matplotlib.pyplot as plt
from PIL import Image
import ghostscript
import moviepy.editor as mp




continuedVer = '2.01_01'  # Номер набора начальных условий и настроек

# Техические вводные данные модели
nol0 = decimal.Decimal('0')  # Ноль типа Decimal
continued = False  # Возобновляемый режим для распределенных вычислений
saveGif=True;
showVisualDelay = 1000;  # Пропуск шагов для следующего этапа визуализации
unlimetedSteps = True;  # Вычислять до полного перебора всех доступных вероятностей перехода состояния модели
unlimetedLimits = False;  # Бесконечная решетка разрешена
averBoardHLimit = True;  # окружаем рабочую область граничными ячейками с "H"
startIcellsFromCenter = True;  # Заполняем начальное состояние решетки вокруг с геометрическогоцентра
t0 = decimal.Decimal('5')  # Начальное время
xlimits = [0, 60 * 24 * 3]  # Лимиты оси X визуализации
T = 300;  # Предельное количество шагов (при unlimetedSteps = False)
visibable=False;

# Вводные данные
X = 300;
Y = 300;
N_I = X * Y * 0.10  # Начальное количество I-ячеек для заполнения (общее количество ячеек умноженное на долю I)
N_D = X * Y * 0.000
N_F = X * Y * 0.0
k1 = decimal.Decimal('0') / 90;  # H->I
k1minus = decimal.Decimal('0') / 90;  # I->H
k2 = decimal.Decimal('1.2') / 360;  # I->D
k4 = decimal.Decimal('0.0')  # I->F
k4minus = decimal.Decimal('0.0')  # F->I
k5 = decimal.Decimal('0.0')  # F->H
k7 = decimal.Decimal('8') / 90;  # IH->HH
k8 = decimal.Decimal('4') / 90;  # HI->II
k9 = decimal.Decimal('8') / 90  # HD->ID
k10 = decimal.Decimal('1.2') / 360  # ID->DD
k11 = decimal.Decimal('1.2') / 360  # II->DI

# Глобальные переменные реализации модели
R = nol0;  # глобальная переменная с R
FetaD_array = []
speeds_dict = {}
images=[]
for i in prange(Y):
    for j in prange(X):
        speeds_dict[f'{i}_{j}'] = {'i': i, 'j': j}


# сохранения кадра визуализации
def save_as_png(canvas):
    global images

    # save postscript image
    canvasImage=canvas.postscript(colormode='color')

    # use PIL to convert to PNG
    img = Image.open(io.BytesIO(canvasImage.encode('utf-8')))
    images.append(img)
    # img.save(fileName + '.png', 'png')


# Заполнение ячеек для начального состояния решетки модели
def start_status():
    board = [['H' for i2 in prange(X)] for i in prange(Y)]
    I = 0
    D = 0
    F = 0
    if startIcellsFromCenter:
        xCenter = X / 2
        yCenter = Y / 2
        radius = math.sqrt(N_I / math.pi)
        pointsInRadius = list()
        for x in range(0, X):
            for y in range(0, Y):
                if math.sqrt((x - xCenter) ** 2 + (y - yCenter) ** 2) < radius:
                    pointsInRadius.append({"x": x, "y": y})
    while I < N_I:
        if startIcellsFromCenter:
            if not len(pointsInRadius):
                break
            onePoint = pointsInRadius.pop()
            x = onePoint['x'];
            y = onePoint['y'];
        else:
            x = random.randint(0, X - 1)
            y = random.randint(0, Y - 1)
        if board[y][x] == "H":
            I = I + 1
            board[y][x] = "I"
    while (D < N_D) and ((I + D) < X * Y):

        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        if board[y][x] == "H":
            D = D + 1
            board[y][x] = "D"
    while (F < N_F) and ((I + D + F) < X * Y):
        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        if board[y][x] == "H":
            F = F + 1
            board[y][x] = "F"
    return board


# граничные условия для 2х2
def get_event_2x2_limits(x, y, dx, dy):
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
        # Граничные условия
        if x2 == X:
            x2 = False;
        elif y2 == Y:
            y2 = False;
        return x, y, dx, dy, x2, y2


# Исследование 1 варианта развития событий при 2 узлах в 2 стороны
def get_event_2x2(x, y, dx, dy, board):
    ret = {'speed': nol0}
    x, y, dx, dy, x2, y2 = get_event_2x2_limits(x, y, dx, dy)
    ret['y'] = y;
    ret['x'] = x;
    if y2 and x2:
        secondCell = board[y2][x2]
        ret['y2'] = y2;
        ret['x2'] = x2;
    else:
        if averBoardHLimit:
            secondCell = "H"
        else:
            return []
    if board[y][x] == 'I':
        if secondCell == 'I':
            ret['speed'] = k11  #
            ret['yx'] = "D"  #
            if y2 and x2:
                ret['y2x2'] = "I"  #
            return [ret]
    return []


# граничные условия для 2х4
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


# Исследование 1 варианта развития событий при 2 узлах на 4 стороны
def get_event_2x4(x, y, dx, dy, board):
    ret = {'speed': nol0}
    x, y, dx, dy, x2, y2 = get_event_2x4_limits(x, y, dx, dy)
    ret['y'] = y;
    ret['x'] = x;
    if y2 and x2:
        secondCell = board[y2][x2]
        ret['y2'] = y2;
        ret['x2'] = x2;
    else:
        if averBoardHLimit:
            secondCell = "H"
        else:
            return []
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


# Вычисление R
def get_r_event(R):
    Ep_minus1 = nol0
    E = decimal.Decimal(str(numpy.random.uniform()))

    for key in speeds_dict:
        if speeds_dict[key]['R_'] == 0: continue
        position_events = speeds_dict[key]['events_']
        for ev in position_events:
            ER = E * R
            if (ER > Ep_minus1) and ((ER) <= (Ep_minus1 + ev['speed'])):
                return ev
            Ep_minus1 = Ep_minus1 + ev['speed']
    return False

# Вычисление R с ускорением
def get_r_event2(R):
    E = decimal.Decimal(str(numpy.random.uniform()))
    ER = E * R
    def get_r_event_from_speeds_dict_R():
        Ep_minus1 = nol0
        for key in speeds_dict:
            R_= speeds_dict[key]['R_']
            if R_ == 0: continue
            if (ER > Ep_minus1) and (ER <= (Ep_minus1 + R_)):
                return Ep_minus1, key
            Ep_minus1 = Ep_minus1 + R_
        return False,False

    Ep_minus1, speeds_dict_key=get_r_event_from_speeds_dict_R()
    if not speeds_dict_key: return False
    position_events = speeds_dict[speeds_dict_key]['events_']
    for ev in position_events:
        if (ER > Ep_minus1) and (ER <= (Ep_minus1 + ev['speed'])):
            return ev
        Ep_minus1 = Ep_minus1 + ev['speed']
    return False

# получить все возможные события для одного узла решетки
def get_event_1(x, y, board):
    ret = []
    if board[y][x] == 'H':
        ret.append({"yx": "I", "speed": k1, "x": x, "y": y});

    elif board[y][x] == 'I':
        ret.append({"yx": "H", "speed": k1minus, "x": x, "y": y})
        ret.append({"yx": "D", "speed": k2, "x": x, "y": y})
        ret.append({"yx": "F", "speed": k4, "x": x, "y": y});

    elif board[y][x] == 'F':
        ret.append({"yx": "H", "speed": k5, "x": x, "y": y});
        ret.append({"yx": "I", "speed": k4minus, "x": x, "y": y});
    return ret


def inv_1_point(i, j, board):
    R_ = nol0;
    events = []
    # генерация скоростей для 4 направлений, добавлених в список событий и подсчет R
    # проверяем на все 4 направления=> обратные реакции учитываются, когда относительно следующей точки происходит проверка
    left = get_event_2x4(x=j, y=i, dx=-1, dy=0, board=board)
    right = get_event_2x4(x=j, y=i, dx=+1, dy=0, board=board)
    up = get_event_2x4(x=j, y=i, dx=0, dy=-1, board=board)
    down = get_event_2x4(x=j, y=i, dx=0, dy=+1, board=board)

    # узлы одинаковые - необходимо только 1 раз учитывать
    down2 = get_event_2x2(x=j, y=i, dx=0, dy=+1, board=board)
    right2 = get_event_2x2(x=j, y=i, dx=+1, dy=0, board=board)

    # узел вне связи с соседними
    this_point = get_event_1(x=j, y=i, board=board)

    for i in left: R_ = R_ + i['speed']
    for i in right: R_ = R_ + i['speed']
    for i in right2: R_ = R_ + i['speed']
    for i in up: R_ = R_ + i['speed']
    for i in down: R_ = R_ + i['speed']
    for i in down2: R_ = R_ + i['speed']
    for i in this_point: R_ = R_ + i['speed']

    # добавляем события
    events = events + left
    events = events + right
    events = events + up
    events = events + down
    events = events + down2
    events = events + right2
    events = events + this_point
    return events, R_


# перевод решетки в новое состояние
def change_board(board, t, changed_points):
    global speeds_dict
    global R
    # шаг 2
    # Вычисление скоростей элементарных событий. На текущий момент времени t1 и вычисление суммарной скорости R

    # Ускорение алгоритма - работа только с измененными ячейками решетки и их окружением
    if changed_points:
        for point in changed_points:
            i = point['y']
            j = point['x']
            events_, R_ = inv_1_point(i, j, board)
            R = R - speeds_dict[f'{i}_{j}']['R_']
            speeds_dict[f'{i}_{j}']['R_'] = R_;
            speeds_dict[f'{i}_{j}']['events_'] = events_;

            R = R + speeds_dict[f'{i}_{j}']['R_']

    if not changed_points:
        for i in prange(Y):
            for j in prange(X):
                events_, R_ = inv_1_point(i, j, board)
                R = R + R_
                speeds_dict[f'{i}_{j}']['R_'] = R_;
                speeds_dict[f'{i}_{j}']['events_'] = events_;

    # шаг 3 Случайно выбирается одно из возможных элементарных событий с вероятностью, пропорциональной его скорости.
    # Изменяется состояние решётки в соответствии с выбранным событием
    ev = get_r_event2(R=R)
    # шаг 4 Вычисление шага по времени. Вычисляется момент времени t2 выхода системы
    # из текущего состояния: t2=t1-ln(E)/R, где E - случайная величина, равномерно распределённая на интервале (0,1).
    E = decimal.Decimal(str(random.random()))

    # Если нет доступных состояний решетки для изменения - значит алгоритм заканчивает работу
    if R == 0:
        return False
    dt = decimal.Decimal(str(math.log(1 / E))) / R
    t = t + dt
    try:
        board[ev['y']][ev['x']] = ev['yx']
    except:
        return False

    def get_near_points(x, y):
        x1 = x + 1
        y1 = y + 0
        x2 = x - 1
        y2 = y + 0
        x3 = x + 0
        y3 = y + 1
        x4 = x + 0
        y4 = y - 1
        if x1 == X: x1 = 0
        if x2 < 0: x2 = X - 1
        if y3 == Y: y3 = 0;
        if y4 < 0: y4 = Y - 1
        return [{'x': x1, 'y': y1}, {'x': x2, 'y': y2}, {'x': x3, 'y': y3}, {'x': x4, 'y': y4}]

    def get_changed_points(ev):
        points = []
        points = points + get_near_points(x=ev['x'], y=ev['y'])
        if ev.get('y2x2'):
            points = points + get_near_points(x=ev['x2'], y=ev['y2'])
        else:
            points = points + [{'x': ev['x'], 'y': ev['y']}]
        return points

    if ev.get('y2x2'):
        board[ev['y2']][ev['x2']] = ev['y2x2']

    changed_points = get_changed_points(ev)

    return board, t, changed_points


# Визуализация на графике по окончании рабготы программы и запись на хранилище данных
def showGraph(FetaD_array,filename_suffix=""):
    def prepareConfigsToSave():
        configs = {"saveGif":saveGif,"continued": continued, "showVisualDelay": showVisualDelay, "unlimetedSteps": unlimetedSteps,
                   "unlimetedLimits": unlimetedLimits, "averBoardHLimit": averBoardHLimit,
                   "startIcellsFromCenter": startIcellsFromCenter, "t0": t0, "continuedVer": continuedVer,
                   "xlimits": xlimits, "X": X, "Y": Y, "T": T, "N_I": N_I, "N_D": N_D, "N_F": N_F, "k1": k1,
                   "k1minus": k1minus, "k2": k2, "k4": k4, "k4minus": k4minus, "k5": k5, "k7": k7, "k8": k8, "k9": k9,
                   "k10": k10, "k11": k11}
        for key in configs:
            if isinstance(configs[key], decimal.Decimal):
                configs[key] = float(configs[key])

        return json.dumps(configs)

    def formatOx(x, pos):
        delta = datetime.timedelta(minutes=float(x))
        deltaStr = str(delta).replace(" days, ", 'd')
        return deltaStr

    dF = pd.DataFrame(FetaD_array)
    with open(f'out/FetaD_array_{continuedVer}{filename_suffix}.csv', 'w') as ff:
        ff.write(prepareConfigsToSave() + '\n')
    dF.to_csv(f'out/FetaD_array_{continuedVer}{filename_suffix}.csv', index=False, mode='a')
    fig = plt.figure(figsize=(18, 6), dpi=200)
    yD = dF['fetaD'].tolist()
    yF = dF['fetaF'].tolist()
    yI = dF['fetaI'].tolist()
    yH = dF['fetaH'].tolist()
    yID = (dF['fetaI'] + dF['fetaD']).tolist()
    x = dF['t'].tolist()

    ax = fig.add_subplot(111)
    ax.plot(x, yD, color="black", label='D')
    ax.plot(x, yI, color="red", label='I')
    ax.plot(x, yH, color="blue", label='H')
    ax.plot(x, yF, color="green", label='F')
    ax.plot(x, yID, '.', color="orange", label='I+D')
    ax.grid()
    ax.set_title(f"t(0)={t0}, N={X}x{Y}, I(0)={N_I / (X * Y)} ")
    ax.set_xlabel("t", fontsize=9, color='blue')
    ax.set_ylabel("", fontsize=9, color='orange')
    ax.legend()
    ax.set_xlim(xlimits)

    ax.xaxis.set_major_formatter(FuncFormatter(formatOx))

    fig.show()
    fig.savefig(f'out/fetas_array_{continuedVer}{filename_suffix}.png')
    print(dF)


def tToint(t):
    delta = datetime.timedelta(minutes=float(t))
    ret = f"t={int(t)}min ({delta})"
    return ret


def pauseUI(root):
    pause_var2 = StringVar()
    root.bind('<Button-1>', lambda e: pause_var2.set(1))
    root.wait_variable(pause_var2)
    pause_var2.set(0)
    root.bind('<Button-1>', lambda e: pauseUI(root))


def main():
    global speeds_dict
    t = t0
    step = 0
    changed_points = []
    # Начальная прорисовка объектов визуализации
    st = (700 * 2) / (X + Y)

    root, canvas = create_TK(width=st * X, height=st * Y)

    def on_closing():
        root.event_generate("<Key>")
        showGraph(FetaD_array, filename_suffix="_interact")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title('Метод Монте-Карло. t=0')

    # отрисовка решетки
    build_square(canvas, st, X, Y)
    build_board(canvas, st, X, Y)

    # step 1 Заполняем начальное состояние решетки
    board = start_status()

    # отрисовка частиц в начальном состоянии и сохранение кадра визуализации
    fetas = checkers4(root, canvas, st, X, Y, board=board, visibable=visibable)
    fetas['t'] = t
    FetaD_array.append(fetas)
    root.title(f'Метод Монте-Карло. t={tToint(t)}, step={step}')
    root.bind('<Button-1>', lambda e: pauseUI(root))

    while unlimetedSteps or t <= 300:  # Алгоритм работает до времени T, отображаем каждый 10, создаем анимацию Гиф
        # tt1=time.time()
        step = step + 1
        try:
            board, t, changed_points = change_board(board=board, t=t, changed_points=changed_points)
        except:
            if saveGif:
                print('saving gif')
                images[0].save(f'out2/{continuedVer}_board.gif',
                               save_all=True,
                               append_images=images[1:],
                               duration=1000,
                               loop=0)
                clip = mp.VideoFileClip(filename=f'out2/{continuedVer}_board.gif',audio=False, target_resolution=(1000,1000) )
                print('saving mp4')
                clip.write_videofile(f'out2/{continuedVer}_board.mp4')
            print("Нет возможных событий для текущего состояния системы.\n Нажмите любую клавишу")
            pause_var = StringVar()
            root.bind('<Key>', lambda e: pause_var.set(1))
            showGraph(FetaD_array)
            root.wait_variable(pause_var)
            exit()

        # конец работы основного алгоритма ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # Прорисовка визуализации
        if step % showVisualDelay == 0:
            root.title(f'Метод Монте-Карло. t={tToint(t)} мин, step={step}')
            fetas = checkers4(root, canvas, st, X, Y, board=board, visibable=visibable)
            fetas['t'] = t
            FetaD_array.append(fetas)

            if saveGif:
                save_as_png(canvas=canvas)

    root.mainloop()


if __name__ == '__main__':
    main()
