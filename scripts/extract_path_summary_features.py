from tkinter.filedialog import askopenfilename,askdirectory, asksaveasfile
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np
import sys,os
import math

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--FPS', default = 30, type = int)
parser.add_argument('--outcome_col', default = 'outcome', type = str )
parser.add_argument('--run_abs_col', default = 'beam-break-rel', type = str)

if __name__ == '__main__':

    args = parser.parse_args()
    FPS = args.FPS
    outcome_col = args.outcome_col
    run_abs_col = args.run_abs_col
        
    print('Select csv file with behavior and stimulus timings.')    
    ktdf = pd.read_csv(askopenfilename(title = "Select csv file with behavior and stimulus timings"))
    
    print('Select folder containing annotated paths.')
    trajectories_folder = askdirectory(title = "Select folder containing annotated paths")

    ktdf = ktdf[ktdf[outcome_col] != 'mistrial']

    data = []
    print('Extracting summary features from path data ...')
    for trajectory_file in os.listdir(trajectories_folder):
        
        trajectory_info = trajectory_file[:-4].split('-')
        group = trajectory_info[0].lower()
        animal = trajectory_info[2]
        trial = int(trajectory_info[4][1:])
        #print(trajectory_file, group, animal, trial)
        
        mask = (ktdf['group'] == group) & (ktdf['animal'] == animal) & (ktdf['trial'] == trial)
        trial_df = ktdf[ mask ].reset_index(drop=True)
        
        if len(trial_df) == 0:
            print(f'WARNING: entry missing for group {group}, animal {animal}, trial-{trial}')
        else:
            # extract features
            traj_df = pd.read_csv(os.path.join(trajectories_folder,trajectory_file))
            c_start = (traj_df['c-xpos'].iloc[0],traj_df['c-ypos'].iloc[0])
            c_end = (traj_df['c-xpos'].iloc[-1],traj_df['c-ypos'].iloc[-1])
            
            dist_e = np.sqrt( (c_end[0] - c_start[0])**2 + (c_end[1] - c_start[1])**2 )
            dist_t = traj_df['c-speed'].cumsum().max() / FPS
            
            run_latency = 'N/A'
            if trial_df[run_abs_col] is not None:
                run_latency = float(trial_df[run_abs_col]) - float(trial_df['shadowON-abs'])
                # TODO add a warning if marked as freeze but beam broken
            
            data.append({
            # basic identifying features
            'group'         : group,
            'animal'        : animal,
            'trial'         : trial,
            
            # additional identifying features
            'outcome'       : trial_df[outcome_col],
            
            # characterizing features
            'latency'       : run_latency,
            'c-start'       : c_start,
            'c-end'         : c_end,
            'dist-euclid'   : dist_e,
            'dist-total'    : dist_t,
            'curvature'     : dist_t / dist_e ,
            'speed-mean'    : traj_df['c-speed'].mean(),
            'speed-peak'    : traj_df['c-speed'].max(),
            'acc-peak'      : traj_df['c-scacc'].max(),
            'xacc-peak'      : traj_df['c-xacc'].max(),
            'yacc-peak'      : traj_df['c-yacc'].max(),
            })
    fdf = pd.DataFrame( data )
    print('Summary features extracted. Head/Tail of dataframe: ')
    print(fdf.head())    
    print(fdf.tail())    
    
    print('Select location to save output data.')
    fdf.to_csv(asksaveasfile(title='Select location to save output data.'))