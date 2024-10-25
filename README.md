# path-vis: Visualization tools for the path annotator

This is a companion repository containing a collection of visualization scripts for working with data from the the path-annotator tool.

Scripts Included:

- [x] Plot overlay of paths (completed)
	- [x] Optionally exclude pre-/post-shadow annotations
- [x] Align timeseries features to arbitrary time point (completed)
	- [x] Low-level timeseries features: position, speed, acceleration
	- [x] Export aligned data to csv
	- [x] High-level timeseries features:
		- [x] Shelter heading error (heading-error)
		- [x] Shelter distance (sh-dist)
		- [x] In danger zone (in-danger-zone)
- [x] Extract summary features from paths
- [ ] Advanced visualizations (planned)
	- [ ] Heading error histograms
	- [ ] Heatmaps
	
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


### 2. Align timeseries data to an experimental time point
```
python extract_path_timeseries_features.py --feature c-speed --align-to beam-break-rel --outcome escape
```
Will plot the speed of the centroid object over time, aligned to beam-break time, for all trials associated with an escape.

![](https://github.com/kpc-simone/path-vis/blob/main/docs/c-speed-alignedto_beam-break-rel_all-trial_all-outcome_escape.png)

