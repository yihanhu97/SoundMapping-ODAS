#! /bin/bash
IP=$(hostname -I)
time=$(date)
echo "$time: $IP" >> IP0.log
rclone copy /home/pi/odas/IP0.log RaspberryPi:/ODAS