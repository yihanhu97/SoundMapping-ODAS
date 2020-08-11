#!/usr/bin/env python
# coding: utf-8

# In[1]:

# CSE4223-ODAS will be installed in /home/pi/odas

import subprocess as p

# Setting up working directory
p.run(["cd","/home/pi/odas/CSE4223-ODAS/Matrix"])

# Ask for array index from user input 
arrayInd = input("Enter array index: ")

# Create backup.sh based on array index
with open ("backup.sh", "w") as rsh:
    rsh.write(
'''
#! /bin/bash
rclone copy /home/pi/odas/recordings/SST RaspberryPi:/ODAS/logs{0}/SST
rclone copy /home/pi/odas/recordings/SSL RaspberryPi:/ODAS/logs{0}/SSL
rclone copy /home/pi/odas/recordings/separated RaspberryPi:/ODAS/recordings{0}/separated
rclone copy /home/pi/odas/recordings/postfiltered RaspberryPi:/ODAS/recordings{0}/postfiltered
'''.format(arrayInd))

# Create IPupload.sh based on array index
with open ('IPupload.sh', 'w') as rsh:
    rsh.write(
'''
#! /bin/bash
IP=$(hostname -I)
time=$(date)
echo "$time: $IP" >> /home/pi/odas/IP{0}.log 
rclone copy /home/pi/odas/IP{0}.log RaspberryPi:/ODAS
''' .format(arrayInd))

# Save arrayInd into a file
with open("/home/pi/odas/arrayInfo.txt","w") as f:
    f.writelines(arrayInd)

# Copy files to their working directory
p.run(["cp","backup.sh","cleanup.sh","crontab","filemanager.sh","IPupload.sh","rclone.conf","startup.sh","~/odas"])
p.run(["cp","matrix_creator_local.cfg","~/odas/config/matrix-demo"])
p.run(["cp","-r","python","~/odas"])

# Make bash scripts executables, set up crontab, set up rclone
p.run(["cd","~/odas"])
p.run(["sudo","chmod","+x","cleanup.sh","filemanager.sh","startup.sh","IPupload.sh","backup.sh"])
p.run(["sudo","crontab","-e","crontab"])
p.run(["cp","rclone.conf","~/.conf/rclone"])

# create recordings folder
p.run(["mkdir","recordings"])
p.run(["cd","recordings"])
p.run(["mkdir","SST","SSL","separated","postfiltered","raw"]) 

# reboot
p.run(["sudo","reboot"])