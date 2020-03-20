# CSE4223-ODAS
This repository is created to document any scripts that are made under the supervision of Prof. Yoav Freund and Prof. Peter Gerstoft in the process of creating a sound data processing and analyzing project

Next Step 1: Correct the time difference between clocks on different arrays
To negate the mis-synchronization of the clocks, we can find the average delay between each pair of microphones (that record sources at the same time).  Let call the average delay between arrays i and j  - d(i,j) , given these estimated value we want to calibrate the clocks. Let ci be the delay between the clock of array i and some "standard" clock. then we have the approximate relations ci - cj ≈ d(i,j).   We don't have a "standard" clock, so instead we choose one of the active arrays (that overlaps with the others on many 8ms time slots) and set it's clock to be the standard. Wlog suppose that c1=0.  We can then find c2,c3,c4 by minimizing ∑i >j (d(i,j) - ci+cj)2
