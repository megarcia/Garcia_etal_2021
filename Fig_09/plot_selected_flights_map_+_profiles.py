"""
Python script "plot_selected_flights_map_+_profiles.py"
by Matthew Garcia, Postdoctoral Research Associate
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2021 by Matthew Garcia
"""


import iso8601
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.cm import get_cmap
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap
mpl.use('Agg')
import matplotlib.pyplot as plt


def get_idxs(alt_all, sfc_all):
    idx1 = 0
    for idx, alt in enumerate(alt_all):
        if alt > sfc_all[idx]:
            idx1 = idx - 1
            break
    idx2 = -1
    for idx in range(len(alt_all)-1, -1, -1):
        if alt_all[idx] > sfc_all[idx]:
            idx2 = idx + 2
            break
    return idx1, idx2


def plot_profile(elapsed_time, alt, Temp, fname):
    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(1,1,1)
    points = np.array([elapsed_time, alt]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    T_min, T_max = 17, 27
    norm = plt.Normalize(T_min, T_max)
    lc = LineCollection(segments, cmap=get_cmap('jet'), norm=norm)
    lc.set_array(Temp)
    lc.set_linewidth(5)
    line = plt.gca().add_collection(lc)
    #
    T_ticks = np.arange(T_min, T_max+1, 2).astype(int)
    cbar = plt.colorbar(line, ticks=T_ticks, pad=0.02, shrink=0.75)  #, orientation='vertical')
    cbar.ax.set_yticklabels(T_ticks, fontsize=14)
    cbar.set_label(r'$T$ [$^{\circ}$C]', fontsize=14)
    #
    plt.plot(elapsed_time, sfc, color='k', label='ground')
    plt.xlim(0, elapsed_time[-1]+1)
    xticks = np.arange(0, ((elapsed_time[-1]//60)+1)*60, 60).astype(int)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xticks, fontsize=14)
    plt.xlabel('Flight time [mins]', fontsize=14)
    #
    plt.ylim(0, 1200)
    yticks = np.arange(0, 1200+1, 200).astype(int)
    ax1.set_yticks(yticks)
    ax1.set_yticklabels(yticks, fontsize=14)
    plt.ylabel('Altitude [m AMSL]', fontsize=14)
    #
    plt.tight_layout()
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    print('saved %s' % fname)
    plt.close()
    return


rep_num = 0
flights = {'20130714' : ['000000101', '000000124'],
           '20130715' : ['000000168', '000000820']}
colors = ['red', 'orange', 'green', 'blue']
markers = [('a', "a'"), ('b', "b'"), ('c', "c'"), ('d', "d'")]
#
#
# setup map
bottom_lat, top_lat = 45.0, 51.0
mid_lat = (bottom_lat + top_lat) / 2.0
left_lon, right_lon = -73.0, -64.0
mid_lon = (left_lon + right_lon) / 2.0
#
map1 = plt.figure(figsize=(6, 6))
bmap = Basemap(projection='tmerc', lon_0=mid_lon, lat_0=mid_lat,
               lat_ts=mid_lat, llcrnrlat=bottom_lat, llcrnrlon=left_lon,
               urcrnrlat=top_lat, urcrnrlon=right_lon, resolution='h',
               area_thresh=500)
bmap.drawcoastlines()
bmap.drawstates()
bmap.drawcountries()
bmap.drawmapboundary(fill_color='lightblue')
bmap.fillcontinents(color='white', lake_color='lightblue')
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
# plot individual flight profiles and map trajectories
i = 0
for sim_date, fliers in flights.items():
    path = '../Data/%s/pyATM/WRF-NARR_d03_%s_simulation_%s_output' % \
        (sim_date, sim_date, str(rep_num).zfill(5))
    for flier in fliers:
        infname = '%s/flier_%s_%s_%s_report.csv' % (path, str(rep_num).zfill(5), sim_date, flier)
        print('reading %s' % infname.split('/')[-1])
        df = pd.read_csv(infname, index_col=False)
        #
        date_time_all = list(df['date_time'])
        lat_all = np.array(df['lat'])
        lon_all = np.array(df['lon'])
        alt_all = np.array(df['alt_MSL'])
        sfc_all = np.array(df['sfc_elev'])
        T_all = np.array(df['T'])
        #
        idx1, idx2 = get_idxs(alt_all, sfc_all)
        date_time = date_time_all[idx1:idx2]
        lat = lat_all[idx1:idx2]
        lon = lon_all[idx1:idx2]
        alt = alt_all[idx1:idx2]
        sfc = sfc_all[idx1:idx2]
        T = T_all[idx1:idx2]
        #
        init_time = iso8601.parse_date(date_time[0])
        elapsed_time = list()
        for tt in date_time:
            tdiff = iso8601.parse_date(tt) - init_time
            elapsed_time.append(tdiff.seconds / 60.0)
        #
        # plot all flight trajectories on common map
        text_offset = 0.1
        bmap.plot(lon[0], lat[0], '+', markersize=10, color='k', latlon=True)
        x, y = bmap(lon[0]-text_offset, lat[0]+text_offset)
        plt.text(x, y, markers[i][0], va='bottom', ha='center', fontsize=14)
        bmap.plot(lon[-1], lat[-1], 'x', markersize=10, color='k', latlon=True)
        x, y = bmap(lon[-1]+text_offset, lat[-1]-text_offset)
        plt.text(x, y, markers[i][1], va='top', ha='center', fontsize=14)
        bmap.plot(lon, lat, linewidth=5, color=colors[i], latlon=True)
        #
        # plot individual flight altitude/T profile
        outfname = 'flier_%s_%s_%s_alt_T_profile.png' % (str(rep_num).zfill(5), sim_date, flier)
        plot_profile(elapsed_time, alt, T, outfname)
        #
        i += 1
#
map1.tight_layout()
fname = 'combined_flight_profiles_map.png'
map1.savefig(fname, dpi=300, bbox_inches='tight')
print('saved figure %s' % fname)
plt.close()

# end plot_selected_flights_map_+_profiles.py
