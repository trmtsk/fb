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
matplotlib.use('Agg')
#matplotlib.use('Qt5Agg')
#plt.ion()

# A target date and user
DATE = "2022-12-17"
user = 1
#print(type(DATE))

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

'''
#BPM
for i in range(0, (len(df)-5)):
    x_label = np.arange(0, 5)
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("heart-rate")
    ax.plot(df["time"][i:i+5], df["value"][i:i+5], label = "BPM")
    plt.xticks(x_label[::], df["time"][::], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./tmp/{user_id}_{DATE}_BPM_short.png')
    #plt.show()
'''
diff = 100
itr = int(len(df2)/diff) - 1
#HF
for i in range(0, itr):
    x_label = np.arange(0, diff)
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("hf")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["hf"][i*diff:i*diff+diff], label = "HF")
    plt.xticks(rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./tmp/{user_id}_{DATE}_HF_short{i}.png')
    #plt.show()

#LF/HF
for i in range(0, itr):
    x_label = np.arange(0, diff)
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("lf/hf")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["lf/hf"][i*diff:i*diff+diff], label = "LF/HF")
    plt.xticks(x_label, df2["time"], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./tmp/{user_id}_{DATE}_LFHF_short{i}.png')
    #plt.show()

#SDNN
for i in range(0, itr):
    x_label = np.arange(0, diff)
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("sndd")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["sdnn"][i*diff:i*diff+diff], label = "SDNN")
    plt.xticks(x_label, df2["time"], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./tmp/{user_id}_{DATE}_SDNN_short{i}.png')
    #plt.show()

#rMSSD
for i in range(0, itr):
    x_label = np.arange(0, diff)
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("rmssd")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["rmssd"][i*diff:i*diff+diff], label = "rMSSD")
    plt.xticks(x_label, df2["time"], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./tmp/{user_id}_{DATE}_rMSSD_short{i}.png')
    #plt.show()

print(f"Done -> {user_id}_{DATE}")
