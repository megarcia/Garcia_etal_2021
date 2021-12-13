"""
Python script "plot_flight_altitude_combined_histograms.py"
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


fig = plt.figure(figsize=(4.5, 6))
ax1 = fig.add_subplot(111)
#
sim_date = '20130714'
overall_fname = '../Data/%s/pyATM/default_flight_alt_histogram.csv' % sim_date
overall_df = pd.read_csv(overall_fname, index_col=False)
y_vals = np.array(overall_df.columns).astype(int)
overall_x_vals = np.array(overall_df.sum(axis=0).astype(float))
female_fname = '../Data/%s/pyATM/default_flight_alt_female_histogram.csv' % sim_date
female_df = pd.read_csv(female_fname, index_col=False)
female_x_vals = np.array(female_df.sum(axis=0).astype(float))
female_x_vals = female_x_vals / np.sum(overall_x_vals)
plt.plot(female_x_vals, y_vals, 'r', linestyle='solid', label='14-15 July females')
male_fname = '../Data/%s/pyATM/default_flight_alt_male_histogram.csv' % sim_date
male_df = pd.read_csv(male_fname, index_col=False)
male_x_vals = np.array(male_df.sum(axis=0).astype(float))
male_x_vals = male_x_vals / np.sum(overall_x_vals)
plt.plot(male_x_vals, y_vals, 'b', linestyle='dotted', label='14-15 July males')
#
sim_date = '20130715'
overall_fname = '../Data/%s/pyATM/default_flight_alt_histogram.csv' % sim_date
overall_df = pd.read_csv(overall_fname, index_col=False)
y_vals = np.array(overall_df.columns).astype(int)
overall_x_vals = np.array(overall_df.sum(axis=0).astype(float))
female_fname = '../Data/%s/pyATM/default_flight_alt_female_histogram.csv' % sim_date
female_df = pd.read_csv(female_fname, index_col=False)
female_x_vals = np.array(female_df.sum(axis=0).astype(float))
female_x_vals = female_x_vals / np.sum(overall_x_vals)
plt.plot(female_x_vals, y_vals, 'r', linestyle='dashed', label='15-16 July females')
male_fname = '../Data/%s/pyATM/default_flight_alt_male_histogram.csv' % sim_date
male_df = pd.read_csv(male_fname, index_col=False)
male_x_vals = np.array(male_df.sum(axis=0).astype(float))
male_x_vals = male_x_vals / np.sum(overall_x_vals)
plt.plot(male_x_vals, y_vals, 'b', linestyle='dashdot', label='15-16 July males')
#
plt.legend(loc='upper right', fontsize=14)
plt.xlim([0, 0.05])
plt.ylim([0.0, 1800])
xticks = np.arange(0, 0.06, 0.01)
ax1.set_xticks(xticks)
ax1.set_xticklabels(xticks, fontsize=16)
plt.xlabel('fraction of all fliers', fontsize=16)
yticks = np.arange(0, 1801, 300)
ax1.set_yticks(yticks)
ax1.set_yticklabels(yticks, fontsize=16, rotation='vertical', va='center')
plt.ylabel('mean flight altitude [m AGL]', fontsize=16)
#
plt.tight_layout()
fname = 'default_flight_alt_combined_histograms.png'
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('saved figure %s' % fname)
plt.close()

# end plot_flight_altitude_combined_histogram.py
