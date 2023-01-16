import fitbit
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates
from ast import literal_eval
import pyhrv
import pyhrv.frequency_domain as fd
import pyhrv.time_domain as td
from scipy import interpolate
import biosppy
import matplotlib
import matplotlib.style as mplstyle
import time
import math
matplotlib.use('Agg')
mplstyle.use('fast')
#matplotlib.use('Qt5Agg')
#plt.ion()
time_start = time.time()

# A target date and user
DATE = "2022-12-17"
user = 1

# ID, Token
if user == 1:
    user_id = "fitbit_1"
    CLIENT_ID = "238RZF"
    CLIENT_SECRET = "379bdd55f5df0674fc423011c69aab8d"
    TOKEN_FILE = "./Tokens/token.txt"
elif user == 2:
    user_id = "fitbit_2"
    CLIENT_ID = "238WS8"
    CLIENT_SECRET = "06fc5a18824f4dd8801729eca707cf72"
    TOKEN_FILE = "./Tokens/token2.txt"
elif user == 3:
    user_id = "fitbit_3"
    CLIENT_ID = "238YPR"
    CLIENT_SECRET = "239a671f62b2813e9a4a7a8c4540c21b"
    TOKEN_FILE = "./Tokens/token3.txt"
else:
    user_id = "fitbit_4"
    CLIENT_ID = "23923D"
    CLIENT_SECRET = "1e60e3fe6195a024c91da05809f1aead"
    TOKEN_FILE = "./Tokens/token4.txt"

# Reading CSV
df = pd.read_csv(f'./CSV/{user_id}_{DATE}.csv')
df2 = pd.read_csv(f'./CSV_dropna/{user_id}_{DATE}_dropna.csv')


# Conventional algorithm with BPM
s = 0
dff = 200
dff2 = 6
df4 = df.iloc[0:dff, :]
#y_half = int(dff/2)
threshold = df4.value[s*dff] + 10
down_trend = False
counter = 0
bpm_info = np.zeros((100,3), dtype = int) # start, stop, amount of decrease
start = []
stop = []
decrease = []
itr = int(len(df4.value)/dff2)

for i in range(itr):
    x = df4.index_sec[i*dff2:i*dff2+dff2]
    y = df4.value[i*dff2:i*dff2+dff2]
    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    #print(t_xy, t_xx)
    slope = round(t_xy/t_xx, 2)
    mean = int(y[i*dff2])
    
    if slope < 0 and down_trend == False and threshold > mean:
        down_trend = True
        basis = mean
        #bpm_info[counter][0] = basis
        start.append((basis, i*dff2))
    elif slope >= 0 and down_trend == True:
        #bpm_info[counter][1] = mean
        #bpm_info[counter][2] = basis - mean
        stop.append((mean, i*dff2))
        decrease.append(basis - mean)
        #counter += 1
        down_trend = False
    else:
        pass

#bpm_info_nonzero = bpm_info.nonzero()
#print(bpm_info_nonzero)
#print(start, stop, decrease)
for i in range(len(decrease)):
    print(f'start = {start[i][0]}, stop = {stop[i][0]}, amount of decrease = {decrease[i]}')
    print(f'start time = {df.time[start[i][1]]}')
    print(f'stop time  = {df.time[stop[i][1]]}\n')

# Conventional algorithm with HF
diff = 100
print('New HF')
itr = int(len(df3.hf)/diff)
for i in range(itr):
    df3 = df2.iloc[i*diff:i*diff+diff, :]
    x = df3.index_sec[i*diff:i*diff+diff]
    y = df3.hf[i*diff:i*diff+diff]
    #data = np.array(0,6)
    y_half = int(diff/2)

    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    slope = round(t_xy/t_xx, 2)
    mean_y1 = sum(y[:y_half])/y_half # y_half must be an even number
    mean_y2 = sum(y[y_half:])/y_half
    increase_rate = round(mean_y2/mean_y1, 2)

    print('increase rate = ', increase_rate)
    print('slope = ', slope)

    if slope > 1.2 and increase_rate > 1.7:
        print('***Up trend***')
    else:
        print('***None***')
    print()


# New algorithm with BPM
print('***New***')
s = 0
dff = 200
dff2 = 6
df4 = df.iloc[0:dff, :]
#y_half = int(dff/2)
threshold = 85
down_trend = False
#counter = 0
#bpm_info2 = np.zeros((100,3), dtype = int) # start, stop, amount of decrease
start_n = []
stop_n = []
decrease_n = []
itr = int(len(df4.value)/dff2)

for i in range(itr):
    x = df4.index_sec[i*dff2+4:i*dff2+4+dff2]
    y = df4.value[i*dff2+4:i*dff2+4+dff2].rolling(5).mean().fillna(df.value[i*dff2+4])
    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    #print(t_xy, t_xx)
    slope = round(t_xy/t_xx, 2)
    #print(slope)
    mean = int(y[i*dff2+4])
    
    if slope < -0.02 and down_trend == False and threshold > mean:
        down_trend = True
        basis = mean
        #bpm_info2[counter][0] = basis
        start_n.append((basis, i*dff2+4))
        #print('  start')
    elif slope >= 0.01 and down_trend == True:
        #bpm_info2[counter][1] = mean
        #bpm_info2[counter][2] = basis - mean
        stop_n.append((mean, i*dff2+4))
        decrease_n.append(basis - mean)
        #counter += 1
        down_trend = False
        #print('  end')
    else:
        pass

for i in range(len(decrease_n)):
    print(f'start = {start_n[i][0]}, stop = {stop_n[i][0]}, amount of decrease = {decrease_n[i]}')
    print(f'start time = {df.time[start_n[i][1]]}')
    print(f'stop time  = {df.time[stop_n[i][1]]}\n')

#print(start, stop, start_n, stop_n)

# New algorithm with HF
diff = 100
print('New HF')
itr = int(len(df3.hf)/diff)
for i in range(itr):
    df3 = df2.iloc[i*diff:i*diff+diff, :]
    x = df3.index_sec[i*diff:i*diff+diff]
    y = df3.hf[i*diff:i*diff+diff]
    #data = np.array(0,6)
    y_half = int(diff/2)

    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    slope = round(t_xy/t_xx, 2)
    mean_y1 = sum(y[:y_half])/y_half # y_half must be an even number
    mean_y2 = sum(y[y_half:])/y_half
    increase_rate = round(mean_y2/mean_y1, 2)

    print('increase rate = ', increase_rate)
    print('slope = ', slope)

    if slope > 1.2 and increase_rate > 1.7:
        print('***Up trend***')
    else:
        print('***None***')
    print()

# New algorithm with SDNN
print('New SDNN')
itr = int(len(df3.sdnn)/diff)
for i in range(itr):
    diff = 100
    df3 = df2.iloc[i*diff:i*diff+diff, :]
    x = df3.index_sec[i*diff:i*diff+diff]
    y = df3.sdnn[i*diff:i*diff+diff]
    #data = np.array(0,6)

    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    slope = round(t_xy/t_xx, 2)

    if slope > 1.2 and y.max() > 80:
        print('***Up trend***  slope = ', slope)
    else:
        print('***None***  slope = ', slope)
    print()

# New algorithm with rMSSD
print('New rMSSD')
itr = int(len(df3.rmssd)/diff)
for i in range(itr):
    diff = 100
    df3 = df2.iloc[i*diff:i*diff+diff, :]
    x = df3.index_sec[i*diff:i*diff+diff]
    y = df3.rmssd[i*diff:i*diff+diff]
    #data = np.array(0,6)

    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    slope = round(t_xy/t_xx, 2)

    if slope > 1.2 and y.max() > 30:
        print('***Up trend***  slope = ', slope)
    else:
        print('***None***  slope = ', slope)
    print()

# New algorithm with all components


# time_end
time_end = time.time()
time_diff = int(time_start - time_end)

print(f"Done -> {user_id}_{DATE}_short")
print(f"time -> {int(time_diff/60)}m{time_diff%60}s")
