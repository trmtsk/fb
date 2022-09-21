import fitbit
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

# ID, Token
CLIENT_ID = "238RZF"
CLIENT_SECRET = "379bdd55f5df0674fc423011c69aab8d"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSWkYiLCJzdWIiOiJCM1BDWVkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3NvYyB3YWN0IHdveHkgd3RlbSB3d2VpIHdzZXQgd3JlcyB3bG9jIiwiZXhwIjoxNjYyNTYyNDM0LCJpYXQiOjE2NjI1MzM2MzR9.i_ujpwaYV5-G7Cpst5p6xPATPqbieLP90KrqSmh1-A4"
REFRESH_TOKEN = "ea16869a6c21db3ed647ebb935d5c68acaa8bc43551fd8fae1c6013583d142df"

# a target date
DATE = "2022-08-14"

# Setting ID
authd_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET
                             ,access_token = ACCESS_TOKEN, refresh_token = REFRESH_TOKEN)

# getting heart rates
data_sec = authd_client.intraday_time_series('activities/heart', DATE, detail_level = '1sec') #'1sec', '1min', or '15min'
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
