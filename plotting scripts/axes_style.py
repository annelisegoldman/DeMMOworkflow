## Contains useful functions for setting axes styling, axes height, and enabling symlog plots

from matplotlib.pyplot import rc
import numpy as np
from matplotlib.ticker import Locator

## Specify fonts and tick sizes

def set_axes_style():
    font = 'Arial'
    rc('font',**{'family':'sans-serif','sans-serif':[font]})
    rc('ytick',**{'major.size': 5})
    rc('ytick',**{'minor.size': 2.5})
    rc('xtick',**{'major.size': 5})
    rc('ytick',**{'labelsize': 10})
    rc('xtick',**{'labelsize': 10})
    rc('axes',**{'labelsize': 10})
    rc('svg', **{'fonttype': 'none'})
    rc('mathtext', **{'default' : 'regular'}) #change latex font to regular font

## Set axes height

def set_axes_height(ax, h):
    fig = ax.figure
    aw, ah = np.diff(ax.transAxes.transform([(0, 0), (1, 1)]), axis=0)[0]
    fw, fh = fig.get_size_inches()
    dpi = fig.get_dpi()
    scale = h / (ah / dpi)
    fig.set_size_inches(fw*scale, fh*scale, forward=True)

## Enable symlog plots
## requires import:

class MinorSymLogLocator(Locator):
    """
    Dynamically find minor tick positions based on the positions of
    major ticks for a symlog scaling.
    """

    def __init__(self, linthresh):
        """
        Ticks will be placed between the major ticks.
        The placement is linear for x between -linthresh and linthresh,
        otherwise its logarithmically
        """
        self.linthresh = linthresh

    def __call__(self):
        'Return the locations of the ticks'
        majorlocs = self.axis.get_majorticklocs()

        # iterate through minor locs
        minorlocs = []

        # handle the lowest part
        for i in range(1, len(majorlocs)):
            majorstep = majorlocs[i] - majorlocs[i-1]
            if abs(majorlocs[i-1] + majorstep/2) < self.linthresh:
                ndivs = 10
            else:
                ndivs = 9
            minorstep = majorstep / ndivs
            locs = np.arange(majorlocs[i-1], majorlocs[i], minorstep)[1:]
            minorlocs.extend(locs)

        return self.raise_if_exceeds(np.array(minorlocs))

    def tick_values(self, vmin, vmax):
        raise NotImplementedError('Cannot get tick locations for a '
                                  '%s type.' % type(self))