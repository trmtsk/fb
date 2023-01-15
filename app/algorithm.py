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

# Reading CSV
df = pd.read_csv(f'./CSV/{user_id}_{DATE}.csv')
df2 = pd.read_csv(f'./CSV_dropna/{user_id}_{DATE}_dropna.csv')

# Conventional algorithm with HF
diff = 100
df3 = df2.iloc[0:diff, :]
x = df3.index_sec[0:diff]
y = df3.hf[0:diff]
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

time_end = time.time()
time_diff = int(time_start - time_end)
print(f"Done -> {user_id}_{DATE}_short")
print(f"time -> {int(time_diff/60)}m{time_diff%60}s")

# Conventional algorithm with BPM

# New algorithm with BPM

# New algorithm with HF

# # New algorithm with all components
