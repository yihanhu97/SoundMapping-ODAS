#!/bin/bash
find /home/pi/odas/recordings -mmin +15 -exec rm {} \;
