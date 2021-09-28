"""
Python script "map_oviposition_hexbin.py"
by Matthew Garcia, Post-doctoral Research Associate
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2021 by Matthew Garcia
"""


import sys
from glob import glob
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


print()
sim_date = sys.argv[1]
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
path = '../Data/%s/PyATM/egg_deposition' % sim_date
infnames = sorted(glob('%s/egg_deposition_*.csv' % path))
print('found %d egg deposition location files' % len(infnames))
#
infname = infnames[0]
print('reading locations from %s' % infname)
locations_df = pd.read_csv(infname, index_col=False, low_memory=False)
for infname in infnames[1:]:
    print('reading locations from %s' % infname)
    temp_df = pd.read_csv(infname, index_col=False, low_memory=False)
    locations_df = pd.concat([locations_df, temp_df], axis=0)
print('found %d data rows' % len(locations_df))
#
lons = np.array(locations_df['longitude'])
lats = np.array(locations_df['latitude'])
eggs = np.array(locations_df['n_eggs'])
#
print('plotting egg deposition counts by location')
x, y = bmap(lons, lats)
x_min, y_min = bmap(left_lon, bottom_lat)
x_max, y_max = bmap(right_lon, top_lat)
hbin = bmap.hexbin(x, y, C=eggs, extent=(x_min, x_max, y_min, y_max), gridsize=100,
                   vmin=1, vmax=6E5, reduce_C_function=np.sum, cmap=get_cmap('viridis'))
cbar = plt.colorbar(pad=0.02, shrink=0.75)
count_clevs = cbar.get_ticks()
cbar.set_ticks(count_clevs)
count_clevs = ['{:.0e}'.format(x) for x in count_clevs]
cbar.ax.set_yticklabels(count_clevs, rotation=90, va='center', fontsize=13)
cbar.ax.set_ylabel('egg deposition count', fontsize=14)
#
plt.tight_layout()
fname = '%s_egg_deposition_map.png' % sim_date
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('- saved %s' % fname)
plt.close()

# end map_oviposition_hexbin.py
