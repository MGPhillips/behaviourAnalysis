fig, ax = plt.subplots(figsize=(20, 10))
mouse_ids = flight_df.groupby(['mouse_id']).groups.keys()

mouse_ratios = {}

for i, mouse_id in enumerate(recent_mice):

    mouse_df = flight_df[flight_df['mouse_id'] == mouse_id]

    n_total_flights = len(mouse_df.index)
    n_dark_flights = len(mouse_df[mouse_df['expt_type'] == 'dark'].index)
    n_light_flights = len(mouse_df[mouse_df['expt_type'] == 'light'].index)
    try:
        total_success = mouse_df['flight_success'].value_counts()['successful'] / n_total_flights

    except:
        total_success = 0

    try:
        dark_success = mouse_df[
                           mouse_df['expt_type'] == 'dark']['flight_success'].value_counts()[
                           'successful'] / n_dark_flights
    except:
        dark_success = 0

    try:
        light_success = mouse_df[
                            mouse_df['expt_type'] == 'light']['flight_success'].value_counts()[
                            'successful'] / n_light_flights
    except:
        light_success = 0

    try:
        ax.scatter(i, total_success, color='black', alpha=0.5)
        ax.scatter(i, dark_success, color='magenta', alpha=0.5)
        ax.scatter(i, light_success, color='blue', alpha=0.5)

    except:
        print('could not plot...', mouse_id)

# ax.set_ylim(0,10)
ax.set_xticks(np.arange(len(recent_mice)))
ax.set_xticklabels(recent_mice, rotation=90)  # np.arange(len(mouse_ids)),