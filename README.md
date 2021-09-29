## Code supplement to accompany Garcia et al. (2021, submitted)

### Primary reference:

Garcia, M., B.R. Sturtevant, R. Saint-Amant, J.J. Charney, J. Delisle, Y. Boulanger, P.A. Townsend, and J. Régnière, 2021: "Modeling weather-driven long-distance dispersal of spruce budworm moths (_Choristoneura fumiferana_), part 1: Model description." Submitted to _Agricultural and Forest Meteorology_ (Elsevier) on 28 September 2021.

Contact: [matt.e.garcia@gmail.com](mailto://matt.e.garcia@gmail.com)

This reference information will be updated throughout the review and publication process.

<hr>

### Supplemental animations:

SA1: [20130714-15_WRF-NARR_900hPa_wind_sfc_T.gif](https://datadryad.org/stash/downloads/zenodo_file/1047948?share=qeePqE_OSF0bZbHcW9gi_nhDvijyLynNj6R4Wwuj_98)

SA2: [20130714-15_SBW-pyATM_flight_trajectories.gif](https://datadryad.org/stash/downloads/zenodo_file/1047951?share=qeePqE_OSF0bZbHcW9gi_nhDvijyLynNj6R4Wwuj_98)

SA3: [20130714-15_pyATM_flier_density_XAM_radar.gif](https://datadryad.org/stash/downloads/zenodo_file/1047952?share=qeePqE_OSF0bZbHcW9gi_nhDvijyLynNj6R4Wwuj_98)

SA4: [20130715-16_WRF-NARR_900hPa_wind_sfc_T.gif](https://datadryad.org/stash/downloads/zenodo_file/1047947?share=qeePqE_OSF0bZbHcW9gi_nhDvijyLynNj6R4Wwuj_98)

SA5: [20130715-16_SBW-pyATM_flight_trajectories.gif](https://datadryad.org/stash/downloads/zenodo_file/1047944?share=qeePqE_OSF0bZbHcW9gi_nhDvijyLynNj6R4Wwuj_98)

SA6: [20130715-16_pyATM_flier_density_XAM_radar.gif](https://datadryad.org/stash/downloads/zenodo_file/1047953?share=qeePqE_OSF0bZbHcW9gi_nhDvijyLynNj6R4Wwuj_98)

<hr>

### Essential info:

This **code supplement** covers the figures in the main manuscript and the supplemental animations referenced there, and includes the data required and python scripts used to render those figures and animations. 

Since two of our authors are U.S. Government employees and four of our authors are Government of Canada employees, we are aiming to provide the main paper as an open-access document in the public domain (CC0).

All code provided here is copyright © 2021 by Matthew Garcia, who programmed and performed all data analysis for the attached publication. All code in this supplement is licensed for reuse under the **GPLv3**, which is reproduced in full in a [separate document](https://github.com/megarcia/Garcia_etal_2021/blob/main/LICENSE) in this repository.

The **datasets** used by these scripts are located on Dryad and will be availble upon publication at https://doi.org/10.5061/dryad.mpg4f4r19. Access prior to publication is available at [this location](https://datadryad.org/stash/share/qeePqE_OSF0bZbHcW9gi_nhDvijyLynNj6R4Wwuj_98) (a large automatic download will start).

The **supplemental animations** produced using these scripts and data are located on Zenodo at the locations listed above.

**Model code for SBW–pyATM** is available in a [separate GitHub repository](https://github.com/megarcia/SBW-pyATM).

<hr>

### Requirements

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

To run the shell script that can generate all of the included figures using each of the python scripts, a `bash` shell script is included and can be modified to your command line interface as needed.

<hr>

### Contents

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

Fig_02:
* python script "map_wrf_io_T_wind_prs.py"
* python script "map_wrf_io_T_wind_sfc.py"
* finished Figure 2 in four parts

Fig_03:
* python script "plot_all_flights.py"
* finished Figure 3

Fig_04:
* python script "map_flier_count_+_radar_hexbin.py"
* finished Figure 4 in two parts

Fig_05 (uses scripts in Fig_02):
* finished Figure 5 in four parts

Fig_06 (uses script in Fig_03):
* finished Figure 6

Fig_07 (uses script in Fig_04):
* finished Figure 7 in two parts

Fig_08:
* python script "plot_selected_flights_map_+_profiles.py"
* finished Figure 8 in five parts

Fig_09:
* python script "plot_wrf_io_T_wind_profile.py"
* finished Figure 9 in two parts

Fig_10:
* python script "plot_flight_altitude_combined_histograms.py"
* python script "plot_flight_distance_combined_histograms.py"
* finished Figure 10 in two parts

Fig_11:
* python script "map_male_landings_female_imported_fecundity_hexbin.py"
* python script "map_oviposition_hexbin.py"
* finished Figure 11 in four parts

Animations (see special instructions below):
* python script "map_wrf_io_T_wind_2-panel.py"
* python script "plot_flight_trajectories_animation.py"
* python script "map_flier_count_+_radar_hexbin.py"

<hr>

### Instructions for figure scripts

1. Download or clone this repository to your local directory:
* `git clone https://github.com/megarcia/Garcia_etal_2021.git`
2. In the Garcia_etal_2021/Data/ subdirectory:
* `mkdir 20130714 20130715`
3. Get the data files from Dryad:
* If you have the `wget` utility on your system:<br>
`wget (URLs forthcoming)`
<br>**or**
* Go to https://doi.org/10.5061/dryad.mpg4f4r19 in your browser, download all six of the "*.tar.gz" files available there, and place them in your new Garcia_etal_2021/Data/ subdirectory.
4. Uncompress the data files to their respective subdirectories:
* `for f in 20130714_*.tar.gz ; do tar -xzf $f -C 20130714/ ; done`
* `for f in 20130715_*.tar.gz ; do tar -xzf $f -C 20130715/ ; done`
6. In the main Garcia_etal_2021 repository directory:
* `bash plot_all_figures.sh`

You can also examine the "plot_all_figures.sh" shell script to see the arguments required for any single figure's python script, as desired. Note that if you're just interested in selected figures and their scripts, you may not need to download and decompress all of the data files.

<hr>

### Instructions for animation scripts

I used the `convert` tool in [ImageMagick](https://imagemagick.org/) to compile animated GIF files from the PNG frames generated using the python scripts included here. There are many ways to animate still frames, from the animation capabilities of [Matplotlib](https://matplotlib.org/stable/index.html) itself to various software that produces animated GIFs and MP4 movies.

These instructions assume that you are using the scripts in this repository to generate still frames, then compiling them to an animated GIF using ImageMagick. These scripts use the same data files as the figure scripts above.

To generate an animated GIF of selected WRF output fields (surface temperature and winds, and 900 hPa wind speed):
1. Generate the hourly maps:
* `python map_wrf_io_T_wind_2-panel.py [date]` where `[date]` is either `20130714` or `20130715`
2. Stitch together the PNG files using ImageMagick:
* `convert -delay 50 *_sfc_T_wind_900hPa_windspeed.png [date]_WRF-NARR_900hPa_wind_sfc_T.gif`<br>
Note that the "delay" option value is given in hundreths of a second, so this animation runs at 2 frames per second.

To generate an animated GIF of pyATM trajectories for one replicate simulation:
1. Generate the minute-by-minute maps:
* `python plot_flight_trajectories_animation.py [date] 0` where `[date]` is either `20130714` or `20130715`
2. Stitch together the PNG files using ImageMagick:
* `convert -delay 10 -loop 0 *.png [date]_SBW-pyATM_flight_trajectories.gif`<br>
Note that the "loop" option value is 0 (zero), so this animation runs at 10 frames per second and does not loop.

The data, script, and instructions for generating the animated comparison between the density of SBW moths in flight and the XAM radar reflectivity are reserved by the authors at this time, as they form the foundation for an algorithm to be presented in Part 2 of the publication.

