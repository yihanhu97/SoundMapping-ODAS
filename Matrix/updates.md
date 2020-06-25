## SYSTEM UPDATE


### odaslive
1. Included sound source localization data
2. Changed file path.
   - `/home/pi/odas/recordings/SSL/SSL.log`
   - `/home/pi/odas/recordings/SST/SST.log`
   - `/home/pi/odas/recordings/separated/separated.raw`
   - `/home/pi/odas/recordings/postfiltered/postfiltered.raw`

### recording v2
Instead of rebooting every 5 minutes, use subprocess to let the process to intercept the kill signal and exit elegantly. `kill -2 ID` is equivalent to `ctrl+c`, which will let odaslive exit with memory freed.
1. Renamed `system.monitoring.py` to `recording.py`
2. Changed `subprocess.kill()` to `subprocess.send_signal(signal.SIGINT)`.
3. Adjusted paths based on new odaslive code.
4. Added code to process `SSL.log`. `SSL.log` will be deleted if no useful data is found in `SST.log`. Recording start time and end time will be added to the file if it is not deleted. 

### watchdog v1
Renamed `file.monitoring.py` to `watchdog.py`.

### crontab
Changed crontab so that all bash scripts and commands are running with user pi permission instead of root. 

### bash scripts
1. Created a bash script that will clean up all remaining files in the recordings folder at reboot.
2. Created a bash script `IPUpload.sh` that publishes private IP address to google drive at reboot. 

### TODO:
1. Update `IPUpload.sh` so that it detects IP address change
2. Update watchdog program, `file.monitoring.py` so that:
   - Monitors any ODAS `defunct` processes, reboot the device once a `defunct` process is found
   - Monitors memory usage
   - Monitors CPU usage
