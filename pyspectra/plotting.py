import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import unittest 
from pyspectra.iospec import read_spec_ww3_native
from pyspectra.iospec import DIRNAME, LATNAME, LONNAME, FREQNAME, DIRNAME, SPECNAME


def add_wrap(theta, grid):
    """
    Adds extra columns to theta and the grid to make plot
    wrap across the zero angle

    theta -- array of angles
    grid -- spectral data
    """
    theta=np.concatenate((theta[-1:]-2*np.pi,theta))
    grid=np.concatenate((grid[-1:],grid),axis=0)
    return theta, grid

def new_axis(subplot=111):
    """
    Creates a new axis
    """
    ax = plt.subplot(subplot, polar=True)
    theta_labels = ['E', 'N-E', 'N', 'N-W', 'W', 'S-W', 'S', 'S-E']
    theta_angles = np.arange(0, 360, 45)
    ax.set_thetagrids(theta_angles, labels=theta_labels)
    return ax

def reorder(theta, grid):
    """
    Reorders angles in ascending order and rearanges grid
    apropriately

    theta -- array of angles
    grid -- spectral data
    """
    indsort = np.argsort(theta)
    theta = theta[indsort]
    grid = grid[indsort,]

    return theta, grid

def from_north(theta):
    """
    Converts angles from regular counterclockwise to clockwise
    from North

    theta -- array of angles
    """
    theta = 3*np.pi/2 - theta

    return theta

def contour(spec, timeindex, pntindex, ax=None, nlevs=20, base=1000,
            maxfreq='auto',ptype='radial',cmap=plt.get_cmap('viridis')):
    """
    Plots contour plot of spectral data

    ax -- axis on which to create plot
    theta -- array of angles
    timeindex -- time index
    pntindex -- point index
    R -- array of radii
    nlevs -- number of contour levels
    base -- base for logarithmic scale (higher plots more
                detail for low energy)
    maxfreq -- Maximum frequency to plot (auto uses maximum from data)
    """
    if not ax:
        ax = new_axis()
    grid = spec[SPECNAME].isel(site = pntindex, time = timeindex).values.transpose()

    theta = np.radians(spec[DIRNAME].values)
    R = spec[FREQNAME].values

    theta, grid = reorder(theta, grid)
    theta, grid = add_wrap(theta, grid)
    theta = np.pi/2 - theta

    r,t = np.meshgrid(R, theta)

    if ptype=='radial':
        clevs = np.logspace(0,1,num=nlevs, base=base)*np.max(grid)/base
        cs = ax.contour(t, r, grid, levels=clevs, colors='black', linewidths=0.5)

        # fixes bug where spectrum that was zero everywhere was causing a crash in
        # the log contour colour assignment
        if np.max(grid) > 0.0:
            cs = ax.contourf(t, r, grid, levels=clevs,norm=colors.LogNorm())
        else:
            cs = ax.contourf(t, r, grid, levels=clevs)
        if maxfreq == 'auto':
            maxfreq = np.max(R)
        #ax.set_lim(0,maxfreq)
        ax.set_rgrids(np.arange(0.1,maxfreq,0.1))

        if np.max(grid) > 0.0:
            cs = ax.contourf(t, r, grid, levels=clevs,norm=colors.LogNorm())
        else:
            cs = ax.contourf(t, r, grid, levels=clevs)
        if maxfreq == 'auto':
            maxfreq = np.max(R)
        #ax.set_lim(0,maxfreq)
        ax.set_rgrids(np.arange(0.1,maxfreq,0.1))

    if ptype=='pcolormesh':
        print 'hello'
        plt.pcolormesh(t,r,grid)

    return cs


class TestSpec(unittest.TestCase):

    def setUp(self):
        print("\n === Testing SWAN: 7 days, 1 site  ===")
        testfile = './tests/snative20141201T00Z_spec.nc'
        self.spec = read_spec_ww3_native(testfile)

    def test_plot(self):
        contour(self.spec, 1, 1)
        plt.show()

if __name__ == "__main__":
    unittest.main()


