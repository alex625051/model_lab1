import os
import json
import decimal
def mprint(m1):
    m = [[i2 for i2 in i] for i in m1]
    l=[0 for i in range(0,len(m[0]))]
    for i in range(0,len(m)):
        for i2 in range(0,len(m[i])):
            m[i][i2]=str(m[i][i2])
            ll=len(m[i][i2])
            if ll>l[i2]:
                l[i2]=ll;
    for i in range(0,len(m)):
        for i2 in range(0,len(m[i])):
            ll = len(m[i][i2])
            if ll < l[i2]:
                a=l[i2]-ll
                m[i][i2]=m[i][i2]+' '*a
    for i in range(0,len(m)):
        for i2 in range(0,len(m[i])):
            print(m[i][i2], end=" | ")
        print("")

def mrange(start,end,step=1):
    if step<0:
        return [n for n in range(start, end-1, step)]
    return [n for n in range(start,end+1,step)]

def mcopy(matrix):
    li=len(matrix)
    lj=len(matrix[0])
    newM=[[matrix[i][i2] for i2 in range(0, lj)] for i in range(0, li)]
    return newM

def norma(f,h):
    sum=0
    for fn in f:
        sum=sum+fn**2
    sum=sum*h
    sum=sum**(1/2)
    return sum

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return f'Decimal({str(obj)})'
        return json.JSONEncoder.default(self, obj)


class DecimalDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    def object_hook(self, obj):
        for key in obj:
            if isinstance(obj[key], str) and obj[key].startswith('Decimal'):
                dec = obj[key].split('Decimal(')
                obj[key]=decimal.Decimal(dec[1].split(')')[0])
        return obj

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


    for i in range(0, X):
        for j in range(0, Y):
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

    for i in range(Y):
        for j in range(X):
            value = board[i][j]
            if value == "":
                continue

            color = 'white' if value == "A" else 'black'

            x1, y1, x2, y2 = j * st+minor, i * st+minor, j * st + st-minor, i * st + st-minor
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline)
    root.update()

def checkers2(root=False, canvas=False, st=False, X=False, Y=False,board=False,visibable=False):
    all=X*Y
    CO=0
    minor=st*0.95
    if visibable:
        canvas.delete("all")
        build_board(canvas, st, X,Y)
    # * - пустые, [O] - синие, [CO] - черные, [O]v - зеленые

    # mprint(board)
    outline = '#000'

    for i in range(Y):
        for j in range(X):
            value = board[i][j]
            if value == "*":
                continue

            if value=="[O]":color='blue'
            elif value=="[CO]":
                color='black';CO=CO+1
            elif value=="[O]v":color='green'

            if visibable:
                x1, y1, x2, y2 = j * st+minor, i * st+minor, j * st + st-minor, i * st + st-minor
                canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline)
    if visibable:
        print(CO/all)
        root.update()
    return CO/all


def checkers3(root, canvas, st, X, Y,board=False):
    all=X*Y
    CO=0
    minor=st*0.95
    canvas.delete("all")
    build_board(canvas, st, X,Y)
    # 0 - пустые, 16 - [O] - синие, 1416 - [CO] - черные, 165 - [O]v - зеленые

    # mprint(board)
    outline = '#000'

    for i in range(Y):
        for j in range(X):
            value = board[i][j]
            if value == 0:
                continue

            if value==16:color='blue'
            elif value==1416:
                color='black';CO=CO+1
            elif value==165:color='green'

            x1, y1, x2, y2 = j * st+minor, i * st+minor, j * st + st-minor, i * st + st-minor
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline)
    print(CO/all)
    root.update()