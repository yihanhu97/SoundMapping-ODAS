### ODAS SYSTEM UPDATE

Instead of rebooting every 5 minutes, use subprocess to let the process to intercept the kill signal and exit elegantly. `kill -2 ID` is equivalent to `ctrl+c`, which will let odaslive exit with memory freed.
