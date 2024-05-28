# plot_all_trial_paths_overlaid.py

from tkinter.filedialog import askdirectory,askopenfilename
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import sys,os

sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../src'))
from visualization import behavior_colors, draw_box, arena, shelter

'''
This script extracts a single timeseries feature from each path associated with an experiment, 
aligns that feature to a user-specified timepoint, and then merges the results into a new csv file.

Input data:
    Experimental conditions file, in CSV format.
    Folder containing only the desired path data files, in CSV format.

Arguments:
    --trial: the trial for which to plot the data. Defaults to all.
    --group: the group for which to plot the data. Defaults to all.
    --outcome: the outcome for which to plot the data. Defaults to all. 

Output:
    A figure (in the desired format) with paths overlaid corresponding to the selected data.
    
'''

ecdf = pd.read_csv( askopenfilename( title = "Select experimental conditions and key timings file" ) )
paths_dir = askdirectory( title = "Select folder containing path data" )

parser = argparse.ArgumentParser()

# select which data to focus on
# TODO: check validity of passed argument given the dataset
parser.add_argument( '--trial', type = str, default = 'all' )
parser.add_argument( '--group', type = str, default = 'all' )
parser.add_argument( '--outcome', type = str, default = 'all' )

# advanced options
parser.add_argument( '--shadow-dur', type = float, default = 8.0 )
parser.add_argument( '--time-col-name', type = str, default = 'time' )
parser.add_argument( '--include-shadow-pre-time', type = bool, default = False )
parser.add_argument( '--include-shadow-post-time', type = bool, default = False )
parser.add_argument( '--figure-format', type = str, default = 'pdf' )

if __name__ == '__main__':
    args = parser.parse_args()
    
    ti = 0.
    tf = args.shadow_dur
    
    # slice and dice the data
    if args.group != 'all':
        ecdf = ecdf[ecdf['group'] == args.group ]
    if args.trial != 'all':
        ecdf = ecdf[ecdf['trial'] == int(args.trial) ]
    if args.outcome != 'outcome':
        ecdf = ecdf[ecdf['outcome'] == args.outcome ]
        
    path_files = [ f for f in os.listdir(paths_dir) if '.csv' in f ]

    fig,ax = plt.subplots(1,1,figsize=(3.,5.))
    for r,row in ecdf.iterrows():
        animal = row['animal']
        trial = row['trial']
        group = row['group']
        outcome = row['outcome']
        
        colstr = f'{group}-{animal}-t{trial}-{outcome}'
        
        try:
            path_file = [ f for f in path_files if f'-t{trial}-' in f and f'-{animal}-' in f ][0]
            trdf = pd.read_csv( os.path.join(paths_dir,path_file), index_col = 0 )
            if args.include_shadow_pre_time == False:
                trdf = trdf[ trdf[args.time_col_name] > ti ]
            if args.include_shadow_post_time == False:
                trdf = trdf[ trdf[args.time_col_name] < tf ]
            ax.plot( trdf['c-xpos'], trdf['c-ypos'], color=behavior_colors[outcome] )
            
        except:
            print(f'WARNING: No path for trial {trial}, animal {animal}')
        
        draw_box(ax,arena)
        ax.set_xlim(-0.20,0.20)
        ax.set_ylim(0.55,-0.05)
        shelter_patch = plt.Rectangle((shelter['xmin'], shelter['ymin']), shelter['width'], shelter['height'],facecolor=behavior_colors['hide'], alpha=0.5)
        ax.add_patch(shelter_patch)
        ax.set_axis_off()    
    fig.tight_layout()

    ### SAVE THE FIGURE(S) ###
    print('Figure saved in: figs')
    figname = f'all-trial-paths-overlaid-group_{args.group}-trial_{args.trial}-outcome_{args.outcome}.{args.figure_format}'
    plt.savefig( os.path.join('../figs',figname), format = args.figure_format )
    plt.show()