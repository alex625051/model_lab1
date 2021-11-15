from service import mrange, mprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import openpyxl
# вариант 3

# start settings
al=1/2
pi=math.pi
k=6;
D=k/100;
L = 1;
c_x_eq0 = lambda t: 0;
c_t_eq0 = lambda x: 0;
c_x_eqL = lambda t: k*(t**2)
h = 0.1;
delta_t = 0.01;
T = 1
Nx = int(L / h)
Nt = int(T / delta_t)


aj = -D * (pi**0.5)*(delta_t**al) / (2*(h ** 2));
bj = 1 + 1 * D * (pi**0.5)*(delta_t**al) / (h ** 2);
cj = -D * (pi**0.5)*(delta_t**al) / (2*(h ** 2));
a = ['' for i in mrange(0, Nx)]
b = ['' for i in mrange(0, Nx)]
c = ['' for i in mrange(0, Nx)]
for j in mrange(1, Nx):
    a[j] = aj
    b[j] = bj
    c[j] = cj

# Пустая матрица функции во времени
U = [['' for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]
for j in mrange(1, Nx):
    U[0][j] = c_t_eq0(x=j*h)
for n in mrange(0, Nt):
    U[n][0] = c_x_eq0(t=delta_t*n)

# for 1st step
def coeff(j):
    return (1+j)**2


def omega(n,j):
    omega=2*D*((n*delta_t)**2)
    omega=k*(((delta_t**(3/2))*((h*j)**2))*coeff(j)/(pi**(1/2))-omega)
    return omega


def feta(U,n,j):
    return 0.5*U[n][j]+pi*(delta_t**2)*omega(n,j)


def G(x):
    if x==1/2: return (math.pi)**(1/2)

def get_alpha1():
    alpha1 = 0;
    return alpha1


def get_beta1():
    beta1 = 0
    return beta1


def get_alpfa_beta(a, b, c, U, alpha, beta, n, j):
    alpha[j] = -a[j] / (b[j] + c[j] * alpha[j - 1])
    beta[j] = (feta(U=U,n=n,j=j)- c[j] * beta[j - 1]) / (b[j] + c[j] * alpha[j - 1])
    return alpha, beta


def get_U_from_PGU(alpha, beta, n, U):
    U[n + 1][Nx] = c_x_eqL(t=n*delta_t)
    return U


def get_U_nPlus1_j(alpha, beta, U, n, j):
    U[n + 1][j] = alpha[j] * U[n + 1][j + 1] + beta[j]
    return U


def iteration_t(n, U):
    alpha = ['' for i in mrange(0, Nx)]
    beta = ['' for i in mrange(0, Nx)]
    #          шаг 1. альфа и бета из первого граничного условия
    alpha[1] = get_alpha1()
    beta[1] = get_beta1()
    # шаг 2: получение альфа и бета на итерации n для всех j

    for j in mrange(2, Nx):
        alpha, beta = get_alpfa_beta(a=a, b=b, c=c, U=U, alpha=alpha, beta=beta, n=n, j=j)

    # Шаг 3. Определение U[n+1][Nx] из правого граничного условия
    U = get_U_from_PGU(alpha=alpha, beta=beta, n=n, U=U)

    # Шаг 5 вычисление U справа налево
    for j in mrange(Nx - 1, 1, -1):
        U = get_U_nPlus1_j(alpha=alpha, beta=beta, U=U, n=n, j=j)
        print(alpha)
    return U


for n in mrange(0, Nt - 1):
    U = iteration_t(n=n, U=U)
df=pd.DataFrame(U)
df.to_excel('out_data.xlsx')
print(df)
fig = plt.figure()




x = (df.columns)*h
y = (df.index)*delta_t
X,Y = np.meshgrid(x,y)
Z = df
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)
ax.grid()
ax.set_title("Поверхность С по х в измерении t")
ax.set_xlabel("x", fontsize=9, color='blue')
ax.set_ylabel("t", fontsize=9, color='orange')
ax.set_zlabel("C", fontsize=9, color='red')

x = [x * h for x in mrange(0, Nx)]
y1 = pd.DataFrame(U[int(Nt * 0.0)]).values.tolist()
y2 = pd.DataFrame(U[int(Nt * 0.5)]).values.tolist()
y3 = pd.DataFrame(U[int(Nt * 1)]).values.tolist()

ax1=fig.add_subplot(212)
ax1.plot(x, y1, label=f't={0.0 * T}')
ax1.plot(x, y2, label=f't={0.5 * T}')
ax1.plot(x, y3, label=f't={1 * T}')
ax1.grid()
ax1.legend()
ax1.set_xlabel("x", fontsize=9, color='blue')
ax1.set_ylabel("U", fontsize=9, color='orange')

fig.show()


