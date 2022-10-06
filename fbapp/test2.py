import fitbit
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime

# ID, Token
CLIENT_ID = "238WS8"
CLIENT_SECRET = "06fc5a18824f4dd8801729eca707cf72"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhXUzgiLCJzdWIiOiJCNzVEUkwiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3NsZSB3c2V0IHdhY3Qgd3JlcyB3b3h5IiwiZXhwIjoxNjY0OTgwMDY1LCJpYXQiOjE2NjQ5NTEyNjV9.bhhfaYmuBKOZuTGaAFLpuTM8wIS0DhLpzWHgjGzYk5M"
REFRESH_TOKEN = "7edaddf24ac51d5b0075f7fc1f5f3c65c828c7f9c97488265c118bcf0d33101c"

# a target date
DATE = "2022-10-05"

# Setting ID
authd_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET
                             ,access_token = ACCESS_TOKEN, refresh_token = REFRESH_TOKEN)

# getting heart rates
data_sec = authd_client.intraday_time_series('activities/heart', DATE, detail_level = '1min') #'1sec', '1min', or '15min'
heart_sec = data_sec["activities-heart-intraday"]["dataset"]
heart_sec[:10]

#print (heart_sec)

heart_df = pd.DataFrame.from_dict(heart_sec)
print(heart_df.shape)
print(heart_df.head(20))

heart_df.plot(y="value", figsize=(20,5))
plt.show()

#df = pd.read_csv("heart20190718.csv", index_col=0, parse_dates=[0])

#df.plot(figsize=(10,5))
