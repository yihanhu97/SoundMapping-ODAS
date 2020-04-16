## <center> Data Combining Outline </center>
This outline is created to help put together all functions/scripts that were written to populate the final data frame. I will outline the general logic and each necessary step, as well as create some skeleton code to get started. The ultimate goal is to make the combining file run on machine without supervisino. The outline be updated everytime after each meeting. **Please check out your own branch and work separately**.  

**Note**: the following discussion will be broken down into two parts. Multi sources in long period (MS+LP) and single source in short period (SS+SP). To simplify the problem for now, the main discussion will focus on SS+SP, which will be gradually extended to MS+LP.   

=======================================================================================
### General Steps:
- [ ]  Sound source matching
- [ ]  Timestamp matching
- [ ]  Delay and significance calculation
- [ ]  Extract coordinates
- [ ]  Populate dataframe

=======================================================================================
### Current Goal:
Formulate data frame for 1 min recording from 1:05 pm - 1:15pm, on March 25th. Single stationary source.

=======================================================================================
#### Sound Source Matching
The biggest challenge for data combining is sound source matching. Each array has 4 beams/channels, with each channel corresponding to a different sound source. ODAS library is able to track and separate up to 4 different sources at the same time. Currently, we have seen two main problems: cross talk between channels within an array and reflection. The first problem happens when one sound source appears in multiple channels as a result of long silence or ODAS sound source tracking (SST) algorithm failure. The second problem happens when the sound source is too close to a smooth surface and ODAS is picking up sound from direct path and reflection path, and therefore two channels have the same sound. 

Since each recording raw file is approximatly 5 mins long, there is a high chance that each channel within an array corresponds to more than one sound source. Calculating cross corrleation pairs over the entire 5 mins recording for sound source matching (SSM) will not be reliable. Therefore, to adapt to the volatile nature of ODAS SST algorithm, we will implement local SSM, using windowing method with no overlap. 

**MS+LP**: For 1 min recording starting at 1:05pm, given a window length of 1s and 4 arrays (16 channels). The number of cross correlation calculation is 60s/1s * (16 pick 2).

**SS+SP**: Assume only one stationary source is present and no reflection paths are recorded. Then each array should only have one valid channel corresponding to that source. Thus for 1 min recording starting at 1:05pm, given a window length of 1s and 4 arrays (4 valid channels). The number of necessary cross correlation calculation is 60s/1s * (4 pick 2).

**Challenge**:


#### Timestamp Matching
