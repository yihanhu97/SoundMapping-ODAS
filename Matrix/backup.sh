#! /bin/bash

rclone copy /home/pi/odas/recordings/SST RaspberryPi:/ODAS/logs0/SST
rclone copy /home/pi/odas/recordings/SSL RaspberryPi:/ODAS/logs0/SSL
rclone copy /home/pi/odas/recordings/separated RaspberryPi:/ODAS/recordings0/separated
rclone copy /home/pi/odas/recordings/postfiltered RaspberryPi:/ODAS/recordings0/postfiltered
