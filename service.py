import os
from numba import njit, prange
def mprint(m1):
    m = [[i2 for i2 in i] for i in m1]
    l=[0 for i in prange(0,len(m[0]))]
    for i in prange(0,len(m)):
        for i2 in prange(0,len(m[i])):
            m[i][i2]=str(m[i][i2])
            ll=len(m[i][i2])
            if ll>l[i2]:
                l[i2]=ll;
    for i in prange(0,len(m)):
        for i2 in prange(0,len(m[i])):
            ll = len(m[i][i2])
            if ll < l[i2]:
                a=l[i2]-ll
                m[i][i2]=m[i][i2]+' '*a
    for i in prange(0,len(m)):
        for i2 in prange(0,len(m[i])):
            print(m[i][i2], end=" | ")
        print("")

def mrange(start,end,step=1):
    if step<0:
        return [n for n in prange(start, end-1, step)]
    return [n for n in prange(start,end+1,step)]

def mcopy(matrix):
    li=len(matrix)
    lj=len(matrix[0])
    newM=[[matrix[i][i2] for i2 in prange(0, lj)] for i in prange(0, li)]
    return newM

def norma(f,h):
    sum=0
    for fn in f:
        sum=sum+fn**2
    sum=sum*h
    sum=sum**(1/2)
    return sum

def shodimost(sigma,delta_t,h):
    a_plus_c=2*sigma*delta_t/h**2
    b= 1+ 2*sigma*delta_t/h**2
    if a_plus_c<b:return True;

from PIL import Image
import ghostscript

images=[]
def save_as_png(canvas,fileName):
    global images

    # save postscipt image
    canvas.postscript(file = fileName + '.eps')
    # use PIL to convert to PNG
    img =  Image.open (fileName + '.eps')
    temp = img.copy()
    images.append(temp)
    img.close()
    os.remove(fileName + '.eps')


from tkinter import Canvas,Tk
def create_TK(width, height):
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    return root, canvas



def build_square(canvas,st, X,Y):
    y = 0
    while y < st*Y:
        x = 0
        while x < st*X:
            canvas.create_rectangle(x, y, x+st, y+st, fill='#fff', outline='#000')
            x += st

        y += st

def build_board(canvas, st, X,Y,x=False,y=False):
    fill = '#FECD72'
    outline = '#825100'
    if x and y:
        canvas.create_rectangle(x * st, y * st, x * st + st, y * st + st, fill=fill, outline=outline)


    for i in prange(0, X):
        for j in prange(0, Y):
            canvas.create_rectangle(i*st, j*st, i*st + st, j*st + st, fill=fill, outline=outline)
            # fill, outline = outline, fill

        # fill, outline = outline, fill

def checkers(root, canvas, st, X, Y,board=False):
    minor=st*0.95
    canvas.delete("all")
    build_board(canvas, st, X,Y)
    # A - белые, B - черные

    # mprint(board)
    outline = '#000'

    for i in prange(Y):
        for j in prange(X):
            value = board[i][j]
            if value == "":
                continue

            color = 'white' if value == "A" else 'black'

            x1, y1, x2, y2 = j * st+minor, i * st+minor, j * st + st-minor, i * st + st-minor
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline)
    root.update()

def checkers2(root, canvas, st, X, Y,board=False):
    all=X*Y
    CO=0
    minor=st*0.95
    canvas.delete("all")
    build_board(canvas, st, X,Y)
    # * - пустые, [O] - синие, [CO] - черные, [O]v - зеленые

    # mprint(board)
    outline = '#000'

    for i in prange(Y):
        for j in prange(X):
            value = board[i][j]
            if value == "*":
                continue

            if value=="[O]":color='blue'
            elif value=="[CO]":
                color='black';CO=CO+1
            elif value=="[O]v":color='green'

            x1, y1, x2, y2 = j * st+minor, i * st+minor, j * st + st-minor, i * st + st-minor
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline)
    print(CO/all)
    root.update()