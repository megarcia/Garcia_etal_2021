"""
Python script "map_wrf_io_T_wind_profile.py"
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
from wrf import getvar, to_np, latlon_coords, interp1d
import matplotlib as mpl
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
mpl.use('Agg')
import matplotlib.pyplot as plt


def find_loc_xy(ncfname, plat, plon):
    ncfile = Dataset(ncfname, 'r')
    T2 = getvar(ncfile, 'T2')
    xlats, xlons = latlon_coords(T2)
    lats = to_np(xlats)
    lons = to_np(xlons)
    lats_offset = plat - lats
    lons_offset = lons - plon
    dist_offset = np.sqrt(lats_offset**2 + lons_offset**2)
    shape = np.shape(dist_offset)
    y, x = np.unravel_index(np.argmin(dist_offset, axis=None), shape)
    return y, x


print()
sim_date = sys.argv[1]
profile_lat = np.float64(sys.argv[2])
profile_lon = np.float64(sys.argv[3])
#
path = '../Data/%s/WRF' % sim_date
ncfnames = sorted(glob('%s/*.nc' % path))
print('found %d files' % len(ncfnames))
print()
#
dates = list()
times = list()
for ncfname in ncfnames:
    grid_num = int(ncfname.split('/')[-1].split('.')[0].split('_')[2][-1:])
    date_str = ncfname.split('/')[-1].split('.')[0].split('_')[3]
    time_str = ncfname.split('/')[-1].split('.')[0].split('_')[4][:2]
    dates.append(date_str)
    times.append(time_str)
ntimes = len(times)
#
y, x = find_loc_xy(ncfnames[0], profile_lat, profile_lon)
level_interval = 100  # m
level_max = 1600  # m
levels = np.arange(0, level_max+level_interval, level_interval).astype(int)
nlevels = len(levels)
T_panel = np.zeros((nlevels, ntimes))
wind_panel = np.zeros_like(T_panel)
#
for i, ncfname in enumerate(ncfnames):
    print('reading and interpolating T/wind profiles for %s' % ncfname)
    ncfile = Dataset(ncfname, 'r')
    Z_loc = getvar(ncfile, 'geopotential_height')[:, y, x]
    T2_loc = getvar(ncfile, 'T2')[y, x]
    T_loc = getvar(ncfile, 'temperature')[:, y, x]
    U_loc = getvar(ncfile, 'ue_unstaggered')[:, y, x]
    V_loc = getvar(ncfile, 've_unstaggered')[:, y, x]
    T_profile = to_np(interp1d(T_loc, Z_loc, levels))
    T_profile[0] = T2_loc
    T_panel[:, i] = T_profile
    U_profile = to_np(interp1d(U_loc, Z_loc, levels))
    U10_loc = getvar(ncfile, 'u10_e')[y, x]
    V_profile = to_np(interp1d(V_loc, Z_loc, levels))
    V10_loc = getvar(ncfile, 'v10_e')[y, x]
    wind_profile = np.sqrt(U_profile**2 + V_profile**2)
    wind_profile[0] = np.sqrt(U10_loc**2 + V10_loc**2)
    wind_panel[:, i] = wind_profile
#
fig = plt.figure(figsize=(8, 8))
ax_T = fig.add_subplot(2,1,1)
clevels = np.arange(4, 35)
T_contours = plt.contourf(T_panel, levels=clevels, cmap=get_cmap('jet'))
cbar = plt.colorbar(T_contours, pad=0.02, shrink=0.75)
labels = cbar.ax.get_yticklabels()
cbar.ax.set_yticklabels(labels=labels, fontsize=14)
cbar.ax.set_ylabel(r'$T$ [$^{\circ}$C]', fontsize=14)
ax_T.set_xticks(np.arange(ntimes))
ax_T.set_xticklabels(times, fontsize=14)
ax_T.set_yticks(np.arange(nlevels)[::2])
ax_T.set_yticklabels(levels[::2], fontsize=14)
ax_T.set_ylabel('Altitude AMSL [m]', fontsize=14)
#
ax_wind = fig.add_subplot(2,1,2)
clevels = np.arange(0, 25)
wind_contours = plt.contourf(wind_panel, levels=clevels, cmap=get_cmap('jet'))
plt.clim(0, 24)
cbar = plt.colorbar(wind_contours, pad=0.02, shrink=0.75)
labels = cbar.ax.get_yticklabels()
cbar.ax.set_yticklabels(labels=labels, fontsize=14)
cbar.ax.set_ylabel('wind speed [m/s]', fontsize=14)
ax_wind.set_xticks(np.arange(ntimes))
ax_wind.set_xticklabels(times, fontsize=14)
ax_wind.set_xlabel('Time [UTC]', fontsize=14)
ax_wind.set_yticks(np.arange(nlevels)[::2])
ax_wind.set_yticklabels(levels[::2], fontsize=14)
ax_wind.set_ylabel('Altitude AMSL [m]', fontsize=14)
#
plt.tight_layout()
fname = 'WRF_%s_%.1fN_%.1fW_T_wind_profiles.png' % (sim_date, profile_lat, abs(profile_lon))
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('- saved %s' % fname)
plt.close()
print()

# end map_wrf_io_T_wind_profiles.py
