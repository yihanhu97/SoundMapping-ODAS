# CSE4223-ODAS
This repository is created to document any scripts that are made under the supervision of Prof. Yoav Freund and Prof. Peter Gerstoft in the process of creating a sound data processing and analyzing project

### TODO

- [ ] Match channels for each sound source within arrays
- [ ] Calibrate delays
- [ ] For each matched source, generate a data matrix with 18 features

### In Progress

#### *Blind Calibration*

To negate the mis-synchronization of the clocks, we can find the average delay between each pair of microphones (that record sources at the same time).  Let call the average delay between arrays i and j  - d(i,j) , given these estimated value we want to calibrate the clocks. Let ci be the delay between the clock of array i and some "standard" clock. then we have the approximate relations ci - cj ≈ d(i,j).   We don't have a "standard" clock, so instead we choose one of the active arrays (that overlaps with the others on many 8ms time slots) and set it's clock to be the standard. Wlog suppose that c1=0.  We can then find c2,c3,c4 by minimizing ∑i >j (d(i,j) - ci+cj)2

#### *Channel Matching*
Problems:
1. Audio leakage: one source is audiby present in two channels within the same array
2. Long pause: when one source is on pause for too long, tracking disappears. 
3. Precision of the cross correlation 

#### *Data Matrix*
Write a script that scans through hour csv file and sort each entry by time. Extract time information, coordinates, and so on. Populate the matrix which is designed to have 18 columns, indexed by time and sound source Id
