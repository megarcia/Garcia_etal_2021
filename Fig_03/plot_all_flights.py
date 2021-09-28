# pylint: disable=C0103,C0412,C0413,R0914,R0915,R1711
"""
Python script "plot_all_flights.py"
by Matthew Garcia, Postdoctoral Research Associate
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2021 by Matthew Garcia
"""


import sys
from glob import glob
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from wrf import getvar, latlon_coords
import matplotlib as mpl
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
mpl.use('Agg')
import matplotlib.pyplot as plt


def get_trajectory(infname):
    """get trajectory from pyATM individual flier output file."""
    df = pd.read_csv(infname, index_col=None)
    lats = np.array(df['lat'])
    lons = np.array(df['lon'])
    alt_AGL = np.array(df['alt_AGL'])
    if np.any(alt_AGL > 0.0):
        idx1 = 0
        for idx, alt in enumerate(alt_AGL):
            if alt > 0.0:
                idx1 = idx - 1
                break
        idx2 = -1
        for idx in range(len(alt_AGL)-1, -1, -1):
            if alt_AGL[idx] > 0.0:
                idx2 = idx + 1
                break
        traj_lats = lats[idx1:idx2]
        traj_lons = lons[idx1:idx2]
    else:
        traj_lats = []
        traj_lons = []
    return traj_lats, traj_lons


print()
sim_date = sys.argv[1]
rep_num = sys.argv[2]
#
# setup map
bottom_lat, top_lat = 45.0, 51.0
mid_lat = (bottom_lat + top_lat) / 2.0
left_lon, right_lon = -73.0, -64.0
mid_lon = (left_lon + right_lon) / 2.0
#
plt.figure(figsize=(8, 8))
bmap = Basemap(projection='tmerc', lon_0=mid_lon, lat_0=mid_lat,
               lat_ts=mid_lat, llcrnrlat=bottom_lat, llcrnrlon=left_lon,
               urcrnrlat=top_lat, urcrnrlon=right_lon, resolution='h',
               area_thresh=500)
bmap.drawcoastlines()
bmap.drawstates()
bmap.drawcountries()
#
# draw map references
bmap.drawmapscale(lon=left_lon+0.75, lat=top_lat-0.5,
                  lon0=mid_lon, lat0=mid_lat, length=100.0,
                  barstyle='fancy')
parallels = np.arange(30., 60., 1.)
bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=12)
meridians = np.arange(270., 360., 1.)
bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=12)
#
# get topography from WRF
path = '../Data/%s/WRF' % sim_date
ncfnames = sorted(glob('%s/*.nc' % path))
print('reading WRF topography from %s' % ncfnames[0].split('/')[-1])
ncfile = Dataset(ncfnames[0], 'r')
topography = getvar(ncfile, 'HGT')
wrf_lats, wrf_lons = latlon_coords(topography)
lons, lats = bmap(wrf_lons, wrf_lats)
#
# plot topography from WRF
bmap.contourf(lons, lats, topography, 48, cmap=get_cmap('terrain'))
cbar = plt.colorbar(pad=0.02, shrink=0.75)
labels = cbar.ax.get_yticklabels()
cbar.ax.set_yticklabels(labels=labels, rotation=90, va='center', fontsize=14)
cbar.ax.set_ylabel('surface elevation [m AMSL]', fontsize=14)
print('- mapped WRF topography')
#
# plot flight trajectories from pyATM
path = '../Data/%s/pyATM/WRF-NARR_d03_%s_simulation_%s_output' % (sim_date, sim_date, str(rep_num).zfill(5))
infnames = sorted(glob('%s/*.csv' % path))
print('found %d Flier data files for %s simulation replicate %s' %
      (len(infnames), sim_date, str(rep_num).zfill(5)))
nflights = 0
for infname in infnames:
    traj_lats, traj_lons = get_trajectory(infname)
    npts = len(traj_lats)
    if npts > 2:
        bmap.plot(traj_lons[0], traj_lats[0], '+', markersize=10, color='k', latlon=True)
        bmap.plot(traj_lons[-1], traj_lats[-1], 'x', markersize=10, color='k', latlon=True)
        bmap.plot(traj_lons, traj_lats, linewidth=1, color='r', latlon=True)
        nflights += 1
print('- plotted %d flight trajectories' % nflights)
#
plt.tight_layout()
fname = '%s_flight_trajectories_default_replicate_%s.png' % (sim_date, str(rep_num).zfill(5))
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('- saved %s' % fname)
plt.close()

# end plot_all_flights.py
