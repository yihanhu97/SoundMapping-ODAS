import glob
import os
import pandas as pd
import re 
import json
import datetime
import time
import shutil
import datetime

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

# Converts .log files into pandas dataframes
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
    t = duration/len(data) / 1000000.0
    
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

#Main

print("Execution of processAllLogs_new.py started at " + str(datetime.datetime.now()))

records0 = glob.glob('/home/ardelalegre/google-drive/ODAS/logs0/SST/*.log')
records1 = glob.glob('/home/ardelalegre/google-drive/ODAS/logs1/SST/*.log')
records2 = glob.glob('/home/ardelalegre/google-drive/ODAS/logs2/SST/*.log')
records3 = glob.glob('/home/ardelalegre/google-drive/ODAS/logs3/SST/*.log')

records = [records0, records1, records2, records3]

for mic_number in range(len(records)):
    
    destination = "/home/ardelalegre/google-drive/ODAS/logs" + str(mic_number) + "/SST/Processed"
    print("Now processing logs" + str(mic_number))
    
    for log in records[mic_number]:
        
        with open(log, 'r') as f:
                firstline = f.readline()
                if firstline == "SST log contains no useful data\n":
                    try:
                        temp = shutil.move(log,destination) # new
                    except:
                        continue
                    
                    continue
                    
        log_string = log[:-6] + '.log' # modification to account for added array number to path
#         print(log_string)
        
        hour = log_string[log_string.rfind('_') + 1: log_string.rfind('_') + 1 + 2]
        day = log_string[log_string.find('_') + 1: log_string.rfind('_')]
        path = log_string[:log_string.find('S/') + 2] + 'dataframes/dataframes' + str(mic_number) + '/'
#         print(path)
#         print(day)
#         print(hour)
        try:
            if(not os.path.isdir(os.path.join(path, day))):
                os.mkdir(os.path.join(path, day))
            
            path = os.path.join(path, day, hour)
            if(not os.path.isdir(path)):
                print("making directory: " + str(path))
                os.mkdir(path)
        
        except:
            continue
            
#         print(path)
        try:
            df = extractDirectionalities(log, mic_number)
            if(not os.path.isdir(path)):
                os.mkdir(path)
            df.to_csv(path_or_buf=path+ '/' + log[log.find('_') + 1:log.find('.')]+'.csv', index=False)
            temp = shutil.move(log,destination) # new
        except:
            print('Could not process file: ' + log)
        
        
print("Execution of processAllLogs_new.py ended at " + str(datetime.datetime.now()))