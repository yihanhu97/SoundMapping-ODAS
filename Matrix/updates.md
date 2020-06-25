## SYSTEM UPDATE


### Odaslive
1. Included sound source localization data
2. Changed file path.
   - `/home/pi/odas/recordings/SSL/SSL.log`
   - `/home/pi/odas/recordings/SST/SST.log`
   - `/home/pi/odas/recordings/separated/separated.raw`
   - `/home/pi/odas/recordings/postfiltered/postfiltered.raw`

### system.monitoring v2
Instead of rebooting every 5 minutes, use subprocess to let the process to intercept the kill signal and exit elegantly. `kill -2 ID` is equivalent to `ctrl+c`, which will let odaslive exit with memory freed.
1. Changed `subprocess.kill()` to `subprocess.send_signal(signal.SIGINT)`.
2. Adjusted paths based on new odaslive code.
3. Added code to process `SSL.log`. `SSL.log` will be deleted if no useful data is found in `SST.log`. Recording start time and end time will be added to the file if it is not deleted. 

### IP address
Created a bash script `IPUpload.sh` that publishes private IP address to google drive at boot. 

### watchdog v1
Renamed `file.monitoring.py` to `watchdog.py`.

### TODO:
1. Update `IPUpload.sh` so that it detects IP address change
2. Update watchdog program, `file.monitoring.py` so that:
   - Monitors any ODAS `defunct` processes, reboot the device once a `defunct` process is found
   - Monitors memory usage
   - Monitors CPU usage
