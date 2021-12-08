# pylint: disable=C0103
"""
Python script "map_defoliation_annotated.py"
by Matthew Garcia, Ph.D.
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2021 by Matthew Garcia
"""


import sys
import numpy as np
from osgeo import gdal
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


tif_name = '../Data/TBE_2013.tif'
year = tif_name.split('/')[-1].split('.')[0].split('_')[1]
#
print('getting grid information from %s' % tif_name)
ds = gdal.Open(tif_name)
nrows = ds.RasterYSize
ncols = ds.RasterXSize
print('grid shape: %d rows, %d cols' % (nrows, ncols))
gt = ds.GetGeoTransform()
grid = np.flipud(ds.ReadAsArray())
grid = np.where(grid == -9999.0, np.nan, grid)
#
SW_lon = gt[0]
dlon = gt[1]
NE_lat = gt[3]
dlat = -gt[5]
SW_lat = NE_lat + ncols * gt[4] - nrows * dlat
NE_lon = SW_lon + ncols * dlon + nrows * gt[2]
lons = np.arange(SW_lon+dlon/2.0, NE_lon+dlon/2.0, dlon)
if len(lons) != ncols:
    sys.exit('len(east) != ncols :: %d != %d' % (len(lons), ncols))
lats = np.arange(SW_lat+dlat/2.0, NE_lat+dlat/2.0, dlat)
if len(lats) != nrows:
    sys.exit('len(north) != nrows :: %d != %d' % (len(lons), nrows))
lons, lats = np.meshgrid(lons, lats)
#
bottom_lat, top_lat = 45.0, 51.0
mid_lat = (bottom_lat + top_lat) / 2.0
left_lon, right_lon = -73.0, -64.0
mid_lon = (left_lon + right_lon) / 2.0
#
fig = plt.figure(figsize=(8, 8))
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
print('- plotting %s defoliation' % year)
x, y = bmap(lons, lats)
clevs = [0.5, 1.5, 2.5, 3.5]
defol_map = bmap.contourf(x, y, grid, clevs, cmap=get_cmap('YlOrRd'), zorder=9)
cbar = plt.colorbar(defol_map, pad=0.02, shrink=0.75)
cbar.set_ticks(clevs)
cbar.ax.set_yticklabels(labels=['light defoliation', 'moderate defoliation', 'severe defoliation', ''],
                        rotation=90, va='bottom', fontsize=12)
# 
bmap.drawmapscale(lon=left_lon+1.25, lat=top_lat-0.5, lon0=mid_lon, lat0=mid_lat, length=200.0,
                  barstyle='fancy', fillcolor1='w', fillcolor2='k', fontsize=16)
parallels = np.arange(30., 60., 1.)
bmap.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=16)
meridians = np.arange(270., 360., 1.)
bmap.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=16)
#
annotations = [(45.8, -69.0, 'Maine', 0, 14), (46.8, -66.5, 'New Brunswick', 0, 14),
               (49.75, -72.0, 'Quebec', 0, 14), (46.1, -71.5, 'Quebec', 0, 14),
               (48.4783, -67.5822, '+', 0, 20), (48.25, -67.95, 'XAM\nradar', 0, 12),
               (48.4, -72.7, 'St. Jean\nLake', 0, 12),
               (48.1, -70.8, 'Saguenay R.', 0, 12),
               (49.35, -65.8, 'St. Lawrence estuary', 10, 12),
               (49.7, -66.3, 'North\nShore', 0, 12),
               (47.5, -69.5, 'Lower St. Lawrence', 50, 12),
               (48.6, -66.0, 'Gaspe', 0, 12),
               (49.1, -69.7, 'Betsiamites R.', -40, 10),
               (50.65, -65.85, 'Moisie R.', -90, 10),
               (50.65, -64.55, 'St. Jean R.', -90, 10),
               (48.5, -69.0, '+', 0, 20), (48.65, -68.65, 'Fig.\n10a', 30, 12),
               (49.0, -68.0, '+', 0, 20), (49.05, -67.6, 'Fig.\n10b', 0, 12)] 
for annotation in annotations:
    x, y = bmap(annotation[1], annotation[0])
    plt.text(x, y, annotation[2], va='center', ha='center',
             rotation=annotation[3], fontsize=annotation[4])
x1, y1 = bmap(-67.8, 49.7)
x2, y2 = bmap(-66.7, 49.7)
plt.plot([x1, x2], [y1, y2], 'k-', linewidth=3, zorder=10)
#
plt.tight_layout()
fname = '%s_defoliation_annotated.png' % year
plt.savefig(fname, dpi=300, bbox_inches='tight')
plt.close()
print('- saved %s' % fname)

# end map_defoliation_annotated.py
