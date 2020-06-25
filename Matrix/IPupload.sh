#! /bin/bash
IP=$(hostname -I)
time=$(date)
echo "$time: $IP" >> /home/pi/odas/IP0.log
rclone copy /home/pi/odas/IP0.log RaspberryPi:/ODAS
