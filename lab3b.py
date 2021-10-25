from service import mrange, mprint, mcopy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)


# start settings
L = 1;
T = 1
LGU_x=0
LGU_t=lambda n,dt: 6 * dt * n


def get_U_yavnaya( U, n, j,dt,dh):
    U[n + 1][j] =U[n][j]+dt/dh*(U[n][j-1]-U[n][j])+(dt*6*math.exp(dh*j))*(1+dt*n)
    if math.isnan(U[n + 1][j]):
        U[n + 1][j]=0
    if U[n + 1][j] > 1000: U[n + 1][j]=1000
    if U[n + 1][j] < -1000: U[n + 1][j]=-1000
    return U

def get_U_NEyavnaya( U, n, j,dt,dh):
    U[n + 1][j] =(U[n][j] + dt/dh*U[n+1][j-1] +dt*6*math.exp(dh*j)*(1+dt*n))/(1+dt/dh)
    return U


def compare_methods(dt,dh,fig,comp,iteration):
    Nx = int(L / dh)
    Nt = int(T / dt)

    # Создаем матрицу U по времени и Х с устыми элементами
    U = [['' for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]

    # Заполняем граничные условия
    for j in mrange(1, Nx):
        U[0][j] = LGU_x;
    for n in mrange(0, Nt):  # левое ГУ для x0
        U[n][0] = LGU_t(n,dt);
    U_yavnaya=mcopy(U)
    U_NEyavnaya=mcopy(U)

    # считаем по явной схеме
    for n in mrange(0, Nt - 1):
        for j in mrange(1, Nx, 1):
            U_yavnaya= get_U_yavnaya( U_yavnaya, n, j,dt,dh)
    df1=pd.DataFrame(U_yavnaya)
    comp[0].append({'dt':dt,'dh':dh,'U':U_yavnaya[-1][-1]})


    # считаем по неявной схеме
    for n in mrange(0, Nt - 1):
        for j in mrange(1, Nx, 1):
            U_NEyavnaya= get_U_NEyavnaya( U_NEyavnaya, n, j,dt,dh)
    df2=pd.DataFrame(U_NEyavnaya)
    comp[1].append({'dt':dt,'dh':dh,'U':U_NEyavnaya[-1][-1]})



    return U_NEyavnaya

def main():

    parameters=[]
    # формирование  пула  значений  dt и  dh  для сравнительного анализа методов.
    dts=[0.001]#
    dhs=[0.001]#

    for i in dts:
        for i2 in dhs:
            parameters.append({'dt': i, 'dh': i2})
    fig = plt.figure()
    comp=[[], []]

    for iteration in range(0,len(parameters)):
        dt=parameters[iteration]['dt']
        dh=parameters[iteration]['dh']
        U_NEyavnaya=compare_methods(dt, dh, fig,comp,iteration)



    dt=dts[0]
    dh=dhs[0]
    Nx = int(L / dh)
    Nt = int(T / dt)
    dfn05=pd.DataFrame(U_NEyavnaya[int(Nt*0.5)])
    dfn10=pd.DataFrame(U_NEyavnaya[int(Nt*1.0)])
    df1=dfn05
    df2=dfn10
    print(df1.values.tolist())
    x=[x*dh for x in range(0,Nx+1)]
    print(x)
    y1=df1.values.tolist()
    y2=df2.values.tolist()
    y3=pd.DataFrame(U_NEyavnaya[int(Nt*0)]).values.tolist()

    ax1=fig.add_subplot(110+1)
    ax1.plot(x, y1,label = 't=0.5')
    ax1.plot(x, y2,label = 't=1')
    ax1.plot(x, y3,label = 't=0')
    ax1.grid()
    ax1.legend()
    ax1.set_title('Неявная схема. t=0.5 и t=1')
    ax1.set_xlabel("x", fontsize=9, color='blue')
    ax1.set_ylabel("U", fontsize=9, color='orange')

# Выводим результаты сравнений
    fig.show()





if __name__ == '__main__':
    main()




