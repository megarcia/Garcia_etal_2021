"""
Python script "map_wrf_io_T_wind_prs.py"
by Matthew Garcia, Post-doctoral Research Associate
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2021 by Matthew Garcia
basic structure borrowed from wrf-python documentation
"""


import sys
from glob import glob
import numpy as np
from netCDF4 import Dataset
from wrf import getvar, to_np, latlon_coords, smooth2d, interplevel
import matplotlib as mpl
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
mpl.use('Agg')
import matplotlib.pyplot as plt


bottom_lat, top_lat = 45.0, 51.0
mid_lat = (bottom_lat + top_lat) / 2.0
left_lon, right_lon = -73.0, -64.0
mid_lon = (left_lon + right_lon) / 2.0


def T_wind_map(T, U, V, fname):
    """generate map figure using matplotlib Basemap module"""
    fig = plt.figure(figsize=(8, 8))
    bmap = Basemap(projection='tmerc', lon_0=mid_lon,
                   lat_0=mid_lat, lat_ts=mid_lat,
                   llcrnrlat=bottom_lat, llcrnrlon=left_lon,
                   urcrnrlat=top_lat, urcrnrlon=right_lon,
                   resolution='h', area_thresh=500)
    bmap.drawcoastlines()
    bmap.drawstates()
    bmap.drawcountries()
    #
    lats, lons = latlon_coords(T)
    x, y = bmap(to_np(lons), to_np(lats))
    #
    # smooth the T variable
    spatial_range = 3
    smooth_T = smooth2d(T, spatial_range)
    #
    # draw T with filled contours
    levels = np.arange(4, 35)
    T_contours = bmap.contourf(x, y, to_np(smooth_T),
                               levels=levels, cmap=get_cmap('jet'))
    cbar = plt.colorbar(T_contours, pad=0.02, shrink=0.75)
    labels = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(labels=labels, fontsize=14)
    cbar.ax.set_ylabel(r'$T$ [$^{\circ}$C]', fontsize=14)
    #
    # draw wind barbs
    interval = 10
    bmap.barbs(x[::interval, ::interval], y[::interval, ::interval],
               to_np(U[::interval, ::interval]),
               to_np(V[::interval, ::interval]), length=4)
    #
    parallels = np.arange(30., 60., 1.)
    bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=12)
    meridians = np.arange(270., 360., 1.)
    bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=12)
    #
    plt.tight_layout()
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    print('- saved %s' % fname)
    plt.close()
    return


def windspeed_map(U, V, fname):
    """generate map figure using matplotlib Basemap module"""
    fig = plt.figure(figsize=(8, 8))
    bmap = Basemap(projection='tmerc', lon_0=mid_lon,
                   lat_0=mid_lat, lat_ts=mid_lat,
                   llcrnrlat=bottom_lat, llcrnrlon=left_lon,
                   urcrnrlat=top_lat, urcrnrlon=right_lon,
                   resolution='h', area_thresh=500)
    bmap.drawcoastlines()
    bmap.drawstates()
    bmap.drawcountries()
    #
    lats, lons = latlon_coords(U)
    x, y = bmap(to_np(lons), to_np(lats))
    #
    # generate and smooth the windspeed variable
    windspeed = np.sqrt(to_np(U)**2 + to_np(V)**2)
    spatial_range = 3
    smooth_windspeed = smooth2d(windspeed, spatial_range)
    #
    # draw windspeed with filled contours
    levels = np.arange(0, 25)
    windspeed_contours = bmap.contourf(x, y, to_np(smooth_windspeed),
                                       levels=levels, cmap=get_cmap('jet'))
    cbar = plt.colorbar(windspeed_contours, pad=0.02, shrink=0.75)
    labels = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(labels=labels, fontsize=14)
    cbar.ax.set_ylabel('wind speed [m/s]', fontsize=14)
    #
    # draw wind barbs
    interval = 10
    bmap.barbs(x[::interval, ::interval], y[::interval, ::interval],
               to_np(U[::interval, ::interval]),
               to_np(V[::interval, ::interval]), length=4)
    #
    parallels = np.arange(30., 60., 1.)
    bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=12)
    meridians = np.arange(270., 360., 1.)
    bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=12)
    #
    plt.tight_layout()
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    print('- saved %s' % fname)
    plt.close()
    return


print()
sim_date = sys.argv[1]
path = '../Data/%s/WRF' % sim_date
ncfnames = sorted(glob('%s/*.nc' % path))
print('found %d files' % len(ncfnames))
print()
#
prs = 900
for ncfname in ncfnames:
    print('plotting upper-air T/wind for %s at %d hPa' % (ncfname, prs))
    grid_num = int(ncfname.split('/')[-1].split('.')[0].split('_')[2][-1:])
    date_str = ncfname.split('/')[-1].split('.')[0].split('_')[3]
    time_str = ncfname.split('/')[-1].split('.')[0].split('_')[4][:-3]
    ncfile = Dataset(ncfname, 'r')    
    P = getvar(ncfile, 'pressure')
    T = getvar(ncfile, 'temperature')
    U = getvar(ncfile, 'ue_unstaggered')
    V = getvar(ncfile, 've_unstaggered')
    T_prs = interplevel(T, P, prs)
    U_prs = interplevel(U, P, prs)
    V_prs = interplevel(V, P, prs)
    fname = 'WRF_d%s_%s_%s_T_wind_%dhPa.png' % (str(grid_num).zfill(2), date_str, time_str, prs)
    T_wind_map(T_prs, U_prs, V_prs, fname)
    fname = 'WRF_d%s_%s_%s_windspeed_%dhPa.png' % (str(grid_num).zfill(2), date_str, time_str, prs)
    windspeed_map(U_prs, V_prs, fname)
    print()

# end map_wrf_io_T_wind_prs.py
