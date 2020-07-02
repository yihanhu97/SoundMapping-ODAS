import glob
import os
import pandas as pd
import re 
import json
import datetime
import time

# Extract time information of each recording from the log file
def timeExtract(filename):
    with open(filename, 'rb') as f:
        # Start counting from the last byte
        counter = 1
        # Go to the 2nd byte before the end of the last line
        f.seek(-2, 2) 
        while f.read(1) != b'\n':
            f.seek(-2, 1)
            counter=counter+1
        endTime_line = f.readline().decode()
        # Go to the 2nd byte before the end of the last second line
        f.seek(-counter-2, 2)
        while f.read(1) != b'\n':
            f.seek(-2, 1)
        startTime_line = f.readline().decode()

    return [startTime_line, endTime_line]

# Calculate duration of each recording in microseconds
def durationinMicroseconds(filename):
    startTime = timeExtract(filename)[0].split()[2:]
    endTime = timeExtract(filename)[1].split()[2:]
    startTimeStr = startTime[0] + ' ' + startTime[1]
    endTimeStr = endTime[0] + ' ' + endTime[1]
    T1 = datetime.datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S.%f')
    T2 = datetime.datetime.strptime(endTimeStr, '%Y-%m-%d %H:%M:%S.%f')
    delta = T2-T1
    duration = delta.seconds*1000000 + delta.microseconds
    
    return duration, T1, T2

def extractDirectionalities(filename, mic_number):
    with open(filename, 'r') as f:
        text = f.read()

        # Use repex to store blocks of data into a list
    data = re.split('(?<=})\n(?={)', text) 
        # Delete the time info from the last data block
    tmp = data[-1][:(data[-1].rfind("}")+1)]
    data[-1] = tmp
        
    #list of src blocks 

    srcList = [json.loads(block)["src"] for block in data]

    
    #initialize dataframe to have colums: timestamp, time, data inside source
    #timestamp is the initial time stamp
    #time is the datetime value converted from the timestamp and intitial time
    #source is a 4 by 6 array where the rows are the source, and the columns are the source values
    df = pd.DataFrame(columns = ['Timestamp', 'Time', 'Time In Seconds', 'Microphone Number', 'Source ID', 'X', 'Y', 'Z', 'Activity'])
    
    #Used for calculating timestamps -> time
    duration, startTime, endTime = durationinMicroseconds(filename)
    start_time_in_seconds = time.mktime(startTime.timetuple())
    t = duration/len(data) / 1000000
    
    index = 1.0
    ind = 0
    df_dict = {}
    for block in srcList:
        if block[0]["id"] != 0 or block[1]["id"] != 0 or block[2]["id"] != 0 or block[3]["id"] != 0:
            time_in_seconds = start_time_in_seconds + (index - 1.0) * t
            for i in range(0, 4):
                if block[i]['id'] != 0:
                    df_dict[ind] = {"Timestamp": [index], "Time":datetime.datetime.fromtimestamp(time_in_seconds).strftime("%A, %B %d, %Y %I:%M:%S"), "Time In Seconds": time_in_seconds, "Microphone Number":mic_number, "Source ID": block[i]["id"], "X": block[i]["x"], "Y": block[i]["y"], "Z": block[i]["z"], "Activity": block[i]["activity"]}
                    ind = ind + 1
                    #df = df.append(pd.DataFrame({"Timestamp": [index], "Time":datetime.datetime.fromtimestamp(time_in_seconds).strftime("%A, %B %d, %Y %I:%M:%S"), "Time In Seconds": time_in_seconds, "Microphone Number":mic_number, "Source ID": block[i]["id"], "X": block[i]["x"], "Y": block[i]["y"], "Z": block[i]["z"], "Activity": block[i]["activity"]}, index=[0]))
        index = index + 1.0
    
    df = df.append(pd.DataFrame.from_dict(df_dict,"index"))
    return(df)

#define the dates and hours to be combined
years = ['2019', '2020']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
days = []
hours = []
for i in range(10):
    days.append('0' + str(i))
    hours.append('0' + str(i))
for i in range(10, 32):
    days.append(str(i))
for i in range(10, 25):
    hours.append(str(i))

#iterate through dates and combine
for year in years:
    for month in months:
        for day in days:
            date = year + '-' + month + '-' + day
            date_path = os.path.join('/home/ardelalegre/google-drive/ODAS/dataframes/combined/', date)
            for hour in hours:
            
                dfs = []
                for mic_number in range(4):
                    if(not os.path.isdir('/home/ardelalegre/google-drive/ODAS/dataframes/dataframes' + str(mic_number) + '/' + date + '/' + hour + '/')):
                        continue
                    
                    for file in glob.glob('/home/ardelalegre/google-drive/ODAS/dataframes/dataframes' + str(mic_number) + '/' + date +'/' + hour + '/*.csv'):
                        df = pd.read_csv(file)
                        dfs.append(df)
                if(len(dfs) > 0):
                    merged = pd.concat(dfs)
                    #sort by time
                    merged = merged.sort_values(['Time In Seconds'])
                
                    if(not os.path.isdir(date_path)):
                        os.mkdir(date_path)
                    merged.to_csv(path_or_buf=date_path + '/' + hour + '.csv', index=False)
       
                              
                
                
