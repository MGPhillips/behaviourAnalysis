from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

success_l = []
success_d = []

time_cutoffs = np.arange(0, 30 * 60)

recent_mice = ['370_1', '371_5', '371_1', '445_1', '447_2', '447_3', '447_4',
               '550_1', '551_5', '551_2', '551_3', '551_4', '551_5', '619_1', '619_2', '619_3', '620_2']

for i in time_cutoffs:
    # flight_df['flight_success'] = flight_df.apply(get_flight_success, args=(i,), axis=1)
    flight_df['flight_success'] = flight_df.apply(get_flight_success, args=(i,), axis=1)

    df_analyse = flight_df[flight_df['mouse_id'].isin(recent_mice)]
    dark_df = df_analyse[df_analyse['expt_type'] == 'dark']
    light_df = df_analyse[df_analyse['expt_type'] == 'light']

    success_l.append(len(light_df[light_df['flight_success'] == 'successful']) / len(light_df))
    success_d.append(len(dark_df[dark_df['flight_success'] == 'successful']) / len(dark_df))

fig, ax = plt.subplots()

ax.plot(time_cutoffs/30, success_l, color='blue', label='Light')
ax.plot(time_cutoffs/30, success_d, color='magenta', label='Dark')

ax.legend(loc=5)

