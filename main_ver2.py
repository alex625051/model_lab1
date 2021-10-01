# This is a sample Python script.
import pprint
from PIL import Image, ImageDraw
import numpy as np



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def mprint(matrix):
    for i in matrix:
        print(i)


n = 80;
m = 60;
dt = 0.15;
h = 1;
nu = 1.1;
psi = [[0 for j in range(0, m + 1 + 1)] for i in range(0, n + 1 + 1)]
w = [[0 for j in range(0, m + 1 + 1)] for i in range(0, n + 1 + 1)]
k=0
kMax=1000
# Пустой желтый фон.
im = Image.new('RGB', (n*6+3, m*6+3), (219, 219, 100))
# im = Image.new('RGB', (600, 600), (219, 219, 219))
draw = ImageDraw.Draw(im)

def gran_uslovia(w, psi):
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            psi[0][j] = 0;
            psi[1][j] = 0;
            psi[n][j] = 0;
            psi[n + 1][j] = 0;
            psi[i][0] = 0;
            psi[i][1] = 0;
            psi[i][2] = 2;
            psi[i][m] = 0;
            psi[i][m + 1] = 0;
            w[1][j] = 2 * psi[2][j];
            w[i][1] = 2 * psi[i][2] - 2;
            w[n][j] = 2 * psi[n - 1][j];
            w[i][m] = 2 * psi[i][m - 1];
    return w, psi


def flow_1(w, psi, i, j):
    psi[i][j] = (psi[i - 1][j] + psi[i + 1][j] + psi[i][j - 1] + psi[i][j + 1] - w[i][j] * h * h) / 4
    return psi


def flow_2(w, psi, i, j):
    vx = -(psi[i][j + 1] - psi[i][j]);
    vy = -(-psi[i + 1][j] + psi[i][j]);
    w[i][j] = w[i][j] + vx * (w[i + 1][j] - w[i - 1][j]) * dt / 2 / h + vy * (
                w[i][j + 1] - w[i][j - 1]) * dt / 2 / h + nu * (w[i - 1][j] -
                    4 * w[i][j] + w[i + 1][j] + w[i][j - 1] + w[i][j + 1]) / h / h * dt;
    return vx,vy


steps=[]
images=[]
while k<kMax:
    k=k+1;
    w,psi=gran_uslovia(w, psi);
    for i in range (1,n+1):
        for j in range(1,m+1):
            psi=flow_1(w, psi, i, j)

    w,psi=gran_uslovia(w, psi);
    for i in range (1,n+1):
        for j in range(1,m+1):
            vx,vy=flow_2(w, psi, i, j)

    w,psi=gran_uslovia(w, psi);
    for i in range(n,0,-1):
        for j in range(m, 0, -1):
            psi = flow_1(w, psi, i, j)

    w,psi=gran_uslovia(w, psi);
    for i in range(n,0,-1):
        for j in range(m, 0,-1):
            vx, vy = flow_2(w, psi, i, j)

    if k%100==0:
        print(f"step {k}")
        #cleardevice
        points=[]

        steps.append(psi)
        for i in range(0,n+1+1):
            for j in range(0,m+1+1):
                color = round (abs((psi[i][ j] ))+1)

                draw.ellipse(
                    xy=(
                        (i * 6 -3, j * 6-3,
                        i * 6 +3, j * 6+3)
                    ), fill=(color*5,color*5,219)
                )

                # draw.point(
                #     xy=(
                #         (i, j)
                #     ), fill=(color * 5, color * 5, 199)
                # )

                frame = im.copy()
        images.append(frame)
        # im.show()
images[0].save('psi_function.gif',
               save_all=True,
               append_images=images[1:],
               duration=500,
               loop=0)














# w, psi = gran_uslovia(w=w, psi=psi)
mprint(w)
print("--------------------------------------------------")
mprint(psi)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # psi_j0=3*y**2


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
