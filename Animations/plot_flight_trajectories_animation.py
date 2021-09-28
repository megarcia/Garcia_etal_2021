# pylint: disable=C0103
"""
Python script "plot_flight_trajectories_animation.py"
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


bottom_lat, top_lat = 45.0, 51.0
mid_lat = (bottom_lat + top_lat) / 2.0
left_lon, right_lon = -73.0, -64.0
mid_lon = (left_lon + right_lon) / 2.0


def set_up_basemap():
    bmap = Basemap(projection='tmerc', lon_0=mid_lon, lat_0=mid_lat,
                   lat_ts=mid_lat, llcrnrlat=bottom_lat, llcrnrlon=left_lon,
                   urcrnrlat=top_lat, urcrnrlon=right_lon, resolution='h',
                   area_thresh=500)
    bmap.drawcoastlines()
    bmap.drawstates()
    bmap.drawcountries()
    bmap.drawmapboundary()
    #
    parallels = np.arange(30., 60., 1.)
    bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    meridians = np.arange(270., 360., 1.)
    bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)
    return bmap


def plot_topography(bmap, topography):
    '''plot topography from WRF, with colorbar'''
    wrf_lats, wrf_lons = latlon_coords(topography)
    lons, lats = bmap(wrf_lons, wrf_lats)
    bmap.contourf(lons, lats, topography, 48, cmap=get_cmap('terrain'))
    cbar = plt.colorbar(pad=0.02, shrink=0.75)
    labels = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(labels=labels, rotation=90, va='center', fontsize=8)
    cbar.ax.set_ylabel('surface elevation [m AMSL]', fontsize=10)
    return


def add_sbw_locations(locations, fname):
    '''read new file and add flier locations to record'''
    new_locs_df = pd.read_csv(fname, index_col=None)
    new_locs_df = new_locs_df.rename(columns = {'Unnamed: 0':'sbw_ID'})
    #
    # add the location of an SBW on the ground only if its previous location was in the air
    ground_df = new_locs_df[new_locs_df['alt_AGL'] == 0.0]
    if len(ground_df):
        sbw_ids = list(ground_df['sbw_ID'])
        lats = np.array(ground_df['lat'])
        lons = np.array(ground_df['lon'])
        alts = np.array(ground_df['alt_AGL'])
        for i, sbw_id in enumerate(sbw_ids):
            if locations[sbw_id][-1][2] > 0.0:
                locations[sbw_id].append((lats[i], lons[i], alts[i]))
    #
    # add the location of any SBW in the air
    fliers_df = new_locs_df[new_locs_df['alt_AGL'] > 0.0]
    if len(fliers_df):
        sbw_ids = list(fliers_df['sbw_ID'])
        lats = np.array(fliers_df['lat'])
        lons = np.array(fliers_df['lon'])
        alts = np.array(fliers_df['alt_AGL'])
        for i, sbw_id in enumerate(sbw_ids):
            locations[sbw_id].append((lats[i], lons[i], alts[i]))
    return locations


def plot_sbw_locations(bmap, locations, last_frame=False):
    '''plot flier locations and trajectories'''
    for sbw, locs in locations.items():
        nlocs = len(locs)
        if nlocs == 1:
            lat = locs[0][0]
            lon = locs[0][1]
            bmap.plot(lon, lat, '+', markersize=10, color='k', latlon=True)
        else:  # nlocs > 1
            lats = list()
            lons = list()
            alts = list()
            for loc in locs:
                lats.append(loc[0])
                lons.append(loc[1])
                alts.append(loc[2])
            bmap.plot(lons[0], lats[0], '+', markersize=10, color='k', latlon=True)
            if (alts[-1] == 0.0) or last_frame:
                bmap.plot(lons[-1], lats[-1], 'x', markersize=10, color='k', latlon=True)
            bmap.plot(lons, lats, linewidth=1, color='r', latlon=True)
    return


def generate_plot(topography, fname, locations, last_frame=False):
    '''generate plot of topography, SBW locations, and trajectories for a specific time'''
    plt.figure(figsize=(8, 8))
    bmap = set_up_basemap()
    plot_topography(bmap, topography)
    plot_sbw_locations(bmap, locations, last_frame)
    datetimestr = fname.split('/')[-1].split('_')[1].split('+')[0]
    datestr, timestr = datetimestr.split('T')
    title = '%s simulation: %s at %s UTC' % (sim_date, datestr, timestr[:-3])
    plt.title(title, fontsize=12)
    plt.tight_layout()
    outfname = '%s/%s_flight_trajectories_%s_%s.png' % (sim_date, sim_date, datestr, timestr[:-3])
    plt.savefig(outfname, dpi=300, bbox_inches='tight')
    print('- saved %s' % outfname)
    plt.close()
    return


print()
sim_date = sys.argv[1]
rep_num = str(int(sys.argv[2])).zfill(5)
#
# get topography from WRF
path = '../Data/%s/WRF' % sim_date
ncfnames = sorted(glob('%s/*.nc' % path))
print('reading WRF topography from %s' % ncfnames[0].split('/')[-1])
ncfile = Dataset(ncfnames[0], 'r')
topography = getvar(ncfile, 'HGT')
#
# get animation map times and file list
path = '../Data/%s/pyATM/WRF-NARR_d03_%s_simulation_%s_summary' % (sim_date, sim_date, rep_num)
locfnames = sorted(glob('%s/locs_*_%s.csv' % (path, rep_num)))
print('found %d simulation output times with SBW locations' % len(locfnames))
#
# get locations at initial time and set up dict structure
sbw_locations = dict()
fname = locfnames[0]
locs_df = pd.read_csv(fname, index_col=None)
locs_df = locs_df.rename(columns = {'Unnamed: 0':'sbw_ID'})
sbw_ids = list(locs_df['sbw_ID'])
lats = np.array(locs_df['lat'])
lons = np.array(locs_df['lon'])
alts = np.array(locs_df['alt_AGL'])
for i, sbw_id in enumerate(sbw_ids):
    sbw_locations[sbw_id] = [(lats[i], lons[i], alts[i])]
#
# plot initial locations
generate_plot(topography, fname, sbw_locations)
#
# plot trajectories
for fname in locfnames[1:]:
    sbw_locations = add_sbw_locations(sbw_locations, fname)
    generate_plot(topography, fname, sbw_locations)
generate_plot(topography, locfnames[-1], sbw_locations, last_frame=True)
#
print()

# end plot_flight_trajectories_animation.py
