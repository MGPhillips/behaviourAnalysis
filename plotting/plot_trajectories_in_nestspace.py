###### Plot trajectories in nest space


fig, ax = plt.subplots(figsize=(6, 6))

colors = {'dark': 'mediumvioletred',
          'light': 'royalblue'}

count = 0

for ind in flight_df[(flight_df['expt_type'] == 'dark') & (flight_df['flight_success'] == 'successful')].index:

    if (int(ind)) % 3 != 0:
        continue
    if count == 0:
        ax.plot(
            flight_df[flight_df.index == ind]['x'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][
                0],
            flight_df[flight_df.index == ind]['y'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][
                1],
            color=colors['dark'], label='Dark')

    ax.plot(
        flight_df[flight_df.index == ind]['x'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][0],
        flight_df[flight_df.index == ind]['y'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][1],
        color=colors['dark'])

    count += 1

count = 0
for ind in flight_df[(flight_df['expt_type'] == 'light') & (flight_df['flight_success'] == 'successful')].index:

    if (int(ind)) % 3 != 0:
        continue
    if count == 0:
        ax.plot(
            flight_df[flight_df.index == ind]['x'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][
                0],
            flight_df[flight_df.index == ind]['y'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][
                1],
            color=colors['light'], label='Light')

    ax.plot(
        flight_df[flight_df.index == ind]['x'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][0],
        flight_df[flight_df.index == ind]['y'][0][300:] - flight_df[flight_df.index == ind]['shelter_position'][0][1],
        color=colors['light'])

    count += 1

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(left=False, bottom=False, labelbottom=False, labelleft=False, )
ax.set_title('Trajectories in nest space (2 x 2m arena)')
ax.legend()
