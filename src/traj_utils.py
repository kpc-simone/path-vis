import matplotlib.pyplot as plt
import numpy as np

import matplotlib.cm as cm
from matplotlib.colors import Normalize

def get_derivatives( trdf, shelter_y = 0.12, shelter_w = 0.16, x_min = -0.15, danger_y = 0.3, plot_each = True ):
    shelter_xc = x_min + shelter_w/2
    shelter_xm = x_min + shelter_w
    
    FPS = 1 / trdf['time'].diff().mean()
    
    # shelter distance
    trdf['sh-dist'] = np.sqrt( (shelter_xc-trdf['c-xpos'] )**2 + (shelter_y-trdf['c-ypos'])**2 )
    trdf['sh-dist'] = trdf['sh-dist'].where( (trdf['c-xpos']>shelter_xm) | (trdf['c-ypos']>shelter_y), other = 0.)
    
    # heading error
    trdf['dy'] = trdf['n-ypos'] - trdf['t-ypos']  
    trdf['dx'] = trdf['n-xpos'] - trdf['t-xpos']
    trdf['dy-ideal'] = shelter_y - trdf['c-ypos']
    trdf['dx-ideal'] = shelter_xc - trdf['c-xpos']    
    trdf['heading'] = np.arctan2(trdf['dy'],trdf['dx']) #+ 3.14
    trdf['heading-ideal'] = np.arctan2(trdf['dy-ideal'],trdf['dx-ideal'])
    trdf['heading-error'] = trdf['heading-ideal'] - trdf['heading']
    # wrapping
    trdf['heading-error'] = trdf['heading-error'].where( trdf['heading-error'] < np.pi, other = 2*np.pi - trdf['heading-error'] )
    trdf['heading-error'] = trdf['heading-error'].where( trdf['heading-error'] > -np.pi, other = trdf['heading-error'] + 2*np.pi)
    
    trdf['heading-error'] = trdf['heading-error'].where( trdf['sh-dist'] > 0., other = 0. )
    
    trdf['in-danger-zone'] = trdf['c-ypos'] > danger_y
    
    if plot_each == True:
        fig,axs = plt.subplots(1,3,figsize=(12.,5.),gridspec_kw={'width_ratios':[3,3,6]})

        cmap = cm.bwr
        norm = Normalize( vmin = -np.pi, vmax = np.pi )
        axs[0].quiver( trdf['c-xpos'],trdf['c-ypos'], trdf['dx'], trdf['dy'],
                        color = cmap(norm(trdf['heading-error']))
                        )
        axs[0].quiver( trdf['c-xpos'],trdf['c-ypos'], trdf['dx-ideal'], trdf['dy-ideal'] )   
        axs[0].set_title('Heading')
        
        axs[1].scatter(trdf['c-xpos'],trdf['c-ypos'],c = trdf['in-danger-zone'],s = trdf['sh-dist']*100,cmap='RdGy')
        axs[1].axhline(danger_y,color='k',linestyle='--')
        axs[1].set_title('Shelter distance / danger zone')
        
        axs[2].plot(trdf['time'],trdf['heading-error'],color='mediumturquoise',label='heading-error')
        axs[2].plot(trdf['time'],trdf['sh-dist'],color='dimgray',label='sh-dist')
        axs[2].plot(trdf['time'],trdf['in-danger-zone'],color='firebrick',label='in-danger-zone')
        axs[2].legend(loc='upper right',fancybox=False)
        axs[2].set_xlabel('Time (s)')
        
        axs[2].set_ylim(-np.pi,np.pi)
        axs[2].axhline(0,color='k',linestyle='--')
        axs[0].set_title('heading')     
        for ax in axs[:2].ravel():
            ax.set_ylim(0.,0.5)
            ax.set_xlim(-.15,.15)
            ax.scatter( -0.09,0.12,color='k',marker='+',s=50 )

        fig.tight_layout()
        plt.show()

    return trdf