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
L = 0.1;
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



    # x1 = df1.columns
    # y1 = df1.index
    # X1,Y1 = np.meshgrid(x1,y1)
    # Z1 = df1
    # ax.append( fig.add_subplot(120+1+iteration, projection='3d'))
    # ax[-1].plot_surface(X1, Y1, Z1)
    #
    # x2 = df2.columns
    # y2 = df2.index
    # X2,Y2 = np.meshgrid(x2,y2)
    # Z2 = df2
    # ax.append( fig.add_subplot(120+1+iteration+1, projection='3d'))
    # ax[-1].plot_surface(X2, Y2, Z2)
    return comp

def main():

    parameters=[]

    dts=[i/1000000 for i in range(100,10000,1000)]#
    dhs=[i/1000000 for i in range(100,10000,1000)]#
    for i in dts:
        for i2 in dhs:
            parameters.append({'dt': i, 'dh': i2})
    fig = plt.figure()
    comp=[[], []]
    for iteration in range(0,len(parameters)):
        dt=parameters[iteration]['dt']
        dh=parameters[iteration]['dh']
        comp=compare_methods(dt, dh, fig,comp,iteration)

    df1=pd.DataFrame(comp[0])
    df2=pd.DataFrame(comp[1])
    x1 = df1['dt']
    y1 = df1['dh']
    Z1 = df1['U']
    ax1=fig.add_subplot(120+1, projection='3d')
    ax1.scatter(x1, y1, Z1)
    ax1.set_title('Явная схема')
    ax1.set_xlabel("dt", fontsize=9, color='blue')
    ax1.set_ylabel("dh", fontsize=9, color='orange')
    ax1.set_zlim([6, 7])


    x2 = df1['dt']
    y2 = df1['dh']
    Z2 = df2['U']
    ax2= fig.add_subplot(120+1+1, projection='3d')
    ax2.scatter(x2, y2, Z2)
    ax2.set_title('Неявная схема')
    ax2.set_xlabel("dt", fontsize=9, color='blue')
    ax2.set_ylabel("dh", fontsize=9, color='orange')
    ax2.set_zlim([6, 7])

# Выводим результаты сравнений
    fig.show()
    print(df1)
    print(df2)
    print(f'явная схема средняя:{df1["U"][(df1.U < 7) & (df1.U > 6)].mean()}')
    print(f'Неявная схема средняя:{df2["U"].mean()}')



if __name__ == '__main__':
    main()




