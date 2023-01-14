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
mplstyle.use('fast')
matplotlib.use('Agg')
#matplotlib.use('Qt5Agg')
#plt.ion()
time_start = time.time()

# A target date and user
DATE = "2022-12-18"
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

tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict["access_token"]
refresh_token = token_dict["refresh_token"]

def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return

# Setting ID
authd_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token = access_token, refresh_token = refresh_token, refresh_cb = updateToken)

# Getting heart rates
data_sec = authd_client.intraday_time_series('activities/heart', DATE, detail_level = '1sec') #'1sec', '1min', or '15min'
heart_sec = data_sec["activities-heart-intraday"]["dataset"]

# Process

df = pd.DataFrame.from_dict(heart_sec)
#print("the number of data_sets = " + str(df.shape[0]))
mean = round(df["value"].mean(), 2)

#datetime
DATE_f = DATE + " 00:00:00"
df["index_sec"] = 0
#df["index_t"] = datetime.datetime.strptime(DATE_f, '%Y-%m-%d %H:%M:%S')

for i in range(len(df.time)):
    str = DATE + " " + df.time[i]
    dte = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    sec = int(dte.hour*3600 +dte.minute*60 + dte.second)
    df.iat[i,2] = sec
    #df.iat[i,3] = dte

#RRV
df = df.assign(
    RRI=lambda df: (60 / df["value"] * 1000).round(2)
)

df["hf"] = np.nan
df["lf/hf"] = np.nan
df["sdnn"] = np.nan
df["rmssd"] = np.nan

diff = 50 # a number of gathered samples
diff2 = 2 # must be a divisor of diff or add 1 to gap
gap = int(diff/diff2) + 1
itr = int(len(df["RRI"])/diff2) - gap

for i in range(itr):
    index = i*diff2 + diff
    results = fd.welch_psd(nni = df["RRI"][(index-diff):index], show = False)
    df.at[index, "lf/hf"] = results['fft_ratio']
    df.at[index, "hf"] = results['fft_abs'][1]
    sdnn = td.sdnn(nni = df["RRI"][(index-diff):index])
    df.at[index, "sdnn"] = float(sdnn[0])
    rmssd = td.rmssd(nni = df["RRI"][(index-diff):index])
    df.at[index, "rmssd"] = float(rmssd[0])

#CSV
print(df)
df.to_csv(f'./CSV/{user_id}_{DATE}.csv')

df2 = df.dropna()
df2.to_csv(f'./CSV_dropna/{user_id}_{DATE}_dropna.csv')

steps = 300
steps2 = 50

#BPM
fig, ax = plt.subplots(figsize=(30,10))
ax.set_title(DATE + "   " + user_id)
ax.set_xlabel("time")
ax.set_ylabel("heart-rate")
ax.plot(df["time"], df["value"], label = "BPM")
plt.xticks(df["time"][::steps], rotation=60)
plt.legend(loc = 'best')
plt.savefig(f'./BPM/{user_id}_{DATE}_BPM.png')
#plt.show()

#HF
fig, ax = plt.subplots(figsize=(30,10))
ax.set_title(DATE + "   " + user_id)
ax.set_xlabel("time")
ax.set_ylabel("hf")
ax.plot(df2["time"], df2["hf"], label = "HF")
plt.xticks(df2["time"][::steps2], rotation=60)
plt.legend(loc = 'best')
plt.savefig(f'./HF/{user_id}_{DATE}_HF.png')
#plt.show()

#LF/HF
fig, ax = plt.subplots(figsize=(30,10))
ax.set_title(DATE + "   " + user_id)
ax.set_xlabel("time")
ax.set_ylabel("lf/hf")
ax.plot(df2["time"], df2["lf/hf"], label = "LF/HF")
plt.xticks(df2["time"][::steps2], rotation=60)
plt.legend(loc = 'best')
plt.savefig(f'./LFHF/{user_id}_{DATE}_LFHF.png')
#plt.show()

#SDNN
fig, ax = plt.subplots(figsize=(30,10))
ax.set_title(DATE + "   " + user_id)
ax.set_xlabel("time")
ax.set_ylabel("sndd")
ax.plot(df2["time"], df2["sdnn"], label = "SDNN")
plt.xticks(df2["time"][::steps2], rotation=60)
plt.legend(loc = 'best')
plt.savefig(f'./SDNN/{user_id}_{DATE}_SDNN.png')
#plt.show()

#rMSSD
fig, ax = plt.subplots(figsize=(30,10))
ax.set_title(DATE + "   " + user_id)
ax.set_xlabel("time")
ax.set_ylabel("rmssd")
ax.plot(df2["time"], df2["rmssd"], label = "rMSSD")
plt.xticks(df2["time"][::steps2], rotation=60)
plt.legend(loc = 'best')
plt.savefig(f'./rMSSD/{user_id}_{DATE}_rMSSD.png')
#plt.show()

time_end = time.time()
time_diff = int(time_start - time_end)

print(f"Done -> {user_id}_{DATE}")
print(f"time -> {int(time_diff/60)}m{time_diff%60}s")
