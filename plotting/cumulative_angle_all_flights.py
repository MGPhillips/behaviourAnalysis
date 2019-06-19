from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

recent_mice = ['445_1', '447_2', '447_3', '447_4',
               '550_1', '551_5', '551_2', '551_3', '551_4','551_5', '619_1', '619_2', '619_3', '620_2']#,

recent_mice_df = flight_df[flight_df['mouse_id'].isin(recent_mice)]

fig, ax = plt.subplots(2, 1, figsize=(15, 30), sharey=True)

for ind in recent_mice_df.index:
    if recent_mice_df['flight_success'][ind] != 'successful':
        continue

    cumulative = np.cumsum(recent_mice_df['vec_angles'][ind][300:])
    x = np.arange(-len(cumulative), 0)
    if recent_mice_df['expt_type'][ind] == 'light':
        ax[0].plot(x, cumulative)

    if recent_mice_df['expt_type'][ind] == 'dark':
        ax[1].plot(x, cumulative)

ax[0].set_title('Cumulative angle across flight: LIGHT')
ax[1].set_title('Cumulative angle across flight: DARK')

for axis in ax:
    axis.set_ylim([0, 60])
    axis.set_xlim([-250, 0])


