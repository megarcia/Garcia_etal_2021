"""
Python script "plot_flight_distance_combined_histograms.py"
by Matthew Garcia, Post-doctoral Research Associate
Dept. of Forest and Wildlife Ecology
University of Wisconsin - Madison
matt.e.garcia@gmail.com

Copyright (C) 2021 by Matthew Garcia
"""


import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)
#
sim_date = '20130714'
overall_fname = '../Data/%s/pyATM/default_flight_dist_histogram.csv' % sim_date
overall_df = pd.read_csv(overall_fname, index_col=False)
x_vals = np.array(overall_df.columns).astype(int)
overall_y_vals = np.array(overall_df.sum(axis=0).astype(float))
female_fname = '../Data/%s/pyATM/default_flight_dist_female_histogram.csv' % sim_date
female_df = pd.read_csv(female_fname, index_col=False)
female_y_vals = np.array(female_df.sum(axis=0).astype(float))
female_y_vals = female_y_vals / np.sum(overall_y_vals)
plt.plot(x_vals, female_y_vals, 'r--', label='14-15 July females')
male_fname = '../Data/%s/pyATM/default_flight_dist_male_histogram.csv' % sim_date
male_df = pd.read_csv(male_fname, index_col=False)
male_y_vals = np.array(male_df.sum(axis=0).astype(float))
male_y_vals = male_y_vals / np.sum(overall_y_vals)
plt.plot(x_vals, male_y_vals, 'b--', label='14-15 July males')
#
sim_date = '20130715'
overall_fname = '../Data/%s/pyATM/default_flight_dist_histogram.csv' % sim_date
overall_df = pd.read_csv(overall_fname, index_col=False)
x_vals = np.array(overall_df.columns).astype(int)
overall_y_vals = np.array(overall_df.sum(axis=0).astype(float))
female_fname = '../Data/%s/pyATM/default_flight_dist_female_histogram.csv' % sim_date
female_df = pd.read_csv(female_fname, index_col=False)
female_y_vals = np.array(female_df.sum(axis=0).astype(float))
female_y_vals = female_y_vals / np.sum(overall_y_vals)
plt.plot(x_vals, female_y_vals, 'r-', label='15-16 July females')
male_fname = '../Data/%s/pyATM/default_flight_dist_male_histogram.csv' % sim_date
male_df = pd.read_csv(male_fname, index_col=False)
male_y_vals = np.array(male_df.sum(axis=0).astype(float))
male_y_vals = male_y_vals / np.sum(overall_y_vals)
plt.plot(x_vals, male_y_vals, 'b-', label='15-16 July males')
#
plt.legend(loc='upper right', fontsize=12)
plt.xlim([0, 400])
plt.ylim([0.0, 0.05])
xticks = np.arange(0, 401, 50)
ax1.set_xticks(xticks)
ax1.set_xticklabels(xticks, fontsize=14)
plt.xlabel('overall flight distance (km)', fontsize=14)
yticks = np.arange(0, 0.06, 0.01)
ax1.set_yticks(yticks)
ax1.set_yticklabels(yticks, fontsize=14, rotation='vertical', va='center')
plt.ylabel('fraction of all fliers', fontsize=14)
#
plt.tight_layout()
fname = 'default_flight_dist_combined_histograms.png'
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('saved figure %s' % fname)
plt.close()

# end plot_flight_distance_combined_histogram.py
