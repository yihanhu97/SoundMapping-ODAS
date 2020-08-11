## SYSTEM UPDATE


### odaslive
1. Added folder for raw recordings`/home/pi/odas/recordings/raw` for future storage.

### recording v2
1. Skipped `matrix-odas` program as it is not needed. 
2. Added code that renames raw recordings once they are available.
3. Takes array index as an input and automatically changes files names based on each device.

### crontab
1. Recording program will not start at boot.

### bash scripts
1. A bash script will be run at user's terminal to start the recording program through ssh.

### TODO:

1. Update watchdog program, `file.monitoring.py` so that:
   - Modify watchdog program to avoid bugs
   - Monitors any ODAS `defunct` processes, reboot the device once a `defunct` process is found
   - Monitors memory usage
   - Monitors CPU usage
