from tkinter.filedialog import askopenfilename,askdirectory, asksaveasfile
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np
import sys,os
import math

import argparse


# todo - user selectable color map

#plt.rcParams['dpi'] = 300
cmap = plt.cm.jet.copy()

parser = argparse.ArgumentParser()
parser.add_argument('--FPS', default = 30, type = int)
parser.add_argument('--outcome_col', default = 'outcome', type = str )
parser.add_argument('--run_abs_col', default = 'beam-break-rel', type = str)
parser.add_argument('--beam_ypos', default = 0.3, type = float)

if __name__ == '__main__':

    args = parser.parse_args()
    FPS = args.FPS
    outcome_col = args.outcome_col
    run_abs_col = args.run_abs_col
    beam_ypos = args.beam_ypos
        
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
            traj_df = pd.read_csv(os.path.join(trajectories_folder,trajectory_file))
            fig,(ax,cax) = plt.subplots(1,2,figsize=(4.,5.),gridspec_kw={'width_ratios':[10,1]})
            counts, xedges, yedges, im = ax.hist2d(traj_df['c-xpos'],traj_df['c-ypos'],
                                bins = (12, 20), 
                                weights = np.ones((traj_df.shape[0],)) / FPS,
                                range = ((-.15,.15),(.0,.5)),
                                cmap = cmap,
                                vmin = 0., vmax = 1.,
                                # norm = colors.LogNorm(vmin = 0.0001, vmax = .1,)
                                )

            ax.set_ylim(0.5,0.0)
            ax.axhline(beam_ypos,color='white',linestyle='--')
            shelter = plt.Rectangle((-0.15, 0), 0.160, 0.120,fill=None,edgecolor='white', alpha=1.,zorder=20)
            ax.add_patch(shelter)   
            
            ax.set_xticks([])
            ax.set_yticks([])

            ticks = [0.,0.2,0.4,0.6,0.8,1.0]
            cbar = fig.colorbar(im, cax = cax, ticks=ticks,orientation='vertical',extend='max')  
            cbar.set_label('Seconds',va='top',ha='left',rotation=90,in_layout=True)
            cbar.ax.set_yticklabels( [int(t) for t in ticks] )
            # todo add title
            ax.set_title(f'{group}-{animal}-{trial}')
           
            fig.tight_layout()
            plt.show()