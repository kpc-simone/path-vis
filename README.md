# Installation

Prerequisites: Anaconda

```
git clone https://github.com/kpc-simone/path-vis.git
cd path-vis
conda env create -f environment.yml --name path-vis-env
conda activate path-vis-env
```

# Usage Examples

The scripts folder contains tools for performing common processing steps and generating visualizations path data.
Detailed documentation for each script is given within the script itself. Here are some examples for working with the scripts.

### 1. Overlay paths associated with certain groups/trials/outcomes.
```
python plot_all_trial_paths_overlaid.py --outcome escape --trial 4 --group crh
```
Will plot all paths associated with the "crh" group, occuring in trial 4, and resulting in an escape. 

![](https://github.com/kpc-simone/path-vis/blob/main/docs/all-trial-paths-overlaid-group_crh-trial_4-outcome_escape.png)

Leave out optional arguments to include all categories for that feature. For example:
```
python plot_all_trial_paths_overlaid.py --trial 1
```
Will plot all paths elicited in trial 1, associated with any outcome and any group. 
