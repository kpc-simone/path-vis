# extract_path_timeseries_features.py

from tkinter.filedialog import askdirectory,askopenfilename
import pandas as pd
import argparse
import sys,os

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

parser = argparse.ArgumentParser()
parser.add_argument( '--feature', type = str, default = 'c-speed' )
# options: x-velocity, y-velocity, speed, acceleration
# TODO: heading error, shelter distance, in danger zone

parser.add_argument( '--align-to', type = str, default = 'shadowON-rel' )
parser.add_argument( '--time-col-name', type = str, default = 'time' )
# TODO: pick from options in the spreadsheet: shadowON-abs, beam-break-rel,

### NOT IMPLEMENTED ###
# parser.add_argument( '--shadow-dur', type = float, default = 8.0 )
# parser.add_argument( '--include-shadow-pre-time', type = bool, default = False )
# parser.add_argument( '--include-shadow-post-time', type = bool, default = False )

# constrain export if desired
# parser.add_argument( '--trial', type = str, default = 'all' )
# parser.add_argument( '--phenotype', type = str, default = 'all' )
# parser.add_argument( '--outcome', type = str, default = 'all' )

if __name__ == '__main__':
    args = parser.parse_args()
    
    if args.align_to == 'shadowON-rel':
        t0 = 0.
    
    path_files = [ f for f in os.listdir(paths_dir) if '.csv' in f ]
    
    df_out = pd.DataFrame( )
    for r,row in ecdf.iterrows():
        animal = row['animal']
        trial = row['trial']
        print(animal,trial)
        
        phenotype = row['phenotype']
        outcome = row['outcome']
        
        colstr = f'{phenotype}-{animal}-t{trial}-{outcome}'
        
        try:
            path_file = [ f for f in path_files if f'-t{trial}-' in f and f'-{animal}-' in f ][0]
            trdf = pd.read_csv( os.path.join(paths_dir,path_file), index_col = 0 )
            trdf = trdf[trdf['time-aligned'] > t0].reset_index( drop = True )
            
            if r == 0:
                df_out['time'] = trdf[args.time_col_name]
            
            df_out[colstr] = trdf[args.feature]
            
            print(df_out.head())
        except:
            print(f'WARNING: No path for trial {trial}, animal {animal}')
            
    df.to_csv(  )