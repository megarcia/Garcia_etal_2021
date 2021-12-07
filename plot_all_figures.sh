#!/bin/bash
#

cd Fig_01
python map_defoliation_annotated.py 
cp 2013_defoliation_annotated.png Fig_01.png
cd ../

cd Fig_03
python map_wrf_io_T_wind_prs.py 20130714
cp WRF_d03_2013-07-15_00:00_windspeed_900hPa.png Fig_03a.png
cp WRF_d03_2013-07-15_06:00_windspeed_900hPa.png Fig_03b.png
python map_wrf_io_T_wind_sfc.py 20130714
cp WRF_d03_2013-07-15_00:00_T_wind_sfc.png Fig_03c.png
cp WRF_d03_2013-07-15_06:00_T_wind_sfc.png Fig_03d.png
cd ../

cd Fig_04
python plot_all_flights.py 20130714 0
cp 20130714_flight_trajectories_default_replicate_00000.png Fig_04.png
cd ../

cd Fig_05
python map_flier_count_+_radar_hexbin.py 20130714 20130715 0429
cp 20130715_0429_XAM_fliers_+_radar.png Fig_05ab.png
python map_flier_count_+_radar_hexbin.py 20130714 20130715 0629
cp 20130715_0629_XAM_fliers_+_radar.png Fig_05cd.png
cd ../

cd Fig_06
python ../Fig_02/map_wrf_io_T_wind_prs.py 20130715
cp WRF_d03_2013-07-16_00:00_windspeed_900hPa.png Fig_06a.png
cp WRF_d03_2013-07-16_06:00_windspeed_900hPa.png Fig_06b.png
python ../Fig_02/map_wrf_io_T_wind_sfc.py 20130715
cp WRF_d03_2013-07-16_00:00_T_wind_sfc.png Fig_06c.png
cp WRF_d03_2013-07-16_06:00_T_wind_sfc.png Fig_06d.png
cd ../

cd Fig_07
python ../Fig_03/plot_all_flights.py 20130715 0
cp 20130715_flight_trajectories_default_replicate_00000.png Fig_07.png
cd ../

cd Fig_08
python ../Fig_04/map_flier_count_+_radar_hexbin.py 20130715 20130716 0159
cp 20130716_0159_XAM_fliers_+_radar.png Fig_08ab.png
python ../Fig_04/map_flier_count_+_radar_hexbin.py 20130715 20130716 0359
cp 20130716_0359_XAM_fliers_+_radar.png Fig_08cd.png
cd ../

cd Fig_09
python plot_selected_flights_map_+_profiles.py
cp combined_flight_profiles_map.png Fig_09_map.png
cp flier_00000_20130714_000000101_alt_T_profile.png Fig_09a.png
cp flier_00000_20130714_000000124_alt_T_profile.png Fig_09b.png
cp flier_00000_20130715_000000168_alt_T_profile.png Fig_09c.png
cp flier_00000_20130715_000000820_alt_T_profile.png Fig_09d.png
cd ../

cd Fig_10
python plot_wrf_io_T_wind_profile.py 20130714 48.5 -69.0
cp WRF_20130714_48.5N_69.0W_T_wind_profiles.png Fig_10a.png
python plot_wrf_io_T_wind_profile.py 20130715 49.0 -68.0
cp WRF_20130715_49.0N_68.0W_T_wind_profiles.png Fig_10b.png
cd ../

cd Fig_11
python plot_flight_altitude_combined_histograms.py
cp default_flight_alt_combined_histograms.png Fig_11a.png
python plot_flight_distance_combined_histograms.py
cp default_flight_dist_combined_histograms.png Fig_11b.png
cd ../

cd Fig_12
python map_oviposition_hexbin.py 20130714
cp 20130714_egg_deposition_map.png Fig_12a.png
python map_male_landings_female_imported_fecundity_hexbin.py 20130714
cp 20130714_male_landings_female_imported_fecundity_map.png Fig_12b.png
python map_oviposition_hexbin.py 20130715
cp 20130715_egg_deposition_map.png Fig_12c.png
python map_male_landings_female_imported_fecundity_hexbin.py 20130715
cp 20130715_male_landings_female_imported_fecundity_map.png Fig_12d.png
cd ../

