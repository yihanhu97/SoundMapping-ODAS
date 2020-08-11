#!/usr/bin/env python
# coding: utf-8

# In[2]:


# CSE4223-ODAS will be installed in /home/pi/odas

# Setting up working directory
get_ipython().system('cd /home/pi/odas/CSE4223-ODAS/Matrix')

# Ask for array index from user input 
arrayInd = input("Enter array index: ")

# Create backup.sh based on array index
with open ('backup.sh', 'w') as rsh:
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
get_ipython().system('cp backup.sh cleanup.sh crontab filemanager.sh IPupload.sh rclone.conf startup.sh ~/odas')
get_ipython().system('cp matrix_creator_local.cfg ~/odas/config/matrix-demo')
get_ipython().system('cp -r python ~/odas')

# Make bash scripts executables, set up crontab, set up rclone
get_ipython().system('cd ~/odas')
get_ipython().system('sudo chmod +x cleanup.sh filemanager.sh startup.sh IPupload.sh backup.sh')
get_ipython().system('sudo crontab -e crontab')
get_ipython().system('cp rclone.conf ~/.conf/rclone')

# create recordings folder
get_ipython().system('mkdir recordings')
get_ipython().system('cd recordings')
get_ipython().system('mkdir SST SSL separated postfiltered raw')

# reboot
get_ipython().system('sudo reboot')

