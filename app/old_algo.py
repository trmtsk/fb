import fitbit
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates
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
DATE = "2022-12-18"
user = 4

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

df['milestone'] = '' # index = 9
df2['milestone'] = ''
df['slope'] = 0 # 10
df2['slope'] = 0
df['decrease'] = 0 # 11
df2['increase rate'] = 0
df['kind'] = np.nan # 12
df2['kind'] = np.nan

# Conventional algorithm with BPM
#print('***old***')
s = 0
dff = 200
dff2 = 6
#y_half = int(dff/2)
threshold = df.value[s*dff] + 10
down_trend = False
counter = 0
bpm_info = np.zeros((100,3), dtype = int) # start, stop, amount of decrease
start = []
stop = []
decrease = []
itr = int(len(df.value)/dff2)

for i in range(itr):
    x = df.index_sec[i*dff2:i*dff2+dff2]
    y = df.value[i*dff2:i*dff2+dff2]
    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    #print(t_xy, t_xx)
    slope = round(t_xy/t_xx, 2)
    mean = int(y[i*dff2])
    
    if slope < 0 and down_trend == False and threshold > mean:
        down_trend = True
        basis = mean
        #print('start')
        #bpm_info[counter][0] = basis
        start.append((basis, i*dff2))
        df.iloc[i*dff2, 9] = 'start'
        df.iloc[i*dff2, 10] = slope
        df.iloc[i*dff2, 12] = 'BPM'
    elif slope >= 0 and down_trend == True:
        down_trend = False
        #bpm_info[counter][1] = mean
        #bpm_info[counter][2] = basis - mean
        stop.append((mean, i*dff2))
        decrease.append(basis - mean)
        counter += 1
        df.iloc[i*dff2, 9] = 'stop'
        df.iloc[i*dff2, 10] = slope
        df.iloc[i*dff2, 11] = basis - mean
        df.iloc[i*dff2, 12] = 'BPM'
        #print('stop')
    else:
        pass

#bpm_info_nonzero = bpm_info.nonzero()
#print(bpm_info_nonzero)
#print(start, stop, decrease)
'''
for i in range(len(decrease)):
    print(f'start = {start[i][0]}, stop = {stop[i][0]}, amount of decrease = {decrease[i]}')
    print(f'start time = {df.time[start[i][1]]}')
    print(f'stop time  = {df.time[stop[i][1]]}\n')
'''

# Conventional algorithm with HF
counter2 = 0
diff = 40
#print('old HF')
itr = int(len(df2.hf)/diff)
for i in range(itr):
    x = df2.index_sec[i*diff:i*diff+diff]
    y = df2.hf[i*diff:i*diff+diff]
    #data = np.array(0,6)
    y_half = int(diff/2)

    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    slope = round(t_xy/t_xx, 2)
    mean_y1 = sum(y[:y_half])/y_half # y_half must be an even number
    mean_y2 = sum(y[y_half:])/y_half
    increase_rate = round(mean_y2/mean_y1, 2)

    #print('increase rate = ', increase_rate)
    #print('slope = ', slope)

    if slope > 0 and increase_rate > 1.7:
        #print('***Up trend***')
        df2.iloc[i*dff2, 9] = 'up trend'
        df.iloc[i*dff2, 10] = slope
        df2.iloc[i*dff2, 11] = increase_rate
        df2.iloc[i*dff2, 12] = 'HF'
        counter2 += 1
    else:
        #print('***None***')
        pass
print(f'-old- bpm={counter}, hf={counter2} ')
# saveing to csv
df.dropna(subset=['kind']).to_csv(f'./CSV_old/{user_id}_{DATE}_df.csv', index=False)
df2.dropna(subset=['kind']).to_csv(f'./CSV_old/{user_id}_{DATE}_df2.csv', index=False)

# time_end
time_end = time.time()
time_diff = int(time_start - time_end)

print(f"Done -> {user_id}_{DATE}_old_algo")
print(f"time -> {int(time_diff/60)}m{time_diff%60}s")
