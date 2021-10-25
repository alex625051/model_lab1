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
L = 7;
Xmax=20;tmax=10;
dh=0.05
m1=15*L/40;m2=25*L/40;
sigma=L/12.6;
LGU_x=lambda x: math.exp(-((x-m1/sigma)**2))+math.exp(-((x-m2/sigma)**2));
LGU_t=lambda n: math.exp(-((-m1/sigma)**2))+math.exp(-((-m2/sigma)**2))


def get_U_NEyavnaya( U, n, j,dt,dh):
    U[n + 1][j] =(dh*U[n][j] + dt*U[n+1][j-1]) / (dh+dt)
    return U

def get_U_Zet( U, n, j,dt,dh):
    U[n + 1][j] =U[n][j]+(dt*(U[n+1][j-1]-U[n][j+1]))/(2*dh+dt)
    return U

def get_U_Podkova( U, n, Nx,dt,dh):
    U[n + 1][Nx] =((2*dh-dt)*U[n][Nx] + dt*(U[n+1][Nx-1]+U[n][Nx-1])) / (2*dh+dt)
    return U

def compare_methods(dt,dh,fig,comp,iteration):
    Nx = int(Xmax / dh)
    Nt = int(tmax / dt)

    # Создаем матрицу U по времени и Х с устыми элементами
    U = [['' for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]

    # Заполняем граничные условия
    for j in mrange(1, Nx):
        U[0][j] = LGU_x(j*dh);
    for n in mrange(0, Nt):  # левое ГУ для x0
        U[n][0] = LGU_t(n);
    U_Zet=mcopy(U)
    U_NEyavnaya=mcopy(U)


    # считаем по левому неявному уголку
    for n in mrange(0, Nt - 1):
        for j in mrange(1, Nx, 1):
            U_NEyavnaya= get_U_NEyavnaya( U_NEyavnaya, n, j,dt,dh)

    # считаем по Z-схеме
    for n in mrange(0, Nt - 1):
        for j in mrange(1, Nx-1, 1):
            U_Zet= get_U_Zet( U_Zet, n, j,dt,dh)
        # Дополняем правые крайние значения по схеме "родкова" для Z-схемы
        U_Zet= get_U_Podkova( U_Zet, n, Nx,dt,dh)



    return U_NEyavnaya,U_Zet

def show_extrems(data_line,ax,x):
    #Убираем мелкие флуктуации
    data_line=[el if el[0]>0.001 else [np.NaN]  for el in data_line ]
    df = pd.DataFrame(data_line, columns=['data'])
    # Find local peaks
    df['min'] = df.data[(df.data.shift(1) > df.data) & (df.data.shift(-1) > df.data)]
    df['max'] = df.data[(df.data.shift(1) < df.data) & (df.data.shift(-1) < df.data)]
    # Plot extrems
    ax[-1].scatter(x, df['min'], c='r')
    ax[-1].scatter(x, df['max'], c='g')
    return ax


def draw_wave_graf(dt,dh,U,fig,ax,title,position=1):
    Nx = int(Xmax / dh)
    Nt = int(tmax / dt)
    x=[x*dh for x in range(0,Nx+1)]
    y1=pd.DataFrame(U[int(Nt*0.5)]).values.tolist()
    y2=pd.DataFrame(U[int(Nt*1.0)]).values.tolist()
    y3=pd.DataFrame(U[int(Nt*0)]).values.tolist()


    ax.append(fig.add_subplot(210+position))
    ax[-1].plot(x, y1,label = f't={0.5*tmax}')
    ax[-1].plot(x, y2,label = f't={1*tmax}')
    ax[-1].plot(x, y3,label = f't={0.0*tmax}')
    ax[-1].grid()
    ax[-1].legend()
    ax[-1].set_title(title)
    ax[-1].set_xlabel("x", fontsize=9, color='blue')
    ax[-1].set_ylabel("U", fontsize=9, color='orange')

    # обозначаем екстремумы функции
    ax=show_extrems(data_line=pd.DataFrame(U[int(Nt*0.0)]).values.tolist(),ax=ax,x=x)
    ax=show_extrems(data_line=pd.DataFrame(U[int(Nt*1)]).values.tolist(),ax=ax,x=x)
    return fig,ax

def main():
    ax=[]
    parameters=[]
    # формирование  пула  значений  dt и  dh  для сравнительного анализа методов.
    dts=[0.001]#
    dhs=[0.05]#неизменно

    for i in dts:
        for i2 in dhs:
            parameters.append({'dt': i, 'dh': i2})
    fig = plt.figure()
    comp=[[], []]

    position = 0;
    for iteration in range(0,len(parameters)):
        position=position+1
        dt=parameters[iteration]['dt']
        dh=parameters[iteration]['dh']
        U_NEyavnaya,U_Zet=compare_methods(dt, dh, fig,comp,iteration)

        title=f'Схема неявный уголок. dt={dt}'
        fig,ax=draw_wave_graf(dt, dh, U_NEyavnaya, fig, ax, title,position=position)

        title=f'Схема Zet. dt={dt}'
        fig,ax=draw_wave_graf(dt, dh, U_Zet, fig, ax, title,position=position+1)



# Выводим результаты сравнений
    fig.show()





if __name__ == '__main__':
    main()




