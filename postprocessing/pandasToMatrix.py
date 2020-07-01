
import pandas as pd
import numpy as np
import copy
import os

def source_matching_single(dfs):
    
    # we drop multiple entries with the same time and microphone number, since these are obvious duplicates
    df = dfs.drop_duplicates(subset=['Time In Seconds', 'Microphone Number'])

    master_list = []
    # call the first entry of the 'Time In Seconds' column 'start_time'
    start_time = df['Time In Seconds'][0]
    split = start_time + 0.0077
    
    # call the last entry of the 'Time In Seconds' column 'end_time'
    end_time = df['Time In Seconds'].iloc[-1]
    
    temp = df.iloc[0] # saving first entry of the data frame in temp
    
    # setting the coordinates of the first entry to None
    temp['X'] = None 
    temp['Y'] = None
    temp['Z'] = None
    temp['Microphone Number'] = None
    
    # Generating one copy of temp for each mic_array. The attributes apart from X,Y,Z and array_number are intact
    array_0 = temp
    array_1 = temp
    array_2 = temp
    array_3 = temp
    
    
    counter = 0 #?
    #Assuming only 1 channel for each array
    
    for row in df.iterrows():
        if row[1]['Time In Seconds'] >= split:
#             print('ok')
            data_point = [None] * 13           # list with 13 None values
            data_point[0] = array_0['X']
            data_point[1] = array_0['Y']
            data_point[2] = array_0['Z']
            data_point[3] = array_1['X']
            data_point[4] = array_1['Y']
            data_point[5] = array_1['Z']
            data_point[6] = array_2['X']
            data_point[7] = array_2['Y']
            data_point[8] = array_2['Z']
            data_point[9] = array_3['X']
            data_point[10] = array_3['Y']
            data_point[11] = array_3['Z']
            data_point[12] = split - .0077
            
            if data_point[0] != None  or data_point[3] != None or  data_point[6] != None or data_point[9] != None:
#                 print('hey')
#                 print(data_point)
                master_list.append(data_point)
            filler = copy.copy(row[1])
            filler['X'] = None
            filler['Y'] = None
            filler['Z'] = None
            array_0 = filler
            array_1 = filler
            array_2 = filler
            array_3 = filler
            
            split = row[1]['Time In Seconds'] + 0.0077

            
                
        if row[1]['Microphone Number'] == 0:
            array_0 = row[1]
            
        elif row[1]['Microphone Number'] == 1:
            array_1 = row[1]
            
        elif row[1]['Microphone Number'] == 2:
            array_2 = row[1]

        else:
            array_3 = row[1]
#     print(master_list) # master_list is being formed correctly
    return master_list


def non_contiguous_hours_extractor(date, path):
    """Returns an integer list of all hours for which a .csv exists. The path needs to have only hh.csv files"""
    list_dir = os.listdir(path)
    list_dir_nums = []
    for i in list_dir:
        list_dir_nums.append(int(i[:-4]))
    list_dir_nums.sort()
    return list_dir_nums

def main(date, starting_hour=1, num_hours=1, multiple_sources=False):
    """ Given the path to the date folder, this function processes combined .csv files on the ODAS google drive folder
    and gives the corresponding matrix as the output."""
    
    # which .csv file to process? -> the one given in the date parameter
    date_path_combined = '/home/ardelalegre/google-drive/ODAS/dataframes/combined/'+ date
    
    # in the date folder, combined .csv files are arranged according to the hour when they were recorded
    
    # we have observed that .csv files are not present for every hour, so right now, we will process
    # the .csv file for every hour instead of doing so for a subset of hours.
    
    # earlier, Ardel had written a main function with additional parameters starting_hour and num_hours.
    # We are keeping the additional parameters but they do not affect the code as of now.
    # Below is his code we are temporarily commenting out.
    
    
    matricies = []
    
    # Ardel's code begins
#     ending_hour = starting_hour + num_hours
#     if(ending_hour >= 25):
#         print("Hours must end before end of day.")
#         return
    # Ardel's code ends
    
    
    # right now, we are just listing all the hours for which a combined .csv exists.
    # non_contiguous_hours returns a list of integers corresponding to such hours
    hours_ints = non_contiguous_hours_extractor(date,date_path_combined)
    
    
    # we convert the list of ints to a list of strings that exactly match the hour file names
    # we store the list in 'hours'
    hours = []
    
    for i in hours_ints:
        if(i > 9):
            hours.append(str(i))
        else:
            hours.append('0' + str(i))

    # each hour directory contains one combined .csv file with the path
    # "/home/ardelalegre/google-drive/ODAS/dataframes/combined/yyyy-mm-dd/hh.csv"
    # In the following code, we read each file in a date directory and pass it to 'source_matching_single()'
    
    if(hours == []):
        print("There are no combinded .csv files to process into a matrix.")
        return []
    
    for hour in hours:
        df = pd.read_csv(date_path_combined+'/' + str(hour) + '.csv')
        if(multiple_sources):
            pass
        else:
#             print(df)
            temp = source_matching_single(df) # earlier convert_single
#             print(temp)
#         try:
        # temp is a list of lists. If we loop through each element and convert it into an nparray
        temp_np_arr = np.asarray([np.asarray(i) for i in temp])
        matricies.append(temp)
#         except:
#             print("Too many hours")
    return matricies


date = '2019-09-14'
test_matrix = main('2019-09-14')
