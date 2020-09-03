#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time as timer
from datetime import datetime
from subprocess import Popen, PIPE
import signal

# Define countdown(): a function that calculates the time difference T between now and the next 5 minute mark
# Put the system to sleep for the length of T
def countdown5():
    timestamp = timer.time()
    t1 = datetime.fromtimestamp(timestamp)
    t2 = datetime.fromtimestamp(timestamp + 300 - timestamp % 300)
    duration = t2 - t1
    sleepTime = round(duration.total_seconds(),3)
    print("Time is " + str(t1) + ". Going to sleep now...")
    timer.sleep(sleepTime)
    print("Time is " + str(datetime.fromtimestamp(timer.time())) + ". Waking up now...")
    
# Find the array Index
f = open("/home/pi/odas/arrayInfo.txt","r")
arrayInd = f.readline()
f.close()
arrayAppendix = "_" + arrayInd

# First set the working directory to /home/pi/odas/bin
wd = "/home/pi/odas/bin"

# start the program at a 5-minute mark, run countdown()
countdown5()

# start the recording loop
while True:  
    try:
        # start odaslive
        print("Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting a new recording session")
        p2 = Popen(["./odaslive", "-vc", "../config/matrix-demo/matrix_creator_local.cfg"],
                   cwd=wd,
                   universal_newlines=True)
        # leave 10s for the remaining process and clean up
        timer.sleep(290)
        # end odaslive
        p2.send_signal(signal.SIGINT)
        p2.wait()
        print("Time is " + str(datetime.fromtimestamp(timer.time())) + ". Odaslive ended")
        
        # obtain the last access and modified time of raw files
        atime = os.path.getatime("/home/pi/odas/recordings/separated/separated.raw")
        mtime = os.path.getmtime("/home/pi/odas/recordings/separated/separated.raw")
        aT = datetime.fromtimestamp(atime)
        mT = datetime.fromtimestamp(mtime)
        
        date0, time0 = str(aT).split()
        time0 = time0.split('.')[0]

        # run odasparsing.py to check if SST.log has empty data
        p3 = Popen(["python3", "/home/pi/odas/python/odasparsing.py"], 
                   stdout=PIPE, 
                   stdin=PIPE, 
                   universal_newlines=True)    
        # flag returns a string that says if the file is or is not useful            
        flag = p3.communicate(input="/home/pi/odas/recordings/SST/SST.log")[0].strip()
        
        # append recording start time and end time to the end of SST.log and SSL.log
        with open("/home/pi/odas/recordings/SST/cleaned.log", "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))
        
        with open("/home/pi/odas/recordings/SSL/SSL.log", "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))

        # rename cleaned.log and remove SST.log
        os.rename("/home/pi/odas/recordings/SST/cleaned.log", 
                  "/home/pi/odas/recordings/SST/cSST_" + date0 + "_" + time0 + arrayAppendix + ".log")
        os.remove("/home/pi/odas/recordings/SST/SST.log")

        # If log file contains no data other than 0, delete raw files 
        key = "not useful"
        if flag == key:
            os.remove("/home/pi/odas/recordings/SSL/SSL.log")
            os.remove("/home/pi/odas/recordings/separated/separated.raw")
            os.remove("/home/pi/odas/recordings/postfiltered/postfiltered.raw")
        else:          
            os.rename("/home/pi/odas/recordings/SSL/SSL.log", 
                      "/home/pi/odas/recordings/SSL/cSSL_" + date0 + "_" + time0 + arrayAppendix + ".log")
            os.rename("/home/pi/odas/recordings/separated/separated.raw", 
                      "/home/pi/odas/recordings/separated/separated_" + date0+ "_" + time0 + arrayAppendix + ".raw")
            os.rename("/home/pi/odas/recordings/postfiltered/postfiltered.raw", 
                      "/home/pi/odas/recordings/postfiltered/postfiltered_" + date0+ "_" + time0 + arrayAppendix + ".raw")
#             os.rename("/home/pi/odas/recordings/raw/allChannels.raw", 
#                       "/home/pi/odas/recordings/raw/allChannels_" + date0+ "_" + time0 + "_0" + ".raw")

        print("Time is " + str(datetime.fromtimestamp(timer.time())) + ". Clean up finished")
        # wait until the next 5-minute mark
        print("Waiting to go into the next cycle...")
        countdown5()
                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()
        break
print("Recording ended")

