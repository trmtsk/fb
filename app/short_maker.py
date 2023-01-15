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

df = pd.read_csv(f'./CSV/{user_id}_{DATE}.csv')
df2 = pd.read_csv(f'./CSV_dropna/{user_id}_{DATE}_dropna.csv')

step = 5

dff = 200
itr_bpm = int(len(df)/dff) - 1

#BPM
y_max = df.value.max()
for i in range(0, itr_bpm):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("heart-rate")
    x = df["time"][i*dff:i*dff+dff]
    y = df["value"][i*dff:i*dff+dff]
    ax.set_ylim(0, y_max+10)
    ax.plot(x, y, label = "BPM")
    plt.xticks(df["time"][i*dff:i*dff+dff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./BPMshort/{user_id}_{DATE}_BPM_s{i}.png')
    #plt.show()

diff = 100
itr = int(len(df2)/diff)

#HF
y_max = df2.hf.max()
for i in range(itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("hf")
    x = df2["time"][i*diff:i*diff+diff]
    y = df2["hf"][i*diff:i*diff+diff]
    ax.set_ylim(0, y_max+100)
    ax.plot(x, y, label = "HF")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./HFshort/{user_id}_{DATE}_HF_s{i}.png')
    #plt.show()

#LF/HF
y_max = df2['lf/hf'].max()
for i in range(itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("lf/hf")
    x = df2["time"][i*diff:i*diff+diff]
    y = df2["lf/hf"][i*diff:i*diff+diff]
    ax.set_ylim(0, y_max+3)
    ax.plot(x, y, label = "LF/HF")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./LFHFshort/{user_id}_{DATE}_LFHF_s{i}.png')
    #plt.show()

#SDNN
y_max = df2.sdnn.max()
for i in range(itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("sndd")
    x = df2["time"][i*diff:i*diff+diff]
    y = df2["sdnn"][i*diff:i*diff+diff]
    ax.set_ylim(0, y_max+10)
    ax.plot(x, y, label = "SDNN")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./SDNNshort/{user_id}_{DATE}_SDNN_s{i}.png')
    #plt.show()

#rMSSD
y_max = df2.rmssd.max()
for i in range(itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("rmssd")
    x = df2["time"][i*diff:i*diff+diff]
    y =df2["rmssd"][i*diff:i*diff+diff]
    ax.set_ylim(0, y_max+5)
    ax.plot(x, y, label = "rMSSD")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./rMSSDshort/{user_id}_{DATE}_rMSSD_s{i}.png')
    #plt.show()

time_end = time.time()
time_diff = int(time_start - time_end)

print(f"Done -> {user_id}_{DATE}_short")
print(f"time -> {int(time_diff/60)}m{time_diff%60}s")
