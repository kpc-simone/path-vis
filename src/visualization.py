# visualization.py
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import sys,os

arena = {
    'xmin'      : -0.15,
    'ymin'      : 0,
    'width'     : 0.3,
    'height'    : 0.5,
}

shelter = {
    'xmin'      : -0.15,
    'ymin'      : 0,
    'width'     : 0.160,
    'height'    : 0.120,
}


def draw_box(ax,bb):

    # a fancy box with round corners. pad=0.1
    box = mpatches.FancyBboxPatch((bb['xmin'], bb['ymin']),
                             abs(bb['width']), abs(bb['height']),
                             boxstyle="round,pad=0.01",
                             fc=(0.95, 0.95, 0.95),
                             ec=(0.25, 0.25, 0.25))
    ax.add_patch(box)    

behavior_colors = {
	'escape'	    : '#279edd',
    'panic'         : '#c97330',
    'attempt'       : '#c97330',    
    'freeze'	    : '#27c687',
	'no response'	: '#b3b3b3',
    'nr'            : '#b3b3b3',
    'mistrial'      : 'white',
	'rear'          : '#fde725',    
    'hide'          : '#675159',
}

def plot_trajectory(xs,ys,outcome,arenaSize):
    width,depth = arenaSize
    
    fig, axes = plt.subplots(1,1,squeeze=False,figsize=(3,5))
    
    if outcome in behavior_colors.keys():
        color_ = behavior_colors[outcome]
    else:
        color_ = 'dimgray'
    axes[0,0].plot(xs,ys,color=color_,linewidth=1.5,alpha=0.5)
    
    xmin = -width/2/1000
    xmax = (width-width/2)/1000
    ymin = 0
    ymax = depth/1000
    
    arena = {
    'xmin'      : xmin,
    'ymin'      : ymin,
    'width'     : width/1000,
    'height'    : depth/1000,
    }
    
    for ax in axes.ravel():
        draw_box(ax,arena)
        ax.set_xlim(xmin,xmax)
        ax.set_ylim(ymax,ymin)
        #shelter = plt.Rectangle((-0.150, 0), 0.160, 0.120,facecolor=behavior_colors['hide'], alpha=0.5)
        #ax.add_patch(shelter)
        ax.set_axis_off()    
    
    plt.show()