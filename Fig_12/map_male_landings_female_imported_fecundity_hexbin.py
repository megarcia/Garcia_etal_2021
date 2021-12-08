"""
Python script "map_male_landings_female_imported_fecundity_hexbin.py"
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
bmap.drawmapscale(lon=left_lon+1.25, lat=top_lat-0.5, lon0=mid_lon, lat0=mid_lat, length=200.0,
                  barstyle='fancy', fillcolor1='w', fillcolor2='k', fontsize=16)
parallels = np.arange(30., 60., 1.)
bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=16)
meridians = np.arange(270., 360., 1.)
bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=16)
#
path = '../Data/%s/PyATM/landing_locs' % sim_date
infnames = sorted(glob('%s/landing_locs_*.csv' % path))
print('found %d landing location files' % len(infnames))
#
infname = infnames[0]
print('reading locations from %s' % infname)
locations_df = pd.read_csv(infname, index_col=False, low_memory=False)
for infname in infnames[1:]:
    print('reading locations from %s' % infname)
    temp_df = pd.read_csv(infname, index_col=False, low_memory=False)
    locations_df = pd.concat([locations_df, temp_df], axis=0)
print('found %d total data rows' % len(locations_df))
#
locations_male_df = locations_df[locations_df['sex'] == 0]
print('filtered to %d male data rows' % len(locations_male_df))
locations_female_df = locations_df[locations_df['sex'] == 1]
print('filtered to %d female data rows' % len(locations_female_df))
#
print('plotting male landings by location as gray areas')
lons_male = np.array(locations_male_df['longitude'])
lats_male = np.array(locations_male_df['latitude'])
x, y = bmap(lons_male, lats_male)
x_min, y_min = bmap(left_lon, bottom_lat)
x_max, y_max = bmap(right_lon, top_lat)    
hbin_m = bmap.hexbin(x, y, extent=(x_min, x_max, y_min, y_max), gridsize=100,
                     mincnt=1, vmin=1, vmax=100, cmap=get_cmap('Greys'))
counts = hbin_m.get_array()
hbin_m.set_array(np.where(counts > 0, 50, 0))
#
print('plotting female imported fecundity by location as color areas')
lons_female = np.array(locations_female_df['longitude'])
lats_female = np.array(locations_female_df['latitude'])
eggs = np.array(locations_df['F'])
x, y = bmap(lons_female, lats_female)
hbin_f = bmap.hexbin(x, y, C=eggs, extent=(x_min, x_max, y_min, y_max), gridsize=100,
                     vmin=1, vmax=20000, reduce_C_function=np.sum, cmap=get_cmap('viridis'))
cbar = plt.colorbar(pad=0.02, shrink=0.7)
count_clevs = [4000, 8000, 12000, 16000, 20000]
cbar.set_ticks(count_clevs)
cbar.ax.set_yticklabels(count_clevs, rotation=90, va='center', fontsize=16)
cbar.ax.set_ylabel('imported fecundity count', fontsize=16)
#
plt.tight_layout()
fname = '%s_male_landings_female_imported_fecundity_map.png' % sim_date
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('- saved %s' % fname)
plt.close()

# end map_male_landings_female_imported_fecundity_hexbin.py
