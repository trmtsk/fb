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
from sklearn.linear_model import LinearRegression
matplotlib.use('Agg')
mplstyle.use('fast')
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

step = 5

dff = 200
itr_bpm = int(len(df)/dff) - 1
#BPM
for i in range(0, itr_bpm):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("heart-rate")
    ax.plot(df["time"][i*dff:i*dff+dff], df["value"][i*dff:i*dff+dff], label = "BPM")
    plt.xticks(df["time"][i*dff:i*dff+dff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./BPMshort/{user_id}_{DATE}_BPM_s{i}.png')
    #plt.show()

diff = 100
itr = int(len(df2)/diff) - 1
#HF
for i in range(0, itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("hf")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["hf"][i*diff:i*diff+diff], label = "HF")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./HFshort/{user_id}_{DATE}_HF_s{i}.png')
    #plt.show()

#LF/HF
for i in range(0, itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("lf/hf")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["lf/hf"][i*diff:i*diff+diff], label = "LF/HF")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./LFHFshort/{user_id}_{DATE}_LFHF_s{i}.png')
    #plt.show()

#SDNN
for i in range(0, itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("sndd")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["sdnn"][i*diff:i*diff+diff], label = "SDNN")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./SDNNshort/{user_id}_{DATE}_SDNN_s{i}.png')
    #plt.show()

#rMSSD
for i in range(0, itr):
    fig, ax = plt.subplots(figsize=(30,10))
    ax.set_title(DATE + "   " + user_id)
    ax.set_xlabel("time")
    ax.set_ylabel("rmssd")
    ax.plot(df2["time"][i*diff:i*diff+diff], df2["rmssd"][i*diff:i*diff+diff], label = "rMSSD")
    plt.xticks(df2["time"][i*diff:i*diff+diff:step], rotation=60)
    plt.legend(loc = 'best')
    plt.savefig(f'./rMSSDshort/{user_id}_{DATE}_rMSSD_s{i}.png')
    #plt.show()

print(f"Done -> {user_id}_{DATE}_short")

x = df2["time"]
y = df2["hf"]
data = np.array(0,6)

n=len(x)
t_xy=sum(x*y)-(1/n)*sum(x)*sum(y)
t_xx=sum(x**2)-(1/n)*sum(x)**2
slope=t_xy/t_xx
intercept=(1/n)*sum(y)-(1/n)*slope*sum(x)
print('傾き=',slope,'切片=',intercept)
predict_x=intercept+slope*x
print('予測値=',predict_x)
resudial_y=y-predict_x
print('残差=',resudial_y)
predict_d=intercept+slope*data
print('x=[0,6] --> y=',predict_d)

fit = np.polyfit(x, y, 1)
print('[傾き,切片]=', fit)
func = np.poly1d(fit)
predict_x = func(x)
print('予測値=', predict_x)
resudial_y = y-predict_x
print('残差=', resudial_y)
predict_d = func(data)
print('x=[0,6] --> y=', predict_d)

'''
lr = LinearRegression()
X = x.reshape((len(x), 1))
lr.fit(X, y)
print('傾き=',lr.coef_, '切片=', lr.intercept_)
predict_x = lr.predict(X)
print('予測値=', predict_x)
resudial_y = y-predict_x
print('残差=', resudial_y)
D = data.reshape((len(data), 1))
predict_d = lr.predict(D)
print('x=[0,6] --> y=', predict_d)
'''