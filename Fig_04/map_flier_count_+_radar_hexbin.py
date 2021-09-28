"""
Python script "map_flier_count_+_radar_hexbin.py"
by Matthew Garcia, Post-doctoral Research Associate
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2021 by Matthew Garcia
"""


import sys
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


bottom_lat, top_lat = 47.5, 49.5
left_lon, right_lon = -69.1, -66.0
radar_dBz_min, radar_dBz_max = -6, 24
radar_lat, radar_lon = 48.4783, -67.5822


def get_flier_locations(infname):
    fliers_df = pd.read_csv(infname, index_col=None)
    print('- found %d total fliers in plot area' % len(fliers_df))
    lats = np.array(fliers_df['lat'])
    lons = np.array(fliers_df['lon'])
    return lats, lons


def get_radar_field(infname):
    radar_df = pd.read_csv(infname, index_col=False)
    print('- found %d radar data rows' % len(radar_df))
    lats = np.array(radar_df['latitude'])
    lons = np.array(radar_df['longitude'])
    refl = np.array(radar_df['reflectivity'])
    refl_nan = np.where(refl < radar_dBz_min, np.nan, refl)
    refl_nan = np.where(refl_nan > radar_dBz_max, np.nan, refl_nan)
    return lats, lons, refl_nan


def set_up_basemap():
    mid_lat = (bottom_lat + top_lat) / 2.0
    mid_lon = (left_lon + right_lon) / 2.0
    bmap = Basemap(projection='tmerc', lon_0=mid_lon, lat_0=mid_lat,
                   lat_ts=mid_lat, llcrnrlat=bottom_lat, llcrnrlon=left_lon,
                   urcrnrlat=top_lat, urcrnrlon=right_lon, resolution='h',
                   area_thresh=500)
    bmap.drawcoastlines()
    bmap.drawstates()
    bmap.drawcountries()
    bmap.drawmapboundary()
    bmap.drawmapscale(lon=left_lon+0.4, lat=bottom_lat+0.2,
                      lon0=mid_lon, lat0=mid_lat, length=40.0,
                      barstyle='fancy')
    parallels = np.arange(30., 60., 1.)
    bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=12)
    meridians = np.arange(270., 360., 1.)
    bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=12)
    #
    x_min, y_min = bmap(left_lon, bottom_lat)
    x_max, y_max = bmap(right_lon, top_lat)
    extent = (x_min, x_max, y_min, y_max)
    return bmap, extent


def make_flier_count_hexbin_map(lats, lons, maxcount):
    bmap, extent = set_up_basemap()
    x, y = bmap(lons, lats)
    hbin = bmap.hexbin(x, y, mincnt=1, extent=extent, gridsize=100,
                       vmin=1, vmax=maxcount, cmap=get_cmap('viridis'))
    cbar = plt.colorbar(pad=0.02, shrink=0.75)
    count_clevs = cbar.get_ticks().astype(int)
    cbar.set_ticks(count_clevs)
    cbar.ax.set_yticklabels(count_clevs, fontsize=14, rotation=90, va='center')
    cbar.ax.set_ylabel('flier count', fontsize=14)
    return


def make_radar_field_hexbin_map(lats, lons, refl_nan):
    bmap, extent = set_up_basemap()
    x, y = bmap(lons, lats)
    hbin = bmap.hexbin(x, y, C=refl_nan, extent=extent, gridsize=100,
                       vmin=radar_dBz_min, vmax=radar_dBz_max, cmap=get_cmap('viridis'))
    radar_x, radar_y = bmap(radar_lon, radar_lat)
    plt.plot(radar_x, radar_y, marker='+', markersize=20, c='red')
    cbar = plt.colorbar(pad=0.02, shrink=0.75)
    count_clevs = cbar.get_ticks().astype(int)
    cbar.set_ticks(count_clevs)
    cbar.ax.set_yticklabels(count_clevs, fontsize=14, rotation=90, va='center')
    cbar.ax.set_ylabel('reflectivity [dBz]', fontsize=14)
    return


print()
sim_date = sys.argv[1]
radar_date = sys.argv[2]
radar_time = sys.argv[3]
# 
infname = '../Data/%s/Radar/XAM_fliers_hexbin_counts.csv' % sim_date
print('reading %s' % infname.split('/')[-1])
count_df = pd.read_csv(infname, index_col=None)
fliers_maxcount = max(count_df['maxcount'])
#
fliers_infname = '../Data/%s/Radar/%s_%s_XAM_fliers.csv' % \
    (sim_date, radar_date, str(radar_time).zfill(4))
print('reading %s' % fliers_infname.split('/')[-1])
flier_lats, flier_lons = get_flier_locations(fliers_infname)
#
radar_infname = '../Data/%s/Radar/cleaned_ref_ppi_xam_%s%s_1km.csv' % \
    (sim_date, radar_date, str(radar_time).zfill(4))
print('reading %s' % radar_infname.split('/')[-1])
radar_lats, radar_lons, radar_refl = get_radar_field(radar_infname)
#
fig = plt.figure(figsize=(16, 8))
print('plotting flier count')
fig.add_subplot(1, 2, 1)
make_flier_count_hexbin_map(flier_lats, flier_lons, fliers_maxcount)
#
print('plotting corresponding radar field')
fig.add_subplot(1, 2, 2)
make_radar_field_hexbin_map(radar_lats, radar_lons, radar_refl)
# 
plt.tight_layout()
fname = '%s_%s_XAM_fliers_+_radar.png' % (radar_date, str(radar_time).zfill(4))
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('- saved %s' % fname)
plt.close()

# end map_flier_count_+_radar_hexbin.py
