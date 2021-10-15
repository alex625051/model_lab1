from service import mrange, mprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# start settings
L = 0.2;
D = 3 * 10 ** (-6);
Re = 6;
d = 10 * 10 ** (-3);
Pr = 400;
cs = 10;
c_t_eq0 = lambda x: 200 + 50 * x;
c_x_eq0 = 200;
h = 0.0001;
delta_t = 1;
T = 10000
Nx = int(L / h)
Nt = int(T / delta_t)
w = (1 + 0.5 * 0.55 * Re ** (1 / 2) * Pr ** (1 / 3)) * h / d
hw = h * w

aj = -D * delta_t / h ** 2;
bj = 1 + 2 * D * delta_t / h ** 2;
cj = -D * delta_t / h ** 2
a = ['' for i in mrange(0, Nx)]
b = ['' for i in mrange(0, Nx)]
c = ['' for i in mrange(0, Nx)]
for j in mrange(1, Nx):
    a[j] = aj
    b[j] = bj
    c[j] = cj

U = [['' for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]
for j in mrange(1, Nx):
    U[0][j] = c_t_eq0(j * h)
for n in mrange(0, Nt):
    U[n][0] = c_x_eq0

# for 1st step
alpha1 = 0;
beta1 = 200


def get_alpha1():
    return alpha1


def get_beta1():
    return beta1


def get_alpfa_beta(a, b, c, U, alpha, beta, n, j):
    feta = U;
    alpha[j] = -a[j] / (b[j] + c[j] * alpha[j - 1])
    beta[j] = (feta[n][j] - c[j] * beta[j - 1]) / (b[j] + c[j] * alpha[j - 1])
    return alpha, beta


def get_U_from_PGU(alpha, beta, n, U):
    U[n + 1][Nx] = (w * cs + beta[Nx - 1]) / (1 + w - alpha[Nx - 1])
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
    return U


for n in mrange(0, Nt - 1):
    U = iteration_t(n=n, U=U)
df=pd.DataFrame(U)

print(df)



x = df.columns
y = df.index
X,Y = np.meshgrid(x,y)
Z = df
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)
fig.show()


