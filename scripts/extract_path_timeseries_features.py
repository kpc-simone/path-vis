# extract_path_timeseries_features.py

from tkinter.filedialog import askdirectory,askopenfilename

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import sys,os

sys.path.insert(0,'../src')
from traj_utils import *

'''
This script extracts a single timeseries feature from each path associated with an experiment, 
aligns that feature to a user-specified timepoint, and then merges the results into a new csv file.

Input data:
    Experimental conditions file, in CSV format.
    Folder containing only the desired path data files, in CSV format.

Arguments:
    --feature: the time series feature to extract from the path data. 
    This can be one of:
    'shadowON-rel'    : align to time = 0.
    OR the name of a column in the path data file.
    
    --align-to: the time point for alignment of the data. 
    This must be the name of a column in the experimental conditions (ec) file.

Returns:
    
    
'''

ecdf = pd.read_csv( askopenfilename( title = "Select experimental conditions and key timings file" ) )
paths_dir = askdirectory( title = "Select folder containing path data" )
out_dir = askdirectory( title = "Select folder to save the processed data" )

parser = argparse.ArgumentParser()
parser.add_argument( '--feature', type = str, default = 'c-speed' )
valid_features = ['n-xpos','n-ypos','t-xpos','c-xpos','c-ypos','c-xvel','c-yvel','c-xacc','c-speed','c-scacc','a-pos','a-vel','heading-error','sh-dist','danger-zone']

parser.add_argument( '--align-to', type = str, default = 'shadowON-rel' )
valid_alignments = ['shadowON-rel','beam-break-rel']
# TODO: pick from options in the spreadsheet: shadowON-abs, beam-break-rel, etc

# customization
parser.add_argument( '--shadow-dur', type = float, default = 8.0 )
parser.add_argument( '--time-col-name', type = str, default = 'time' )

# constrain export if desired
parser.add_argument( '--trial', type = str, default = 'all' )
parser.add_argument( '--group', type = str, default = 'all' )
parser.add_argument( '--outcome', type = str, default = 'all' )

parser.add_argument( '--max-dur', type = float, default = 10.0 )
parser.add_argument( '--figure-format', type = str, default = 'pdf' )
parser.add_argument( '--plot-each', type = bool, default = True )

if __name__ == '__main__':
    args = parser.parse_args()
    assert args.feature in valid_features, f'ERROR: Requested feature {args.feature} is not available. Available features: {[f for f in valid_features]}'
    assert args.align_to in valid_alignments, f'ERROR: Requested alignment {args.align_to} is not available. Available alignments: {[f for f in valid_alignments]}'
    
    # slice and dice the data
    if args.group != 'all':
        ecdf = ecdf[ecdf['group'] == args.group ]
        print('slicing data')
    if args.trial != 'all':
        ecdf = ecdf[ecdf['trial'] == int(args.trial) ]
    if args.outcome != 'all':
        ecdf = ecdf[ecdf['outcome'] == args.outcome ]

    path_files = [ f for f in os.listdir(paths_dir) if '.csv' in f ]
    ts = pd.read_csv( os.path.join(paths_dir,path_files[0]), index_col = 0 )[args.time_col_name]
    
    fps = 1 / np.mean( ts.diff() )
    ts_common = np.linspace( -args.max_dur, args.max_dur, int(np.ceil( 2*args.max_dur * fps )), endpoint = True )
    
    df_out = pd.DataFrame( data = { 'time' : ts_common } )
    for r,row in ecdf.iterrows():
        animal = row['animal']
        trial = row['trial']
        group = row['group']
        outcome = row['outcome']
        print(animal,trial,group,outcome)
        
        colstr = f'{group}-{animal}-t{trial}-{outcome}'
        
        try:
            path_file = [ f for f in path_files if f'-t{trial}-' in f and f'-{animal}-' in f ][0]
            trdf = pd.read_csv( os.path.join(paths_dir,path_file), index_col = 0 )
            trdf = get_derivatives(trdf,plot_each = args.plot_each)
            
            if args.align_to == 'shadowON-rel':
                pass
            elif args.align_to == 'beam-break-rel':
                trdf[args.time_col_name] = trdf[args.time_col_name] - row['beam-break-rel']
                
            tpre = trdf[args.time_col_name].min()
            idx0 = np.argmin( [ np.abs( t - tpre ) for t in df_out['time'].values ] ) 
            idxs_new = np.arange(idx0,idx0+trdf.shape[0])
            trdf.index = idxs_new
            
            df_out[colstr] = np.nan
            df_out.loc[idxs_new,colstr] = trdf[args.feature]
            
        except:
            print(f'WARNING: Skipped path for trial {trial}, animal {animal}')
     
    fig,ax = plt.subplots(1,1, figsize=(6.,4.))
    ax.plot( df_out['time'], df_out.iloc[:,1:], color = 'silver', linewidth = 0.2 )
    ax.plot( df_out['time'], df_out.iloc[:,1:].mean(axis=1), color = 'dimgray' )
    ax.set_ylabel(args.feature)
    ax.set_xlabel( f'Time (s) aligned to {args.align_to}' )
    ax.axvline(0.,color='k',linestyle='--')
    
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
        
    fig.tight_layout()
    
    print('Figure saved in: figs')
    figname = f'{args.feature}-alignedto_{args.align_to}_{args.group}-trial_{args.trial}-outcome_{args.outcome}.{args.figure_format}'
    plt.savefig( os.path.join('../figs',figname), format = args.figure_format )
    plt.show()
    
    df_out.to_csv( os.path.join(out_dir,f'{args.feature}-alignedto_{args.align_to}_{args.group}-trial_{args.trial}-outcome_{args.outcome}.csv' ) )