from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

fig, ax = plt.subplots()

for trial in flight_df.loc[(flight_df['expt_type'] == 'light') &
                           (flight_df['dwm_trial'] != True) &
                           (flight_df['flight_success'] == 'successful')].index:
    ax.scatter(flight_df['start_distance'][trial], sum(flight_df['distance_per_frame'][trial][300:]) + 40,
               color='navy', alpha=0.5)

for trial in flight_df.loc[(flight_df['expt_type'] == 'dark') &
                           (flight_df['dwm_trial'] != True) &
                           (flight_df['flight_success'] == 'successful')].index:
    ax.scatter(flight_df['start_distance'][trial], sum(flight_df['distance_per_frame'][trial][300:]) + 40,
               color='magenta', alpha=0.5)

x_line = np.linspace(0, 850, 1000)
y_line = np.linspace(0, 850, 1000)

ax.plot(x_line, y_line, color='gray', label='linear', linestyle=':')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_xlim(0, 900)
ax.set_ylim(0, 900)