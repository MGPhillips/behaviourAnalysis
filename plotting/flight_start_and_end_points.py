#### Plot flight start and end points in nest space


fig, ax = plt.subplots(2, 1, figsize=(6, 12))

colors = {'dark': 'mediumvioletred',
          'light': 'royalblue'}

count = 0
# [flight_df.index == ind]
for ind in flight_df[(flight_df['expt_type'] == 'dark')].index:  # & (flight_df['flight_success']=='successful')
    if (int(ind)) % 3 != 0:
        continue
    if count == 0:
        ax[0].scatter(flight_df['x'][ind][300] - flight_df['shelter_position'][ind][0],
                      flight_df['y'][ind][300] - flight_df['shelter_position'][ind][1],
                      color=colors['dark'], label='Dark (start)')
        ax[0].scatter(flight_df['x'][ind][-1] - flight_df['shelter_position'][ind][0],
                      flight_df['y'][ind][-1] - flight_df['shelter_position'][ind][1],
                      color=colors['dark'], marker='x', label='Dark (end)')

    ax[0].scatter(flight_df['x'][ind][300] - flight_df['shelter_position'][ind][0],
                  flight_df['y'][ind][300] - flight_df['shelter_position'][ind][1],
                  color=colors['dark'])
    ax[0].scatter(flight_df['x'][ind][-1] - flight_df['shelter_position'][ind][0],
                  flight_df['y'][ind][-1] - flight_df['shelter_position'][ind][1],
                  color=colors['dark'], marker='x')

    count += 1

count = 0
for ind in flight_df[(flight_df['expt_type'] == 'light')].index:  # & (flight_df['flight_success']=='successful')

    if (int(ind)) % 3 != 0:
        continue
    if count == 0:
        ax[1].scatter(flight_df['x'][ind][300] - flight_df['shelter_position'][ind][0],
                      flight_df['y'][ind][300] - flight_df['shelter_position'][ind][1],
                      color=colors['light'], label='Light (start)')
        ax[1].scatter(flight_df['x'][ind][-1] - flight_df['shelter_position'][ind][0],
                      flight_df['y'][ind][-1] - flight_df['shelter_position'][ind][1],
                      color=colors['light'], marker='x', label='Light (end)')

    ax[1].scatter(flight_df['x'][ind][300] - flight_df['shelter_position'][ind][0],
                  flight_df['y'][ind][300] - flight_df['shelter_position'][ind][1],
                  color=colors['light'])
    ax[1].scatter(flight_df['x'][ind][-1] - flight_df['shelter_position'][ind][0],
                  flight_df['y'][ind][-1] - flight_df['shelter_position'][ind][1],
                  color=colors['light'], marker='x')
    count += 1

for axis in ax:
    axis.scatter(0, 0, color='k')

    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)
    axis.tick_params(left=False, bottom=False, labelbottom=False, labelleft=False, )
    axis.set_title('Mouse start and end positions in nest space (2 x 2m arena)')
    axis.legend()