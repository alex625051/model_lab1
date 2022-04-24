import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import decimal
from matplotlib.ticker import FuncFormatter

from service import *
import datetime
continuedVer='1.6'
letConfigFromFile=True;
nrows = None;
continuedVer = '1.15'
# Вводные данные




def showGraph(FetaD_array, configs=False):
    if configs and letConfigFromFile:
        t0 = configs['t0']
        X = configs['X']
        Y = configs['Y']
        N_I = configs['N_I']
        xlimits = configs['xlimits']
        xlimits = [0, 60*10]

    def formatOx(x, pos):
        delta = datetime.timedelta(minutes=float(x))
        deltaStr=str(delta).replace(" days, ",'d')
        return deltaStr
    dF = FetaD_array
    fig = plt.figure(figsize=(18, 6), dpi = 200)
    yD = dF['fetaD'].tolist()
    yF = dF['fetaF'].tolist()
    yI = dF['fetaI'].tolist()
    yH = dF['fetaH'].tolist()
    yID=(dF['fetaI']+dF['fetaD']).tolist()
    x = dF['t'].tolist()

    ax = fig.add_subplot(111)
    ax.plot(x, yD,  color="black",label='D')
    ax.plot(x, yI, color="red", label='I')
    ax.plot(x, yH, color="blue", label='H')
    ax.plot(x, yF, color="green", label='F')
    ax.plot(x, yID,  '.', color="orange", label='I+D')
    ax.grid()
    ax.set_title(f"t(0)={t0}, N={X}x{Y}, I(0)={N_I/(X*Y)} ")
    ax.set_xlabel("t", fontsize=9, color='blue')
    ax.set_ylabel("", fontsize=9, color='orange')
    ax.set_xlim(xlimits)
    ax.legend()
    ax.xaxis.set_major_formatter(FuncFormatter(formatOx))

    fig.show()
    fig.savefig(f'out/fetas_array_{continuedVer}.png')
    print(dF)


if __name__ == '__main__':
    with open(f'out/FetaD_array_{continuedVer}.csv', 'r') as ff:
        configs=json.loads(ff.readline())
    FetaD_array = pd.read_csv(f'out/FetaD_array_{continuedVer}.csv', nrows=nrows, skiprows=1)
    showGraph(FetaD_array, configs)
