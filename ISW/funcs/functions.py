import time
import math as m
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import funcs.prueba

def get_symbols():
    dataFrame = pd.read_csv("/home/ivalenzu/Downloads/companylist.csv")
    dataFrame = dataFrame[['Symbol', 'Name']]
    values = list()

    for indice_fila, fila in dataFrame.iterrows():
        values.append((fila['Symbol'], fila['Symbol'] + " -- " + fila['Name'])) 

    return values
    
def icsv(path):
    data_frame = pd.read_csv(path)
    data_frame = data_frame[['Date', 'Close']]
    return data_frame

def volatility(df):
    lista = list()
    for i in range(0, df.shape[0]):
        if i == 0:
            lista.append(0)
        else:
            lista.append(df.at[i, 'Close']/df.at[i-1, 'Close'])
    df['Dt'] = lista
    df['Rt'] = np.log(lista)
    df.at[0, 'Rt'] = 0
    mean = np.mean(df['Rt'])
    df['Dev'] = pow(df['Rt'] - mean, 2)

    return m.sqrt(np.mean(df['Dev'])*252)

def iterations(x,y,price,riskfree,volatile,times, type_opt):
    np.random.seed(1)
    estimate_gain = 0
    estimate_value = 0
    times = (times/12)/y
    for i in range(0, x):
        for j in range(0, y):
            if j == 0:
                S = [price]
            else:
                auxiliar = riskfree*S[j-1]*times + volatile*S[j-1]*np.random.normal(0, 1, 1)*m.sqrt(times)
                S.append(S[j-1] + auxiliar)       
        if i == 0:
            Z = S
        else:
            list_of = [Z, S]
            Z = [sum(x) for x in zip(*list_of)]
        if type_opt:
            estimate_gain = estimate_gain + max((S[y-1] - price), 0)
        else:
            estimate_gain = estimate_gain + max((price - S[y-1]), 0)
        estimate_value = estimate_value + S[y-1]

    return [a / x for a in Z], estimate_gain/x, estimate_value/x

def save_plot(x_axis, y_axis, symbol):
    plt.plot(x_axis,y_axis)
    plt.xlabel('Time [Months]')
    plt.ylabel('Action Value [Dollars]')
    plt.grid(True)
    plt.savefig('/home/ivalenzu/Languages/Django/ISW/ISW/static/images/' + symbol + '.jpg')
    plt.close()

def main(symbol, exercise_time, price, riskfree, type_opt):
    funcs.prueba.download_quotes(symbol,exercise_time)
    data_frame = icsv('/home/ivalenzu/Languages/Django/ISW/ISW/funcs/csv/' + symbol + '.csv')
    volatile = volatility(data_frame)
    y_axis, estimate_gain, estimate_value = iterations(100, 5000, price, riskfree, volatile, exercise_time, type_opt)
    size_interval = (exercise_time/12)/5000
    x_axis = np.linspace(size_interval, exercise_time/12, 5000)
    estimate_gain = np.exp(-riskfree * exercise_time/12 * estimate_gain)
    estimate_value = estimate_value
    save_plot(x_axis,y_axis, symbol)
    time.sleep(1)
    return estimate_gain[0], estimate_value[0]
            