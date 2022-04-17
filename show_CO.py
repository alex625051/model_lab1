import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import decimal
from service import *

continuedVer='1.5-green_footer'

def show_from_CO_line():
    dF=pd.read_csv(f'out/FetaCO_{continuedVer}.csv')# ,nrows=100 )
    fig = plt.figure()

    x = dF.index.tolist()
    y= dF['0.015'].tolist()


    ax = fig.add_subplot(111)
    ax.plot(x,y)
    ax.grid()
    ax.set_title("Удельная концентрация СО")
    ax.set_xlabel("t", fontsize=9, color='blue')
    ax.set_ylabel("СО", fontsize=9, color='orange')
    ax.legend()
    fig.show()
    print(dF)


def show_from_back():
    dF=pd.read_json(f'out/present_status_{continuedVer}.json', lines=True)
    x=dF['t']
    x = x.map(lambda el: decimal_decoder(el))
    y=dF['CO']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y)
    ax.grid()
    ax.set_title("Удельная концентрация СО")
    ax.set_xlabel("t", fontsize=9, color='blue')
    ax.set_ylabel("СО", fontsize=9, color='orange')
    ax.legend()
    fig.show()


show_from_back()