import json
import re

filename = raw_input()

with open(filename, 'r') as f:
    text = f.read()
    # The find() method returns the lowest index of the substring if it is found in given string
    # Find the first left curly brace
    ind = text.find('{\n')
    # Delete initialization text
    body = text[ind:]
"""
+--------------------------------------------+
|    ODAS (Open embeddeD Audition System)    |
+--------------------------------------------+
| Author:  Francois Grondin                  |
| Email:   francois.grondin2@usherbrooke.ca  |
| Website: introlab.3it.usherbrooke.ca       |
| Version: 1.0                               |
+--------------------------------------------+
| + Initializing configurations...... [Done] |
| + Initializing objects............. [Done] |
| + Launch threads................... [Done] |
| + Threads running.................. {
"""        
# Use repex to store blocks of data into a list
data = re.split('(?<=})\n(?={)', body) 
# Delete the last block in the list
del data[-1]

# Set a flag for zero data log file
saveFlag = False

# Use Json to convert each data block string to a dictionary
for block in data:
    d = json.loads(block)
    # Obtain all id values from 4 entries
    idList = [line['id'] for line in d['src']]
    # Check the values of ids, if there is a none zero then break
    if not all(value == 0 for value in idList):
        saveFlag = True
        break
        
if saveFlag:
    print('useful\n')
else:
    print('not useful\n')
   
# create a new log file that is checked and cleaned
with open('/home/pi/odas/recordings/SST/cleaned.log', 'w') as f:
    if saveFlag:
        for item in data:
            f.write("%s\n" % item)
    else:
        f.write('SST log contains no useful data\n')
        
