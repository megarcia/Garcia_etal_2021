"""
Python script "map_wrf_io_T_wind_2-panel.py"
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
    #
    parallels = np.arange(30., 60., 1.)
    bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=14)
    meridians = np.arange(270., 360., 1.)
    bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=14)
    return bmap


def plot_upa_windspeed_map(U, V, title):
    """generate map using matplotlib Basemap module"""
    bmap  = set_up_basemap()
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
                                       levels=levels, cmap=get_cmap('Blues'))
    cbar = plt.colorbar(windspeed_contours, pad=0.02, shrink=0.9)
    labels = np.arange(0, 25, 3)
    cbar.ax.set_yticks(labels)
    cbar.ax.set_yticklabels(labels=labels, fontsize=14)
    cbar.ax.set_ylabel('wind speed [m/s]', fontsize=14)
    #
    # draw wind barbs
    interval = 10
    bmap.barbs(x[::interval, ::interval], y[::interval, ::interval],
               to_np(U[::interval, ::interval]),
               to_np(V[::interval, ::interval]), length=4)
    #
    plt.title(title, fontsize=14)
    return


def plot_sfc_T_wind_map(T2, U10, V10, title):
    """generate map using matplotlib Basemap module"""
    bmap = set_up_basemap()
    #
    lats, lons = latlon_coords(T2)
    x, y = bmap(to_np(lons), to_np(lats))
    #
    # smooth the T2 variable
    spatial_range = 3
    smooth_T2 = smooth2d(T2, spatial_range)
    #
    # draw T2 with filled contours
    levels = np.arange(4, 35)
    T2_contours = bmap.contourf(x, y, to_np(smooth_T2),
                                levels=levels, cmap=get_cmap('plasma'))
    cbar = plt.colorbar(T2_contours, pad=0.02, shrink=0.9)
    labels = np.arange(4, 35, 3)
    cbar.ax.set_yticks(labels)
    cbar.ax.set_yticklabels(labels=labels, fontsize=14)
    cbar.ax.set_ylabel(r'$T_{sfc}$ [$^{\circ}$C]', fontsize=14)
    #
    # draw wind barbs
    interval = 10
    bmap.barbs(x[::interval, ::interval], y[::interval, ::interval],
               to_np(U10[::interval, ::interval]),
               to_np(V10[::interval, ::interval]), length=4)
    #
    plt.title(title, fontsize=14)
    return


print()
sim_date = sys.argv[1]
path = '../Data/%s/WRF' % sim_date
ncfnames = sorted(glob('%s/*.nc' % path))
print('found %d files' % len(ncfnames))
print()
#
for ncfname in ncfnames:
    fig = plt.figure(figsize=(8, 14))
    #
    grid_num = int(ncfname.split('/')[-1].split('.')[0].split('_')[2][-1:])
    date_str = ncfname.split('/')[-1].split('.')[0].split('_')[3]
    time_str = ncfname.split('/')[-1].split('.')[0].split('_')[4][:-3]
    #
    ncfile = Dataset(ncfname, 'r')
    T2 = getvar(ncfile, 'T2')
    U10 = getvar(ncfile, 'u10_e')
    V10 = getvar(ncfile, 'v10_e')
    P = getvar(ncfile, 'pressure')
    U = getvar(ncfile, 'ue_unstaggered')
    V = getvar(ncfile, 've_unstaggered')
    #
    fig.add_subplot(2, 1, 1)
    prs = 900
    print('plotting %d hPa T/wind for %s' % (prs, ncfname))
    U_prs = interplevel(U, P, prs)
    V_prs = interplevel(V, P, prs)
    title = 'WRF-NARR grid %d %d hPa wind speed at %s %s UTC' % (grid_num, prs, date_str, time_str)
    plot_upa_windspeed_map(U_prs, V_prs, title)
    #
    fig.add_subplot(2, 1, 2)
    print('plotting surface T/wind for %s' % ncfname)
    title = 'WRF-NARR grid %d surface T + winds at %s %s UTC' % (grid_num, date_str, time_str)
    plot_sfc_T_wind_map(T2, U10, V10, title)
    #
    plt.tight_layout()
    fname = 'WRF_d%s_%s_%s_sfc_T_wind_900hPa_windspeed.png' % (str(grid_num).zfill(2), date_str, time_str)
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    print('- saved %s' % fname)
    plt.close()
    #
    print()

# end map_wrf_io_T_wind_2-panel.py
