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
df3 = pd.read_csv(f'./CSV_dropna/{user_id}_{DATE}_dropna.csv')
df4 = pd.read_csv(f'./CSV_dropna/{user_id}_{DATE}_dropna.csv')

df['milestone'] = '' # index = 9
df2['milestone'] = ''
df3['milestone'] = ''
df4['milestone'] = ''
df['slope'] = 0 # 10
df2['slope'] = 0
df3['slope'] = 0
df4['slope'] = 0
df['decrease'] = 0 # 11
df2['decrease'] = ''
df3['decrease'] = ''
df4['decrease'] = ''
df['kind'] = np.nan # 12
df2['kind'] = np.nan
df3['kind'] = np.nan
df4['kind'] = np.nan

counter, counter2, counter3, counter4 = 0, 0, 0, 0

# New algorithm with BPM
#print('***New BPM***')
s = 0
dff = 200
dff2 = 6
#y_half = int(dff/2)
threshold = df.value.mean()
#print (threshold)
down_trend = False
#counter = 0
#bpm_info2 = np.zeros((100,3), dtype = int) # start, stop, amount of decrease
start_n = []
stop_n = []
decrease_n = []
itr = int(len(df.value)/dff2)
print(itr)
for i in range(itr):
    x = df.index_sec[i*dff2+4:i*dff2+4+dff2]
    y = df.value[i*dff2+4:i*dff2+4+dff2].rolling(5).mean().fillna(df.value[i*dff2+4])
    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    #print(t_xy, t_xx)
    slope = round(t_xy/t_xx, 2)
    #print(slope)
    mean = int(y[i*dff2+4])
    
    if slope < -0.2 and down_trend == False and threshold > mean:
        down_trend = True
        basis = mean
        #bpm_info2[counter][0] = basis
        start_n.append((basis, i*dff2+4))
        #print('  start')
        df.iloc[i*dff2, 9] = 'start'
        df.iloc[i*dff2, 10] = slope
        df.iloc[i*dff2, 12] = 'BPM'
    elif slope >= 0.2 and down_trend == True:
        #bpm_info2[counter][1] = mean
        #bpm_info2[counter][2] = basis - mean
        stop_n.append((mean, i*dff2+4))
        decrease_n.append(basis - mean)
        #counter += 1
        down_trend = False
        #print('  end')
        df.iloc[i*dff2, 9] = 'stop'
        df.iloc[i*dff2, 10] = slope
        df.iloc[i*dff2, 11] = basis - mean
        df.iloc[i*dff2, 12] = 'BPM'
        counter += 1
    else:
        pass
'''
for i in range(len(decrease_n)):
    print(f'start = {start_n[i][0]}, stop = {stop_n[i][0]}, amount of decrease = {decrease_n[i]}')
    print(f'start time = {df.time[start_n[i][1]]}')
    print(f'stop time  = {df.time[stop_n[i][1]]}\n')
'''
#print(start, stop, start_n, stop_n)

# New algorithm with HF
diff = 10
#print('New HF')
itr = int(len(df2.hf)/diff)
print(itr)
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

    #print('increase rate = ', increase_rate)
    #print('slope = ', slope)

    if slope > 10 and y.mean() > df2.hf.mean()+1000:
        #print('***Up trend***')
        df2.iloc[i*dff2, 9] = 'up trend'
        df.iloc[i*dff2, 10] = slope
        df2.iloc[i*dff2, 12] = 'HF'
        counter2 += 1
    else:
        #print('***None***')
        pass

# New algorithm with SDNN
#print('New SDNN')
itr = int(len(df3.sdnn)/diff)
for i in range(itr):
    x = df3.index_sec[i*diff:i*diff+diff]
    y = df3.sdnn[i*diff:i*diff+diff]
    #data = np.array(0,6)

    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    slope = round(t_xy/t_xx, 2)

    if slope > 0.5 and y.max() > df3.sdnn.mean():
        #print('***Up trend***  slope = ', slope)
        df3.iloc[i*dff2, 9] = 'up trend'
        df3.iloc[i*dff2, 10] = slope
        df3.iloc[i*dff2, 12] = 'SDNN'
        counter3 += 1
    else:
        #print('***None***  slope = ', slope)
        pass

# New algorithm with rMSSD
#print('New rMSSD')
itr = int(len(df4.rmssd)/diff)
for i in range(itr):
    x = df4.index_sec[i*diff:i*diff+diff]
    y = df4.rmssd[i*diff:i*diff+diff]
    #data = np.array(0,6)

    n = len(x)
    t_xy = sum(x*y)-(1/n)*sum(x)*sum(y)
    t_xx = sum(x**2)-(1/n)*sum(x)**2
    slope = round(t_xy/t_xx, 2)

    if slope > 0.1 and y.max() > df4.rmssd.mean():
        #print('***Up trend***  slope = ', slope)
        df4.iloc[i*dff2, 9] = 'up trend'
        df4.iloc[i*dff2, 10] = slope
        df4.iloc[i*dff2, 12] = 'rMSSD'
        counter4 += 1
    else:
        #print('***None***  slope = ', slope)
        pass

print(f'-new- bpm={counter}, hf={counter2}, sdnn={counter3}, rmssd={counter4}')

# saveing to csv
df = df.dropna(subset=['kind'])
df2 = df2.dropna(subset=['kind'])
df3 = df3.dropna(subset=['kind'])
df4 = df4.dropna(subset=['kind'])

df_concat = pd.concat([df, df2, df3, df4])
df_concat = df_concat.reset_index(drop=True)
df_concat.to_csv(f'./CSV_concat/{user_id}_{DATE}_concat.csv', index=False)

# New algorithm with all components
l = []
for i in range(len(df_concat.index_sec)):
    if df_concat.kind[i] == 'BPM' and df_concat.milestone[i] == 'start':
        for j in range(len(df_concat.index_sec)):
            if df_concat.kind[j] != 'BPM':
                index_i = df_concat.index_sec[i]
                index_j = df_concat.index_sec[j]
                if index_i-1800 < index_j and index_i+1800 > index_j:
                    print(df_concat.time[i], df_concat.time[j], df_concat.kind[j])
                    if df_concat.time[i] not in l:
                        l.append(df_concat.time[i])
#print('\n', l)
#print(f'count = {len(l)}\n')

'''
df.to_csv(f'./CSV_new/{user_id}_{DATE}_df.csv', index=False)
df2.to_csv(f'./CSV_new/{user_id}_{DATE}_df2.csv', index=False)
df3.to_csv(f'./CSV_new/{user_id}_{DATE}_df3.csv', index=False)
df4.to_csv(f'./CSV_new/{user_id}_{DATE}_df4.csv', index=False)
'''

# writing to txt
str_l = ', '.join(l)
f = open('new.txt', 'a')

f.write(f" -> {user_id}_{DATE}_new_algo\n")
f.write(str_l + '\n')
f.write('count = ' + str(len(l)) + '\n')

f.close()

# time_end
time_end = time.time()
time_diff = int(time_start - time_end)

print(f"Done -> {user_id}_{DATE}_new_algo")
print(f"time -> {int(time_diff/60)}m{time_diff%60}s")
