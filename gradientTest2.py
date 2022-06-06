import math

from colour import Color
from PIL import Image, ImageDraw
import numpy as np
from concurrent.futures import ThreadPoolExecutor


red = Color()
green = Color()
ye = Color()
red.set_hex('#d99795')
green.set_hex('#abda74')
ye.set_hex('#fefe98')

l = 1000
a1=500;b1=250
a2=750;b2=375
R=990
bigA=1000

# colorsRed_Ye = list(red.range_to(ye, 1000))
# colorsY_green = list(ye.range_to(green, 1000))
# colorsGreen_green = list(green.range_to(green, 1000))

colorsRed_Ye = list(red.range_to(red, 1000))
colorsY_green = list(red.range_to(ye, 1000))
colorsGreen_green = list(ye.range_to(green, 1000))

# Пустой желтый фон.
im = Image.new('RGB', (1000, 1000))
draw = ImageDraw.Draw(im)

class Point:
    def __init__(self, x=0, y=0):
        self.x= x
        self.y = y

    def __call__(self):
        return (x, y)
    def get(self):
        return (x,y)

def yOflineFormula(p0:Point, x):
    x0=p0.x
    y0=p0.y
    return (y0/x0)*x

def commonWithOval(p0:Point,a,b):
    x0=p0.x
    y0=p0.y
    x=math.sqrt((a**2)*(b**2)/((b**2)+((y0/x0)**2)*a**2))
    y=yOflineFormula(p0, x)
    return Point(x,y)

def commonWithKvadrat(p0:Point,b,a):
    x0=p0.x
    y0=p0.y
    k=x0/y0
    if b/a < k:
        y=b
        x=y/k
    elif b/a>k:
        x=a;
        y=k*x
    else:
        x=a;
        y=b
    return Point(x,y)

def commonWithCircle(p0,r):
    x0=p0.x
    y0=p0.y
    x=math.sqrt((r**2)/(1+(y0/x0)**2))
    y=yOflineFormula(p0, x)
    return Point(x,y)

def rasst(p1:Point,p2:Point):
    l=math.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2)
    return l


def rgb2rgb(rgb):
    return(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def yOfOval(a,b,x):
    y=math.sqrt(((a**2)*(b**2)-(x**2)*b**2)/(a**2))
    return y

OO=Point(0,0)



def takeRaw(x0):
    yPoints=[]
    print(f'x= {x0}')
    for y0 in np.arange(1, 1000, 1):
        xy=Point(x0,y0)
        redYeOvalPoint=commonWithKvadrat(xy, a1, b1)
        yeGreenOvalPoint=commonWithKvadrat(xy, a2, b2)
        greenOver=commonWithKvadrat(xy, 1000, 1000)

        # l_0_oval1=rasst(OO,redYeOvalPoint)
        # l_oval1_oval2=rasst(redYeOvalPoint,yeGreenOvalPoint)
        # l_oval2_over=rasst(yeGreenOvalPoint,greenOver)
        l_0_thePoint=rasst(OO,xy)
        l_0_theRedYe=rasst(OO,redYeOvalPoint)
        l_0_theYeGreen=rasst(OO,yeGreenOvalPoint)
        # l_0_theGreenOver=rasst(OO,greenOver)

        if l_0_thePoint <= l_0_theRedYe:
            p1=OO
            p2=redYeOvalPoint
            colorsM = colorsRed_Ye

        elif l_0_thePoint <= l_0_theYeGreen:
            p1 = redYeOvalPoint
            p2 = yeGreenOvalPoint
            colorsM = colorsY_green

        else:# l_0_thePoint <= l_0_theGreenOver:
            p1 = yeGreenOvalPoint
            p2 = greenOver
            colorsM = colorsGreen_green


        len2Ovals=rasst(p1,p2)
        pointInSectorProcent = (l_0_thePoint-rasst(p1,OO))/len2Ovals

        nInColors=int(1000*pointInSectorProcent)
        if nInColors>999:nInColors=999

        yPoints.append([x0,y0,rgb2rgb(colorsM[nInColors].get_rgb())])
    return yPoints

with ThreadPoolExecutor(8) as executor:
    results = executor.map(takeRaw, np.arange(1, 1000, 1))
for p in results:
    for y in p:
        draw.point(xy=(y[0], 1000-y[1]), fill=y[2])



for x in np.arange(0, a1, 0.1):
    y= yOfOval(a1,b1,x)
    draw.point(xy=((x,1000-y)),fill='white')

for x in np.arange(0, a2, 0.1):
    y= yOfOval(a2,b2,x)
    draw.point(xy=((x,1000-y)),fill='white')

for x in np.arange(0, a1, 0.1):
    y= b1
    draw.point(xy=((x,1000-y)),fill='white')
for y in np.arange(0, b1, 0.1):
    x= a1
    draw.point(xy=((x,1000-y)),fill='white')

for x in np.arange(0, a2, 0.1):
    y= b2
    draw.point(xy=((x,1000-y)),fill='white')
for y in np.arange(0, b2, 0.1):
    x= a2
    draw.point(xy=((x,1000-y)),fill='white')

im.show()
im.save("out2/test2.png")
