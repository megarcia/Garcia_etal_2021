## Code supplement to accompany

## Garcia et al. (2021, submitted)

### Reference:

Garcia, M., B.R. Sturtevant, R. Saint-Amant, J.J. Charney, J. Delisle, Y. Boulanger, P.A. Townsend, and J. Régnière, 2021: "Modeling weather-driven long-distance dispersal of spruce budworm moths (_Choristoneura fumiferana_), part 1: Model description." Submitted to _Agricultural and Forest Meteorology_ (Elsevier) on 28 September 2021.

Contact: [matt.e.garcia@gmail.com](mailto://matt.e.garcia@gmail.com)

This reference information will be updated throughout the review and publication process.

<hr>

This code supplement covers the figures in the main manuscript and includes the data required and python scripts used to render those figures. Model code for SBW–pyATM is available in a [separate GitHub repository](https://github.com/megarcia/SBW-pyATM).

Since two of our authors are U.S. Government employees and four of our authors are Government of Canada employees, the main paper will be provided as an open-access document in the public domain (CC0).

This code supplement is licensed for use under the GPLv3, reproduced in full in a [separate document](https://github.com/megarcia/Garcia_etal_2021/blob/main/LICENSE) in this repository.

<hr>

### Requirements

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

Data:
* SBW defoliation map
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

<hr>

### Instructions

1. Download or clone this repository to your local directory:
* `git clone https://github.com/megarcia/Garcia_etal_2021.git`
2. In the Data subdirectory, from your command line:
* `tar -xzf 20130714.tar.gz` (note: uncompressed size ~3GB)
* `tar -xzf 20130715.tar.gz` (note: uncompressed size ~3GB)
3. In the main repository directory:
* `bash plot_all_figures.sh`

You can also examine the "plot_all_figures.sh" shell script to see the arguments required for any single figure's python script, as desired.

<hr>


