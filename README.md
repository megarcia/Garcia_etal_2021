## Code supplement to accompany Garcia et al. (2022)

### Primary reference:

Garcia, M., B.R. Sturtevant, R. Saint-Amant, J.J. Charney, J. Delisle, Y. Boulanger, P.A. Townsend, and J. Régnière, 2022: "Modeling weather-driven long-distance dispersal of spruce budworm moths (_Choristoneura fumiferana_). Part 1: Model description." _Agricultural and Forest Meteorology_, doi: [10.1016/j.agrformet.2022.108815](https://doi.org/10.1016/j.agrformet.2022.108815).

Contact: [matt.e.garcia@gmail.com](mailto://matt.e.garcia@gmail.com)

<hr>

### Essential info:

This **code supplement** covers the python scripts we used to generate the figures in the main paper, some of the figures in the Supplemental Materials, and the supplemental animations referenced there. Links are provided to the sample data used to render those figures and animations. 

**Model code for SBW–pyATM** is available in a [separate GitHub repository](https://github.com/megarcia/SBW-pyATM).

Since two of our authors are U.S. Government employees and four of our authors are Government of Canada employees, we are aiming to provide the main paper as an open-access document in the public domain (CC0).

All **code** provided here is copyright ©2021 by Matthew Garcia, who programmed and performed all data analysis for the publication. All code in this supplement is licensed for reuse under the **GPLv3**, which is reproduced in full in a [separate document](https://github.com/megarcia/Garcia_etal_2022a/blob/main/LICENSE) in this repository.

The **datasets** used by these scripts are located on [Dryad](https://datadryad.org/) and will be available upon final publication at doi: [10.5061/dryad.mpg4f4r19](https://doi.org/10.5061/dryad.mpg4f4r19). A README.txt file is also available there describing the sample datasets and supplemental animations.

The **supplemental animations** (SA) produced using these scripts and data are located on [Zenodo](https://zenodo.org/) (via Dryad) at doi: [10.5281/zenodo.5534999](https://doi.org/10.5281/zenodo.5534999):

<hr>

### Repository contents:

LICENSE (text of GPLv3)

README.md (this file)

Shell script "plot_all_figures.sh" (see instructions below)

Data (structure after you obtain the remaining data files from Dryad):
* 2013 SBW defoliation aerial survey map (GeoTIFF format)
* 20130714
    * WRF model output (3-km horizontal resolution, 1-h temporal resolution)
    * XAM radar data (derived reflectivity product)
    * SBW–pyATM simulation results 
* 20130715
    * WRF model output (3-km horizontal resolution, 1-h temporal resolution)
    * XAM radar data (derived reflectivity product)
    * SBW–pyATM simulation results

Fig_01:
* python script "map_defoliation_annotated.py"
* finished Figure 1

Fig_04:
* finished Figure 2, developed using [LucidChart](https://www.lucidchart.com/)

Fig_03:
* python script "map_wrf_io_T_wind_prs.py"
* python script "map_wrf_io_T_wind_sfc.py"
* finished Figure 3 in ten parts, all included in the Supplemental Materials, with four parts shown in the main paper

Fig_04:
* python script "plot_all_flights.py"
* finished Figure 4

Fig_05:
* python script "map_flier_count_+_radar_hexbin.py"
* finished Figure 5 in two parts

Fig_06 (uses scripts in Fig_03):
* finished Figure 6 in ten parts, all included in the Supplemental Materials, with four parts shown in the main paper

Fig_07 (uses script in Fig_04):
* finished Figure 7

Fig_08 (uses script in Fig_05):
* finished Figure 8 in two parts

Fig_09:
* python script "plot_selected_flights_map_+_profiles.py"
* finished Figure 9 in five parts, including an orientation map and four flight profiles

Fig_10:
* python script "plot_wrf_io_T_wind_profile.py"
* finished Figure 10 in two parts

Fig_11:
* python script "plot_flight_altitude_combined_histograms.py"
* python script "plot_flight_distance_combined_histograms.py"
* finished Figure 11 in two parts

Fig_12:
* python script "map_male_landings_female_imported_fecundity_hexbin.py"
* python script "map_oviposition_hexbin.py"
* finished Figure 12 in four parts

Animations (see special instructions below):
* python script "map_wrf_io_T_wind_2-panel.py"
* python script "plot_flight_trajectories_animation.py"
* python script "map_flier_count_+_radar_hexbin.py"

<hr>

### Python requirements:

Follow the instructions below to obtain from Dryad the data files that are processed with these scripts.

To run the python scripts included here, you will need the following python packages and libraries in your local python installation:

* standard libraries: os, sys, glob
* numpy
* pandas
* netCDF4
* matplotlib
* basemap
* basemap-data-hires
* gdal (via osgeo)
* wrf-python (as wrf)

I recommend the [Anaconda](http://www.anaconda.com/products/individual) package installation for python, and then using the `conda` package manager, but the `pip` package manager works just as well.

To run the shell script that can generate all of the included figures using each of the python scripts, a `bash` shell script is included and can be modified to your command-line interface (and flavor of Linux) as needed.

<hr>

### Reproducing published figures using the sample data:

1. Download or clone this repository to your local directory:
* `git clone https://github.com/megarcia/Garcia_etal_2022a.git`
2. In the Garcia_etal_2022a/Data/ subdirectory:
* `mkdir 20130714 20130715`
3. Get the data files from Dryad:
* If you have the `wget` utility on your system:<br>
`wget (URLs forthcoming)`
<br>**or**
* Go to https://doi.org/10.5061/dryad.mpg4f4r19 in your browser, download all six (6) of the "*.tar.gz" files available there, and place them in your new Garcia_etal_2022a/Data/ subdirectory.
4. Uncompress the data files to their respective subdirectories:
* `for f in 20130714_*.tar.gz ; do tar -xzf $f -C 20130714/ ; done`
* `for f in 20130715_*.tar.gz ; do tar -xzf $f -C 20130715/ ; done`
6. In the main Garcia_etal_2022a repository directory:
* `bash plot_all_figures.sh`

You can also examine the "plot_all_figures.sh" shell script to see the arguments required for any single figure's python script, as desired. Note that if you're just interested in selected figures and their scripts, you may not need to download and decompress all of the data files.

<hr>

### Reproducing supplemental animations using the sample data:

I used the `convert` tool in [ImageMagick](https://imagemagick.org/) to compile animated GIF files from the PNG frames generated using the python scripts included here. There are many ways to animate still frames, from the animation capabilities of [Matplotlib](https://matplotlib.org/stable/index.html) itself to various software that produces animated GIFs and MP4 movies.

These instructions assume that you are using the scripts in this repository to generate still frames, then compiling them to an animated GIF using ImageMagick. These scripts use the same data files as the figure scripts above.

To generate an animated GIF of selected WRF output fields (surface temperature and winds, and 900 hPa wind speed):
1. Generate the hourly maps:
* `python map_wrf_io_T_wind_2-panel.py [date]` where `[date]` is either `20130714` or `20130715`
2. Stitch together the PNG files using ImageMagick:
* `convert -delay 50 -loop 1 *_sfc_T_wind_900hPa_windspeed.png [date]_WRF-NARR_900hPa_wind_sfc_T.gif`<br>
Note that the "delay" option value is given in hundredths of a second and the "loop" option value is 1 (one), so this animation runs at 2 frames per second and plays only once.

To generate an animated GIF of pyATM trajectories for one replicate simulation:
1. Generate the maps at 5-minute intervals:
* `python plot_flight_trajectories_animation.py [date] 0 5` where `[date]` is either `20130714` or `20130715`
2. Stitch together the PNG files using ImageMagick:
* `convert -delay 50 -loop 1 [date]_*.png [date]_SBW-pyATM_flight_trajectories.gif`<br>

The data, script, and instructions for generating the animated comparison between the density of SBW moths in flight and the XAM radar reflectivity are reserved by the authors at this time, as they form the foundation for an algorithm to be presented in Part 2 of the publication.

