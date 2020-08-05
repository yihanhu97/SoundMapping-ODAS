# This script combines dataframes from all microphone arrays produced one day ago relative to the date when the script is run

import glob
import os
import pandas as pd
import re
import json
import datetime
import time

#define the dates and hours to be combined

today = datetime.datetime.now() # extract todays date
a = today - datetime.timedelta(days = 1) # extract yesterday's date

a = str(a) # convert into string
year = a[:4] # extract yesterday's year
month = a[5:7] # extract yesterday's month
day = a[8:10] # extract yesterday


hours = []
for i in range(10):
    hours.append('0' + str(i))
for i in range(10, 25):
    hours.append(str(i))

#iterate through dates and combine. Then for each hour, for each array if a directory exists for that hour, list all the csv files for that hour. Read them and append 

date = year + '-' + month + '-' + day # setting date to yesterdays date
date_path = os.path.join('/home/ardelalegre/google-drive/ODAS/localization_dataframes/combined/', date)
for hour in hours:
    dfs = []
    for mic_number in range(4):
        if(not os.path.isdir('/home/ardelalegre/google-drive/ODAS/localization_dataframes/dataframes' + str(mic_number) + '/' + date + '/' + hour + '/')):
            continue

        for file in glob.glob('/home/ardelalegre/google-drive/ODAS/localization_dataframes/dataframes' + str(mic_number) + '/' + date +'/' + hour + '/*.csv'):
            print("Reading file " + file) 
            df = pd.read_csv(file)
            dfs.append(df)
    if(len(dfs) > 0):
        merged = pd.concat(dfs)
        #sort by time
        merged = merged.sort_values(['Time In Seconds'])

        if(not os.path.isdir(date_path)):
            os.mkdir(date_path)
        merged.to_csv(path_or_buf=date_path + '/' + hour + '.csv', index=False)

