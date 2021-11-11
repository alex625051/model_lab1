from service import mrange, mprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import openpyxl
# вариант 6
Xmax=1; Ymax=6;
Ksi_t0_x0_ymax=10;
Psi_x_eq_0 = lambda y:3*(y**2)
Psi_x_max = lambda y:2+ 3*(y**2)
Psi_y_eq_0 = lambda x:2*(x**2)
Psi_y_max = lambda x:108+2*(x**2)

dhx = 0.01;
dhy = 0.01;
dt = 1;
Tmax=100
Nx = int(Xmax / dhx)
Ny = int(Ymax / dhy)
Nt = int(Tmax / dt)

Ksi = [[['' for i3 in mrange(0, Ny)] for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]
Psi = [[['' for i3 in mrange(0, Ny)] for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]
Vx = [[['' for i3 in mrange(0, Ny)] for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]
Vy = [[['' for i3 in mrange(0, Ny)] for i2 in mrange(0, Nx)] for i in mrange(0, Nt)]
alpha = [['' for i2 in mrange(0, Ny)] for i in mrange(0, Nx)]
beta = [['' for i2 in mrange(0, Ny)] for i in mrange(0, Nx)]
a = [['' for i2 in mrange(0, Ny)] for i in mrange(0, Nx)]
b = [['' for i2 in mrange(0, Ny)] for i in mrange(0, Nx)]
c = [['' for i2 in mrange(0, Ny)] for i in mrange(0, Nx)]

#Граничные условия:
Ksi[0]=[[Ksi_t0_x0_ymax for i3 in mrange(0, Ny)] for i2 in mrange(0, Nx)]

#итерация 1



