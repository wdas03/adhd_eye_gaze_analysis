import pandas as pd
import numpy as np
import pickle

# Loading and storing pickle objects
def load_pickle(filename):
    var = pickle.load(open(filename, 'rb'))
    print('Loaded data from:', filename)
    return var

def store_pickle(var, filename):
    pickle.dump(var, open(filename, 'wb'), protocol=4)
    print('Stored data in:', filename)

def load_raw_data(subject_num):
    data_dir = 'adhd_eye_movement_data/'
    raw_data_dir = data_dir + 'raw_data/'
    user_info_df = pd.read_csv(data_dir + 'user_info.csv')

    user_info_df_subj = user_info_df['Subject']
    data = pd.DataFrame()

    # If off-ADHD/on-ADHD subject:
    if user_info_df_subj.value_counts()[subject_num] == 2:
        data = pd.read_csv("{}/subject_{}_off_ADHD.csv".format(raw_data_dir, subject_num))
    elif user_info_df_subj.value_counts()[subject_num] == 1:
        group = user_info_df.iloc[user_info_df.index[user_info_df['Subject'] == subject_num][0]]['Group']

        if group == 'off-ADHD':
            data = pd.read_csv("{}/subject_{}_off_ADHD.csv".format(raw_data_dir, subject_num))
        elif group == 'Ctrl':
            data = pd.read_csv("{}/subject_{}_Ctrl.csv".format(raw_data_dir, subject_num))
    else:
        return -1

    data = data.dropna(subset=['Time']).set_index('Time')
    data.index = data.index.astype(int)
    
    return data

def extract_trials(raw_data):
    trials = []
    for idx, row in raw_data[raw_data['Events'] == 7].iterrows():
        # Find start of trial
        start_interval = raw_data.loc[idx-5250:idx-4250]
        end_interval = raw_data.loc[idx:idx+4000]
        
        start_idx = idx - 4750
        if 1 in start_interval['Events'].values:
            assert start_interval['Events'].value_counts()[1] == 1

            start_idx = start_interval.index[start_interval['Events'] == 1].to_list()[0]
        elif 2 in start_interval['Events'].values:
            assert start_interval['Events'].value_counts()[2] == 1

            start_idx = start_interval.index[start_interval['Events'] == 2].to_list()[0]
        
        trials.append(raw_data.loc[start_idx:start_idx+7999].to_numpy())
    
    return trials